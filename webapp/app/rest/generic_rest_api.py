from typing import Generic, TypeVar
from flask import Blueprint, Response, request
from flask_login import login_required
from flask_principal import Permission
from pydantic import BaseModel

from app.models.base_db_model import BaseDBModel
from app.repositories import database_repository
from app.repositories.base_database_repository import BaseDatabaseRepository
from app.request_model.query_request import QueryRequest

T = TypeVar('T', bound=BaseDBModel)
D = TypeVar('D', bound=BaseDatabaseRepository[T])

class GenericRestAPI(Generic[T]):
    blueprint: Blueprint

    def __init__(self, model: Generic[T], root_url: str, request_cls, read_permissions: Permission, write_permissions: Permission, delete_permissions: Permission, purge_permissions: Permission):
        self._root_url_ = root_url
        self._db_: BaseDatabaseRepository[T] = database_repository.DatabaseRepository.instance().get_model_db_repository(model)
        self._read_permissions_ = read_permissions
        if self._read_permissions_ is None:
            raise Exception('Read permissions are required')
        self._write_permissions_ = write_permissions
        self._delete_permissions_ = delete_permissions
        self._purge_permissions_ = purge_permissions
        self._request_cls_ = request_cls
        self._model_ = model
        self.blueprint = Blueprint(f'{model.__name__}_api', __name__, url_prefix=f'/{root_url}')
        self.blueprint.add_url_rule('', view_func=self.get_all, methods=['GET'])
        self.blueprint.add_url_rule('/<string:id>', view_func=self.get_by_id, methods=['GET'])
        self.blueprint.add_url_rule('/query', view_func=self.query, methods=['GET'])
        self.blueprint.add_url_rule('/count', view_func=self.count, methods=['GET'])
        if self._write_permissions_ is not None:
            self.blueprint.add_url_rule('', view_func=self.create, methods=['POST'])
            self.blueprint.add_url_rule('/<string:id>', view_func=self.update, methods=['PUT'])
        if self._delete_permissions_ is not None:
            self.blueprint.add_url_rule('/<string:id>', view_func=self.delete, methods=['DELETE'])
        if hasattr(self._model_, 'deleted') and self._purge_permissions_ is not None:
            self.blueprint.add_url_rule('/purge', view_func=self.purge, methods=['DELETE'])

    def _can_delete_check_(self, item: T) -> bool:
        return True
    
    def _can_update_check_(self, instance: T) -> bool:
        return True

    @login_required
    def get_all(self):
        with self._read_permissions_.require(http_exception=403):
            items = self._db_.get_all()
            items = [item.to_response() for item in items]
            return items
        
    @login_required
    def get_by_id(self, id: str):
        with self._read_permissions_.require(http_exception=403):
            item = self._db_.get_by_id(id)
            if item is None:
                return Response(status=404, response=f'{T.__class__} not found')
            return item.to_response()
        
    @login_required
    def create(self):
        with self._write_permissions_.require(http_exception=403):
            json_data = request.get_json(silent=True) or {}

            try:
                request_data = self._request_cls_(**json_data)
            except TypeError:
                return Response(status=400, response='Invalid request type')
            except ValueError as ve:
                return Response(status=400, response=str(ve))
            # find all database model classes in the request data
            for key, value in request_data.__dict__.items():
                if isinstance(value, BaseModel) and hasattr(value, 'id'):
                    model_name = value.__class__.__name__.replace('Request', '')
                    model = getattr(__import__('app.models', fromlist=[model_name]), model_name)
                    temp_db = database_repository.DatabaseRepository.instance().get_model_db_repository(model)
                    request_data.__dict__[key] = temp_db.get_by_id(value.id)
                if isinstance(value, list):
                    # find all database model classes in the list
                    temp_db = None
                    for item in value:
                        if not hasattr(item, 'id'):
                            continue
                        model_name = item.__class__.__name__.replace('Request', '')
                        model = getattr(__import__('app.models', fromlist=[model_name]), model_name)
                        temp_db = database_repository.DatabaseRepository.instance().get_model_db_repository(model)
                        break
                    if temp_db is None:
                        return Response(status=400, response='Invalid request type')
                    request_data.__dict__[key] = [temp_db.get_by_id(item.id) for item in value]
            item = self._db_.create(**request_data.__dict__)
            return item.to_response(), 201
        
    @login_required
    def update(self, id: str):
        with self._write_permissions_.require(http_exception=403):
            json_data = request.get_json(silent=True) or {}
            try:
                request_data = self._request_cls_(**json_data)
            except TypeError:
                return Response(status=400, response='Invalid request type')
            except ValueError as ve:
                return Response(status=400, response=str(ve))
            self._can_update_check_(request_data)
            # find all database model classes in the request data
            for key, value in request_data.__dict__.items():
                if key == 'id':
                    continue
                if isinstance(value, BaseModel) and hasattr(value, 'id'):
                    model_name = value.__class__.__name__.replace('Request', '')
                    model = getattr(__import__('app.models', fromlist=[model_name]), model_name)
                    temp_db = database_repository.DatabaseRepository.instance().get_model_db_repository(model)
                    request_data.__dict__[key] = temp_db.get_by_id(value.id)
                if isinstance(value, list):
                    # find all database model classes in the list
                    temp_db = None
                    for item in value:
                        if not hasattr(item, 'id'):
                            continue
                        model_name = item.__class__.__name__.replace('Request', '')
                        model = getattr(__import__('app.models', fromlist=[model_name]), model_name)
                        temp_db = database_repository.DatabaseRepository.instance().get_model_db_repository(model)
                        break
                    if temp_db is None:
                        return Response(status=400, response='Invalid request type')
                    request_data.__dict__[key] = [temp_db.get_by_id(item.id) for item in value]
            if 'id' in request_data.__dict__:
                del request_data.__dict__['id']
            for key in self._model_.read_only_fields():
                if key in request_data.__dict__:
                    del request_data.__dict__[key]
            item = self._db_.update(id=id, **request_data.__dict__)
            return item.to_response()

    @login_required
    def delete(self, id: str):
        with self._delete_permissions_.require(http_exception=403):
            item = self._db_.get_by_id(id)
            if item is None:
                return Response(status=404)
            if self._can_delete_check_(item):
                item = self._db_.delete(id)
                return item.to_response()
        
    @login_required
    def purge(self):
        with self._purge_permissions_.require(http_exception=403):
            self._db_.purge()
            return Response(status=200)
        
    @login_required
    def query(self):
        with self._read_permissions_.require(http_exception=403):
            try:
                request_args = QueryRequest(request.args)
            except TypeError:
                return Response(status=400, response='Invalid request type')
            except ValueError as ve:
                return Response(status=400, response=str(ve))
            
            results = set()

            if request_args.filter_value == '':
                results = self._db_.get_all()
            else:
                fields = self._model_.query_fields()
                if len(fields) > 0:
                    for f in fields:
                        if f['model'] is None:
                            results.update(self._db_.get_by(**{f['field']: request_args.filter_value}))
            if request_args.sort_active != '':
                if request_args.sort_direction == 'asc':
                    results = sorted(results, key=lambda x: getattr(x, request_args.sort_active))
                else:
                    results = sorted(results, key=lambda x: getattr(x, request_args.sort_active), reverse=True)
            start_index = (request_args.page_num) * request_args.page_size
            end_index = start_index + request_args.page_size
            results = results[start_index:end_index]
            results = [item.to_response() for item in results]
            return results

    @login_required
    def count(self):
        with self._read_permissions_.require(http_exception=403):
            count = self._db_.get_count()
            return {'count': count}
        
    def get_blueprint(self) -> Blueprint:
        return self.blueprint