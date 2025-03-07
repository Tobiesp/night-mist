from flask import Blueprint, Response, request
from app.models.event_model import Point
from app.models.users_model import event_read_permission, event_write_permission, admin_permission
from app.repositories import database_repository
from app.request_model.point_request import PointRequest
from app.response_model.point_response import PointListResponse, PointResponse


point_api = Blueprint('point_api', __name__, url_prefix='/points')


@point_api.route('/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_all_points():
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    points = database.get_all_points()
    return Response(status=200, response=PointListResponse(points).get_response())


@point_api.route('/<string:point_id>/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_point(point_id: str):
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    point = database.get_point_by_id(point_id)
    if point is None:
        return Response(status=404)
    return Response(status=200, response=PointResponse(point).get_response())


@point_api.route('/', methods=['POST'])
@event_write_permission.require(http_exception=403)
def create_point():
    json_data = request.get_json(silent=True) or {}
    try:
        point_request = PointRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    point_category = database.get_point_category_by_id(point_request.point_category.id)
    if point_category is None:
        return Response(status=400, response='Invalid point_category id')
    student_group_instance = database_repository.DatabaseRepository.instance().get_student_db_repository().get_group_by_id(point_request.student_group.id)
    if student_group_instance is None:
        return Response(status=400, response='Invalid group instance id')
    point = Point(
        point_category=point_category,
        student_group=student_group_instance,
        points=point_request.points,
        points_interval=point_request.points_interval
    )
    point = database.create_point(point)
    return Response(status=200, response=PointResponse(point).get_response())


@point_api.route('/<string:point_id>/', methods=['PUT'])
@event_write_permission.require(http_exception=403)
def update_point(point_id: str):
    json_data = request.get_json(silent=True) or {}
    try:
        point_request = PointRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    point = database.get_point_by_id(point_id)
    if point is None:
        return Response(status=404)
    point_category = database.get_point_category_by_id(point_request.point_category.id)
    if point_category is None:
        return Response(status=400, response='Invalid point_category id')
    student_group_instance = database_repository.DatabaseRepository.instance().get_student_db_repository().get_group_by_id(point_request.student_group.id)
    if student_group_instance is None:
        return Response(status=400, response='Invalid group instance id')
    point.point_category = point_category
    point.student_group = student_group_instance
    point.points = point_request.points
    point.points_interval = point_request.points_interval
    point = database.update_point(point)
    return Response(status=200, response=PointResponse(point).get_response())


@point_api.route('/<string:point_id>/', methods=['DELETE'])
@event_write_permission.require(http_exception=403)
def delete_point(point_id: str):
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    point = database.get_point_by_id(point_id)
    if point is None:
        return Response(status=404)
    database.delete_point(point)
    return Response(status=200)


@point_api.route('/purge/', methods=['DELETE'])
@admin_permission.require(http_exception=403)
def purge_points():
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    database.purge_points()
    return Response(status=200)


@point_api.route('/count/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_point_count():
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    count = database.get_point_count()
    return Response(status=200, response={'count': count})


@point_api.route('/query/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def query_points():
    request_args = request.args or {}
    filter_value = request_args.get('filter_value') or ''
    page_num = request_args.get('page_num') or 1
    page_size = request_args.get('page_size') or 100
    sort_active = request_args.get('sort_active') or ''
    sort_direction = request_args.get('sort_direction') or ''
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    points = set()
    if filter_value == '':
        points = database.get_all_points()
    else:
        categories = database.get_point_category_by_name(filter_value)
        if categories is None:
            return Response(status=200, response=[])
        if len(categories) > 10:
            categories = categories[:10]
        student_groups = database_repository.DatabaseRepository.instance().get_student_db_repository().get_group_by_name(filter_value)
        if student_groups is None:
            return Response(status=200, response=[])
        if len(student_groups) > 10:
            student_groups = student_groups[:10]
        for c in categories:
            for s in student_groups:
                points.update(database.get_point_by_point_category_and_student_group(c, s))
        points = list(points)
    if sort_active != '':
        if sort_direction == 'asc':
            points = sorted(points, key=lambda x: getattr(x, sort_active))
        else:
            points = sorted(points, key=lambda x: getattr(x, sort_active), reverse=True)
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    points = points[start_index:end_index]
    return Response(status=200, response=PointListResponse(points).get_response())
