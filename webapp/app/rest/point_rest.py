from flask import Blueprint, Response, request
from app.models.event_model import Point
from app.models.point_model import PointEarned, PointSpent
from app.models.users_model import event_read_permission, event_write_permission, admin_permission, student_read_permission
from app.repositories import database_repository
from app.request_model.point_earned_request import PointEarnedRequest
from app.request_model.point_request import PointRequest
from app.request_model.point_spent_request import PointSpentRequest
from app.response_model.point_earned_response import PointEarnedListResponse, PointEarnedResponse
from app.response_model.point_response import PointListResponse, PointResponse
from app.response_model.point_spent_response import PointSpentListResponse, PointSpentResponse
from app.response_model.running_total_response import RunningTotalResponse, RunningTotalListResponse


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


@point_api.route('/earned/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_all_points_earned():
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    points_earned = database.get_all_points_earned()
    return Response(status=200, response=PointEarnedListResponse(points_earned).get_response())


@point_api.route('/earned/<string:point_earned_id>/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_point_earned(point_earned_id: str):
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    point_earned = database.get_point_earned_by_id(point_earned_id)
    if point_earned is None:
        return Response(status=404)
    return Response(status=200, response=PointEarnedResponse(point_earned).get_response())


@point_api.route('/earned/', methods=['POST'])
@event_write_permission.require(http_exception=403)
def create_point_earned():
    json_data = request.get_json(silent=True) or {}
    try:
        point_request = PointEarnedRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    event_db = database_repository.DatabaseRepository.instance().get_event_db_repository()
    student = database_repository.DatabaseRepository.instance().get_student_db_repository().get_student_by_id(point_request.student)
    if student is None:
        return Response(status=400, response=f'Invalid student id: {point_request.student}')
    event_instance = event_db.get_event_instance_by_id(point_request.eventInstance)
    if event_instance is None:
        return Response(status=400, response=f'Invalid event instance id: {point_request.eventInstance}')
    point = database.get_point_earned_by_id(point_request.point)
    if point is None:
        return Response(status=400, response=f'Invalid point id: {point_request.point}')
    point_earned = PointEarned()
    point_earned.student = student
    point_earned.event_instance = event_instance
    point_earned.point = point
    point_earned = database.create_point_earned(point_earned)
    database.update_running_total_by_student(student)
    return Response(status=200, response=PointEarnedResponse(point_earned).get_response())


@point_api.route('/earned/<string:point_earned_id>/', methods=['PUT'])
@event_write_permission.require(http_exception=403)
def update_point_earned(point_earned_id: str):
    json_data = request.get_json(silent=True) or {}
    try:
        point_request = PointEarnedRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    event_db = database_repository.DatabaseRepository.instance().get_event_db_repository()
    point_earned = database.get_point_earned_by_id(point_earned_id)
    if point_earned is None:
        return Response(status=404)
    student = database_repository.DatabaseRepository.instance().get_student_db_repository().get_student_by_id(point_request.student)
    if student is None:
        return Response(status=400, response=f'Invalid student id: {point_request.student}')
    event_instance = event_db.get_event_instance_by_id(point_request.eventInstance)
    if event_instance is None:
        return Response(status=400, response=f'Invalid event instance id: {point_request.eventInstance}')
    point = database.get_point_earned_by_id(point_request.point)
    if point is None:
        return Response(status=400, response=f'Invalid point id: {point_request.point}')
    point_earned.student = student
    point_earned.event_instance = event_instance
    point_earned.point = point
    point_earned = database.update_point_earned(point_earned)
    database.update_running_total_by_student(student)
    return Response(status=200, response=PointEarnedResponse(point_earned).get_response())


@point_api.route('/earned/<string:point_earned_id>/', methods=['DELETE'])
@event_write_permission.require(http_exception=403)
def delete_point_earned(point_earned_id: str):
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    point_earned = database.get_point_earned_by_id(point_earned_id)
    if point_earned is None:
        return Response(status=404)
    database.delete_point_earned(point_earned)
    student = database_repository.DatabaseRepository.instance().get_student_db_repository().get_student_by_id(point_earned.student_id)
    if student is None:
        return Response(status=500, response=f'Invalid student id: {point_earned.student.id}')
    database.update_running_total_by_student(student)
    return Response(status=200)


@point_api.route('/earned/purge/', methods=['DELETE'])
@admin_permission.require(http_exception=403)
def purge_points_earned():
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    database.purge_points_earned()
    return Response(status=200)


@point_api.route('/earned/count/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_point_earned_count():
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    count = database.get_point_earned_count()
    return Response(status=200, response={'count': count})


@point_api.route('/earned/query/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def query_points_earned():
    request_args = request.args or {}
    filter_value = request_args.get('filter_value') or ''
    page_num = request_args.get('page_num') or 1
    page_size = request_args.get('page_size') or 100
    sort_active = request_args.get('sort_active') or ''
    sort_direction = request_args.get('sort_direction') or ''
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    event_db = database_repository.DatabaseRepository.instance().get_event_db_repository()
    points_earned = set()
    if filter_value == '':
        points_earned = database.get_all_points_earned()
    else:
        points = event_db.get_point_category_by_name(filter_value)
        if points is None:
            return Response(status=200, response=[])
        if len(points) > 10:
            points = points[:10]
        for p in points:
            points_earned.update(database.get_points_earned_by_point(p))
        points_earned = list(points_earned)
    if sort_active != '':
        if sort_direction == 'asc':
            points_earned = sorted(points_earned, key=lambda x: getattr(x, sort_active))
        else:
            points_earned = sorted(points_earned, key=lambda x: getattr(x, sort_active), reverse=True)
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    points_earned = points_earned[start_index:end_index]
    return Response(status=200, response=PointEarnedListResponse(points_earned).get_response())


@point_api.route('/spent/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_all_points_spent():
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    points_spent = database.get_all_points_spent()
    return Response(status=200, response=PointSpentListResponse(points_spent).get_response())


@point_api.route('/spent/<string:point_spent_id>/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_point_spent(point_spent_id: str):
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    point_spent = database.get_point_spent_by_id(point_spent_id)
    if point_spent is None:
        return Response(status=404)
    return Response(status=200, response=PointSpentResponse(point_spent).get_response())


@point_api.route('/spent/', methods=['POST'])
@event_write_permission.require(http_exception=403)
def create_point_spent():
    json_data = request.get_json(silent=True) or {}
    try:
        point_request = PointSpentRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    event_db = database_repository.DatabaseRepository.instance().get_event_db_repository()
    student = database_repository.DatabaseRepository.instance().get_student_db_repository().get_student_by_id(point_request.student)
    if student is None:
        return Response(status=400, response=f'Invalid student id: {point_request.student}')
    event_instance = event_db.get_event_instance_by_id(point_request.eventInstance)
    if event_instance is None:
        return Response(status=400, response=f'Invalid event instance id: {point_request.eventInstance}')
    point_spent = PointSpent()
    point_spent.student = student
    point_spent.event_instance = event_instance
    point_spent.points = point_request.points
    point_spent = database.create_point_spent(point_spent)
    database.update_running_total_by_student(student)
    return Response(status=200, response=PointSpentResponse(point_spent).get_response())


@point_api.route('/spent/<string:point_spent_id>/', methods=['PUT'])
@event_write_permission.require(http_exception=403)
def update_point_spent(point_spent_id: str):
    json_data = request.get_json(silent=True) or {}
    try:
        point_request = PointSpentRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    event_db = database_repository.DatabaseRepository.instance().get_event_db_repository()
    point_spent = database.get_point_spent_by_id(point_spent_id)
    if point_spent is None:
        return Response(status=404)
    student = database_repository.DatabaseRepository.instance().get_student_db_repository().get_student_by_id(point_request.student)
    if student is None:
        return Response(status=400, response=f'Invalid student id: {point_request.student}')
    event_instance = event_db.get_event_instance_by_id(point_request.eventInstance)
    if event_instance is None:
        return Response(status=400, response=f'Invalid event instance id: {point_request.eventInstance}')
    point_spent.student = student
    point_spent.event_instance = event_instance
    point_spent.points = point_request.points
    point_spent = database.update_point_spent(point_spent)
    database.update_running_total_by_student(student)
    return Response(status=200, response=PointSpentResponse(point_spent).get_response())


@point_api.route('/spent/<string:point_spent_id>/', methods=['DELETE'])
@event_write_permission.require(http_exception=403)
def delete_point_spent(point_spent_id: str):
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    point_spent = database.get_point_spent_by_id(point_spent_id)
    if point_spent is None:
        return Response(status=404)
    database.delete_point_spent(point_spent)
    student = database_repository.DatabaseRepository.instance().get_student_db_repository().get_student_by_id(point_spent.student_id)
    if student is None:
        return Response(status=500, response=f'Invalid student id: {point_spent.student.id}')
    database.update_running_total_by_student(student)
    return Response(status=200)


@point_api.route('/spent/purge/', methods=['DELETE'])
@admin_permission.require(http_exception=403)
def purge_points_spent():
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    database.purge_points_spent()
    return Response(status=200)


@point_api.route('/spent/count/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_point_spent_count():
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    count = database.get_point_spent_count()
    return Response(status=200, response={'count': count})


@point_api.route('/spent/query/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def query_points_spent():
    request_args = request.args or {}
    page_num = request_args.get('page_num') or 1
    page_size = request_args.get('page_size') or 100
    sort_active = request_args.get('sort_active') or ''
    sort_direction = request_args.get('sort_direction') or ''
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    points_spent = set()
    points_spent = database.get_all_points_spent()
    if sort_active != '':
        if sort_direction == 'asc':
            points_spent = sorted(points_spent, key=lambda x: getattr(x, sort_active))
        else:
            points_spent = sorted(points_spent, key=lambda x: getattr(x, sort_active), reverse=True)
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    points_spent = points_spent[start_index:end_index]
    return Response(status=200, response=PointSpentListResponse(points_spent).get_response())


@point_api.route('/running-totals/', methods=['GET'])
@student_read_permission.require(http_exception=403)
def get_all_running_totals():
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    running_totals = database.get_all_running_totals()
    return Response(status=200, response=RunningTotalListResponse(running_totals).get_response())


@point_api.route('/running-totals/<string:student_id>/', methods=['GET'])
@student_read_permission.require(http_exception=403)
def get_running_total(student_id: str):
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    student = database_repository.DatabaseRepository.instance().get_student_db_repository().get_student_by_id(student_id)
    if student is None:
        return Response(status=400, response=f'Invalid student id: {student_id}')
    running_total = database.get_running_total_by_student(student)
    if running_total is None:
        return Response(status=404)
    return Response(status=200, response=RunningTotalResponse(running_total).get_response())


@point_api.route('/running-totals/update', methods=['POST'])
@event_write_permission.require(http_exception=403)
def update_running_totals():
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    students = database_repository.DatabaseRepository.instance().get_student_db_repository().get_all_students()
    for student in students:
        database.update_running_total_by_student(student)
    return Response(status=200)

@point_api.route('/running-totals/update/<string:student_id>/', methods=['GET'])
@event_write_permission.require(http_exception=403)
def update_running_total(student_id: str):
    database = database_repository.DatabaseRepository.instance().get_point_db_repository()
    student = database_repository.DatabaseRepository.instance().get_student_db_repository().get_student_by_id(student_id)
    if student is None:
        return Response(status=400, response=f'Invalid student id: {student_id}')
    database.update_running_total_by_student(student)
    return Response(status=200)