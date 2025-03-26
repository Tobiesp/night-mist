from typing import Generic, Optional, TypeVar
import uuid

from flask import Flask, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

from app.models.base_db_model import BaseDBModel


T = TypeVar('T', bound=BaseDBModel)

class BaseDatabaseRepository(Generic[T]):
    def __init__(self, model: Generic[T], app: Flask = None, db: SQLAlchemy = None):
        self.model = model
        self._app_ = app
        self._db_ = db
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_.session.close()

    def _paginate(self, query, page=0, pageSize=100):
        if page < 0:
            page = 0
        if pageSize < 0:
            pageSize = 100
        return query.offset(page * pageSize).limit(pageSize)
    
    def sort(self, query, sort_field: Optional[str] = None, sort_direction='desc'):
        if sort_field is not None and self.model.__dict__.get(sort_field) is not None:
            if sort_direction == 'desc':
                query = query.order_by(getattr(self.model, sort_field).desc())
            else:
                query = query.order_by(getattr(self.model, sort_field).asc())
        return query

    def get_all(self, page=0, pageSize=100, sort_field: Optional[str] = None, sort_direction='desc') -> list[T]:
        with self._app_.app_context():
            query = self._db_.session.query(self.model)
            if hasattr(self.model, 'deleted'):
                query = query.filter_by(deleted=False)
            query = self.sort(query=query, sort_field=sort_field, sort_direction=sort_direction)
            items = self._paginate(query=query, page=page, pageSize=pageSize).all()
            return items

    def get_by_id(self, id: str) -> T:
        uuid_id = uuid.UUID(id)
        with self._app_.app_context():
            return self._db_.session.query(self.model).get(uuid_id)

    def create(self, **kwargs) -> T:
        with self._app_.app_context():
            kwargs = {key: value for key, value in kwargs.items() if key in self.model.__dict__ and not key.startswith('_') and key != 'id'}
            for key, value in kwargs.items():
                # check if value is a database model class
                if hasattr(value, 'id') or (isinstance(value, dict) and 'id' in value):
                    if isinstance(value, dict):
                        related_model = getattr(self.model, key).property.mapper.class_
                        if value['id'] is None or value['id'] == '':
                            value = None
                        else:
                            tmp_uuid = uuid.UUID(value['id']) if isinstance(value['id'], str) else value['id']
                            tmp = self._db_.session.query(related_model).filter_by(id=tmp_uuid).first()
                            if tmp is None:
                                value = None
                            else:
                                value = tmp
                    else:
                        value = self._db_.session.query(value.__class__).get(value.id)
                # Check if value is a list of database model classes
                if isinstance(value, list):
                    value = [self._db_.session.query(item.__class__).get(item.id) for item in value]
                if isinstance(value, dict) and key.find('interval') != -1:
                    related_model = getattr(self.model, key).property.mapper.class_
                    value = related_model(**value)
                kwargs[key] = value
            new_instance = self.model(**kwargs)
            self._db_.session.add(new_instance)
            self._db_.session.commit()
            return new_instance

    def update(self, id: str, **kwargs) -> T:
        if id is None or id == '':
            return Response(status=400, response='ID is required')
        with self._app_.app_context():
            uuid_id = uuid.UUID(id)
            instance: T = self._db_.session.query(self.model).filter_by(id=uuid_id).first()
            kwargs = {key: value for key, value in kwargs.items() if key in self.model.__dict__ and not key.startswith('_') and key != 'id'}
            for key, value in kwargs.items():
                # check if value is a database model class
                if hasattr(value, 'id') or (isinstance(value, dict) and 'id' in value):
                    if isinstance(value, dict):
                        related_model = getattr(self.model, key).property.mapper.class_
                        if value['id'] is None or value['id'] == '':
                            value = None
                        else:
                            tmp_uuid = uuid.UUID(value['id']) if isinstance(value['id'], str) else value['id']
                            tmp = self._db_.session.query(related_model).filter_by(id=tmp_uuid).first()
                            if tmp is None:
                                value = None
                            else:
                                value = tmp
                    else:
                        value = self._db_.session.query(value.__class__).get(value.id)
                # Check if value is a list of database model classes
                if isinstance(value, list):
                    value = [self._db_.session.query(item.__class__).get(item.id) for item in value]
                if isinstance(value, dict) and key.find('interval') != -1:
                    related_model = getattr(self.model, key).property.mapper.class_
                    value = related_model(**value)
                setattr(instance, key, value)
            self._db_.session.commit()
            return instance

    def delete(self, id) -> T:
        with self._app_.app_context():
            instance = self.get_by_id(id)
            # Check if model has a deleted column
            if hasattr(instance, 'deleted'):
                instance.deleted = True
                self._db_.session.commit()
                return instance
            self._db_.session.delete(instance)
            self._db_.session.commit
        return instance
    
    def purge(self, **kwargs) -> None:
        with self._app_.app_context():
            if kwargs is not None:
                if hasattr(self.model, 'deleted'):
                    instances = self._db_.session.query(self.model).filter_by(deleted=False, **kwargs).all()
                    for instance in instances:
                        self._db_.session.delete(instance)
                    self._db_.session.commit()
            else:
                if hasattr(self.model, 'deleted'):
                    instances = self._db_.session.query(self.model).filter_by(deleted=True).all()
                    for instance in instances:
                        self._db_.session.delete(instance)
                    self._db_.session.commit()

    def get_count(self, **kwargs) -> int:
        with self._app_.app_context():
            if kwargs is not None:
                if hasattr(self.model, 'deleted'):
                    return self._db_.session.query(self.model).filter_by(deleted=False, **kwargs).count()
                return self._db_.session.query(self.model).filter_by(**kwargs).count()
            else:
                if hasattr(self.model, 'deleted'):
                    return self._db_.session.query(self.model).filter_by(deleted=False).count()
                return self._db_.session.query(self.model).count()
        
    def get_by_and(self, page=0, pageSize=0, sort_field: Optional[str] = None, sort_direction='desc', **kwargs) -> list[T]:
        with self._app_.app_context():
            query  = self._db_.session.query(self.model)
            if hasattr(self.model, 'deleted'):
                query = query.filter_by(deleted=False, **kwargs)
            else:
                query = query.filter_by(**kwargs)
            query = self.sort(query=query, sort_field=sort_field, sort_direction=sort_direction)
            query = self._paginate(query=query, page=page, pageSize=pageSize)
            return query.all()
        
    def get_by_or(self, page=0, pageSize=0, sort_field: Optional[str] = None, sort_direction='desc', **kwargs) -> list[T]:
        with self._app_.app_context():
            filters = [getattr(self.model, key).ilike(f"%{value}%") for key, value in kwargs.items()]
            query  = self._db_.session.query(self.model)
            if hasattr(self.model, 'deleted'):
                query = query.filter_by(deleted=False).filter(or_(*filters))
            else:
                query = query.filter(or_(*filters))
            query = self.sort(query=query, sort_field=sort_field, sort_direction=sort_direction)
            query = self._paginate(query=query, page=page, pageSize=pageSize)
            return query.all()
        
    def get_by_and_first(self, **kwargs) -> T:
        with self._app_.app_context():
            query  = self._db_.session.query(self.model)
            if hasattr(self.model, 'deleted'):
                return query.filter_by(deleted=False, **kwargs).first()
            else:
                return query.filter_by(**kwargs).first()
        
    def get_by_or_first(self, **kwargs) -> list[T]:
        with self._app_.app_context():
            filters = [getattr(self.model, key).ilike(f"%{value}%") for key, value in kwargs.items()]
            query  = self._db_.session.query(self.model)
            if hasattr(self.model, 'deleted'):
                return query.filter_by(deleted=False).filter(or_(*filters)).first()
            else:
                return query.filter(or_(*filters)).first()