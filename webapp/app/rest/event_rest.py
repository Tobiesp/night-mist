import datetime
from flask import Blueprint, Response, request
from app.models.event_model import Event, EventInstance
from app.models.users_model import event_read_permission, event_write_permission, admin_permission
from app.repositories import database_repository
from app.request_model.event_request import EventRequest
from app.response_model.event_instance_response import EventInstanceResponse
from app.response_model.event_response import EventListResponse, EventResponse
from app.response_model.user_response import UserListResponse


event_api = Blueprint('event_api', __name__, url_prefix='/events')


@event_api.route('/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_events():
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    events = database.get_all_events()
    return Response(status=200, response=EventListResponse(events).get_response())


@event_api.route('/<string:event_id>/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_event(event_id: str):
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    event = database.get_event_by_id(event_id)
    if event is None:
        return Response(status=404)
    return Response(status=200, response=EventResponse(event).get_response())


@event_api.route('/', methods=['POST'])
@event_write_permission.require(http_exception=403)
def create_event():
    json_data = request.get_json(silent=True) or {}
    try:
        event_request = EventRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    student_groups = [database.get_event_by_id(s.id) for s in event_request.student_groups if s.id is not None]
    student_groups = [s for s in student_groups if s is not None]
    if len(student_groups) == 0:
        return Response(status=400, response='Cannot create event without groups')
    if len(event_request.student_groups) != len(student_groups):
        return Response(status=400, response='Invalid group id\'s')
    point_categories = [database.get_point_category_by_id(p.id) for p in event_request.point_categories if p.id is not None]
    point_categories = [p for p in point_categories if p is not None]
    if len(point_categories) == 0:
        return Response(status=400, response='Cannot create event without point categories')
    if len(event_request.point_categories) != len(point_categories):
        return Response(status=400, response='Invalid point category id\'s')
    event = Event(
        event_name=event_request.event_name,
        student_groups=student_groups,
        point_categories=point_categories
    )
    event.interval = event_request.event_interval
    event = database.create_event(event=event)
    return Response(status=200, response=EventResponse(event).get_response())


@event_api.route('/<string:event_id>/', methods=['PUT'])
@event_write_permission.require(http_exception=403)
def update_event(event_id: str):
    json_data = request.get_json(silent=True) or {}
    try:
        event_request = EventRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    event = database.get_event_by_id(event_id)
    if event is None:
        return Response(status=404)
    student_groups = [database.get_event_by_id(s.id) for s in event_request.student_groups if s.id is not None]
    student_groups = [s for s in student_groups if s is not None]
    if len(student_groups) == 0:
        return Response(status=400, response='Cannot create event without groups')
    if len(event_request.student_groups) != len(student_groups):
        return Response(status=400, response='Invalid group id\'s')
    point_categories = [database.get_point_category_by_id(p.id) for p in event_request.point_categories if p.id is not None]
    point_categories = [p for p in point_categories if p is not None]
    if len(point_categories) == 0:
        return Response(status=400, response='Cannot create event without point categories')
    if len(event_request.point_categories) != len(point_categories):
        return Response(status=400, response='Invalid point category id\'s')
    event.event_name = event_request.event_name
    event.student_groups = student_groups
    event.point_categories = point_categories
    event.interval = event_request.event_interval
    event = database.update_event(event=event)
    return Response(status=200, response=EventResponse(event).get_response())


@event_api.route('/<string:event_id>/', methods=['DELETE'])
@event_write_permission.require(http_exception=403)
def delete_event(event_id: str):
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    event = database.get_event_by_id(event_id)
    if event is None:
        return Response(status=404)
    database.delete_event(event)
    return Response(status=200)


@event_api.route('/purge/', methods=['DELETE'])
@admin_permission.require(http_exception=403)
def purge_events():
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    database.purge_events()
    return Response(status=200)


@event_api.route('/<string:event_id>/users/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_event_users(event_id: str):
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    event = database.get_event_by_id(event_id)
    if event is None:
        return Response(status=404)
    return Response(status=200, response=UserListResponse(event.users).get_response())


@event_api.route('/query/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def query_events():
    request_args = request.args or {}
    filter_value = request_args.get('filter_value') or ''
    page_num = request_args.get('page_num') or 1
    page_size = request_args.get('page_size') or 100
    sort_active = request_args.get('sort_active') or ''
    sort_direction = request_args.get('sort_direction') or ''
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    events = []
    if filter_value == '':
        events = database.get_all_events()
    else:
        events = database.get_event_by_name(filter_value)
    if sort_active != '':
        if sort_direction == 'asc':
            events = sorted(events, key=lambda x: getattr(x, sort_active))
        else:
            events = sorted(events, key=lambda x: getattr(x, sort_active), reverse=True)
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    events = events[start_index:end_index]
    return Response(status=200, response=EventListResponse(events).get_response())


@event_api.route('/count/', methods=['POST'])
@event_read_permission.require(http_exception=403)
def count_events():
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    count = database.get_event_count()
    return Response(status=200, response={'count': count})


@event_api.route('/<string:event_id>/instance/', methods=['POST'])
@event_write_permission.require(http_exception=403)
def start_event_instance(event_id: str):
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    event = database.get_event_by_id(event_id)
    if event is None:
        return Response(status=404)
    interval = event.interval
    if interval is None:
        event_instance = database.get_latest_event_instance(event)
        if event_instance is not None and event_instance.completed is False:
            if interval.is_event_passed(event_instance.event_date):
                event_instance = database.complete_event_instance(event_instance)
                date = interval.get_next_event_date(event_instance.event_date)
                event_instance = database.start_event_instance_for_event(event, date)
        else:
            date = interval.get_next_event_date(event_instance.event_date if event_instance is not None else datetime.now())
            event_instance = database.start_event_instance_for_event(event, date)
        return Response(status=201, response=EventInstanceResponse(event_instance).get_response())
    else:
        last_event_instance = database.get_latest_event_instance(event)
        if last_event_instance is not None and last_event_instance.completed is False:
            if interval.is_event_passed(last_event_instance.event_date):
                last_event_instance = database.complete_event_instance(last_event_instance)
                date = interval.get_next_event_date(last_event_instance.event_date)
                event_instance = database.start_event_instance_for_event(event, date)
                return Response(status=201, response=EventInstanceResponse(event_instance).get_response())
            return Response(status=201, response=EventInstanceResponse(last_event_instance).get_response())
        else:
            date = interval.get_next_event_date(last_event_instance.event_date if last_event_instance is not None else datetime.now())
            event_instance = database.start_event_instance_for_event(event, date)
            return Response(status=201, response=EventInstanceResponse(event_instance).get_response())
        

@event_api.route('/<string:event_id>/instances/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_event_instances(event_id: str):
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    event = database.get_event_by_id(event_id)
    if event is None:
        return Response(status=404, response='Event not found')
    event_instances = database.get_event_instances_by_event(event_id)
    return Response(status=200, response=EventInstanceResponse(event_instances).get_response())


@event_api.route('/instances/<string:event_instance_id>/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_event_instance(event_instance_id: str):
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    event_instance = database.get_event_instance_by_id(event_instance_id)
    if event_instance is None:
        return Response(status=404)
    return Response(status=200, response=EventInstanceResponse(event_instance).get_response())


@event_api.route('/instances/<string:event_instance_id>/', methods=['DELETE'])
@event_write_permission.require(http_exception=403)
def delete_event_instance(event_instance_id: str):
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    event_instance = database.get_event_instance_by_id(event_instance_id)
    if event_instance is None:
        return Response(status=404)
    database.delete_event_instance(event_instance)
    return Response(status=200)


@event_api.route('/instances/purge/', methods=['DELETE'])
@admin_permission.require(http_exception=403)
def purge_event_instances():
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    database.purge_event_instances()
    return Response(status=200)


@event_api.route('/instances/<string:event_instance_id>/complete/', methods=['POST'])
@event_write_permission.require(http_exception=403)
def end_event_instance(event_instance_id: str):
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    event_instance = database.get_event_instance_by_id(event_instance_id)
    if event_instance is None:
        return Response(status=404)
    event_instance = database.complete_event_instance(event_instance)
    return Response(status=200, response=EventInstanceResponse(event_instance).get_response())


@event_api.route('/<string:event_id>/instances/count/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_event_instance_count(event_id: str):
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    count = database.get_event_by_id(event_id).event_instances.count()
    return Response(status=200, response={'count': count})


@event_api.route('/instances/count/', methods=['GET'])
@event_read_permission.require(http_exception=403)
def get_event_instances_count():
    database = database_repository.DatabaseRepository.instance().get_event_db_repository()
    count = database.get_event_instance_count()
    return Response(status=200, response={'count': count})
