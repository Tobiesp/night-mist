from flask import Blueprint, Response, request
from app.models.event_model import PointCategory
from app.models.users_model import event_read_permission, event_write_permission, admin_permission
from app.repositories import database_repository
from app.request_model.point_category_request import PointCategoryRequest
from app.response_model.point_category_response import PointCategoryListResponse, PointCategoryResponse


point_category_api = Blueprint('point_category_api', __name__, url_prefix='/point_categories')


@point_category_api.route('/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_all_point_categories():
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    point_categories = database.get_all_point_categories()
    return Response(status=200, response=PointCategoryListResponse(point_categories).get_response())


@point_category_api.route('/<string:point_category_id>/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_point_category(point_category_id: str):
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    point_category = database.get_point_category_by_id(point_category_id)
    if point_category is None:
        return Response(status=404)
    return Response(status=200, response=PointCategoryResponse(point_category).get_response())


@point_category_api.route('/', methods=['POST'])
@event_write_permission.require(http_exception=403)
def create_point_category():
    json_data = request.get_json(silent=True) or {}
    try:
        point_category_request = PointCategoryRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    point_category = PointCategory()
    point_category.category_name = point_category_request.category_name
    point_category.description = point_category_request.description
    point_category = database.create_point_category(point_category)
    return Response(status=200, response=PointCategoryResponse(point_category).get_response())


@point_category_api.route('/<string:point_category_id>/', methods=['PUT'])
@event_write_permission.require(http_exception=403)
def update_point_category(point_category_id: str):
    json_data = request.get_json(silent=True) or {}
    try:
        point_category_request = PointCategoryRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    point_category = database.get_point_category_by_id(point_category_id)
    if point_category is None:
        return Response(status=404)
    point_category.category_name = point_category_request.category_name
    point_category.description = point_category_request.description
    database.update_point_category(point_category)
    return Response(status=200, response=PointCategoryResponse(point_category).get_response())


@point_category_api.route('/<string:point_category_id>/', methods=['DELETE'])
@event_write_permission.require(http_exception=403)
def delete_point_category(point_category_id: str):
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    point_category = database.get_point_category_by_id(point_category_id)
    if point_category is None:
        return Response(status=404)
    database.delete_point_category(point_category)
    return Response(status=200)


@point_category_api.route('/purge/', methods=['DELETE'])
@admin_permission.require(http_exception=403)
def purge_point_categories():
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    database.purge_point_categories()
    return Response(status=200)

@point_category_api.route('/query/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def query_point_categories():
    request_args = request.args or {}
    filter_value = request_args.get('filter_value') or ''
    page_num = request_args.get('page_num') or 1
    page_size = request_args.get('page_size') or 100
    sort_active = request_args.get('sort_active') or ''
    sort_direction = request_args.get('sort_direction') or ''
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    categories = []
    if filter_value == '':
        categories = database.get_all_point_categories()
    else:
        categories = database.get_point_category_by_name(filter_value)
    if sort_active != '':
        if sort_direction == 'asc':
            categories = sorted(categories, key=lambda x: getattr(x, sort_active))
        else:
            categories = sorted(categories, key=lambda x: getattr(x, sort_active), reverse=True)
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    categories = categories[start_index:end_index]
    return Response(status=200, response=PointCategoryListResponse(categories).get_response())


@point_category_api.route('/count/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_point_category_count():
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    count = database.get_point_category_count()
    return Response(status=200, response={'count': count})