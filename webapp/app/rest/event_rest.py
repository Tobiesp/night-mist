import datetime
from flask import Response
from flask_login import login_required
from app.models.event_model import Event, EventInstance
from app.models.users_model import event_read_permission, event_write_permission, admin_permission
from app.repositories import database_repository
from app.request_model.event_instance_request import EventInstanceRequest
from app.request_model.event_request import EventRequest
from app.rest.generic_rest_api import GenericRestAPI


class EventRestAPI(GenericRestAPI[Event]):
    def __init__(self):
        super().__init__(
            Event,
            'events',
            EventRequest,
            event_read_permission,
            event_write_permission,
            event_write_permission,
            admin_permission)


        self.blueprint.add_url_rule('/<string:event_id>/instance', view_func=self.start_event_instance, methods=['POST'])
        self.blueprint.add_url_rule('/<string:event_id>/instances', view_func=self.get_event_instances, methods=['GET'])
        self.blueprint.add_url_rule('/<string:event_id>/instances/count', view_func=self.get_event_instance_count, methods=['GET'])

    @login_required
    def start_event_instance(event_id: str):
        with event_write_permission.require(http_exception=403):
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
                return event_instance.to_response()
            else:
                last_event_instance = database.get_latest_event_instance(event)
                if last_event_instance is not None and last_event_instance.completed is False:
                    if interval.is_event_passed(last_event_instance.event_date):
                        last_event_instance = database.complete_event_instance(last_event_instance)
                        date = interval.get_next_event_date(last_event_instance.event_date)
                        event_instance = database.start_event_instance_for_event(event, date)
                        return Response(status=201, response=event_instance.to_json())
                    else:
                        return last_event_instance.to_response()
                else:
                    date = interval.get_next_event_date(last_event_instance.event_date if last_event_instance is not None else datetime.now())
                    event_instance = database.start_event_instance_for_event(event, date)
                return Response(status=201, response=event_instance.to_json())
        
    @login_required
    def get_event_instances(event_id: str):
        with event_read_permission.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_event_db_repository()
            event = database.get_event_by_id(event_id)
            if event is None:
                return Response(status=404, response='Event not found')
            event_instances = database.get_event_instances_by_event(event_id)
            event_instances = [event_instance.to_response() for event_instance in event_instances]
            return event_instances

    @login_required
    def get_event_instance_count(event_id: str):
        with event_read_permission.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_event_db_repository()
            count = database.get_event_instance_count_by_event(event_id)
            return {'count': count}
        

class EventInstanceRestAPI(GenericRestAPI[EventInstance]):
    def __init__(self):
        super().__init__(
            EventInstance,
            'events/instances',
            EventInstanceRequest,
            event_read_permission,
            event_write_permission,
            event_write_permission,
            admin_permission)
        self.blueprint.add_url_rule('/<string:event_instance_id>/complete', view_func=self.end_event_instance, methods=['POST'])

    @login_required
    def end_event_instance(event_instance_id: str):
        with event_write_permission.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_event_db_repository()
            event_instance = database.get_event_instance_by_id(event_instance_id)
            if event_instance is None:
                return Response(status=404)
            event_instance = database.complete_event_instance(event_instance)
            return event_instance.to_response()
