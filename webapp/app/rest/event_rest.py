import datetime
from flask import Response
from flask_login import login_required
from app.models.base_db_model import Interval
from app.models.event_model import Event, EventInstance
from app.models.users_model import event_read_permission, event_write_permission, admin_permission
from app.repositories import database_repository
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
        if self._write_permissions_ is not None:
            self.blueprint.add_url_rule('/<string:event_id>/instance', view_func=self.start_event_instance, methods=['POST'])
            self.blueprint.add_url_rule('/<string:event_id>/complete', view_func=self.end_event, methods=['POST'])
            self.blueprint.add_url_rule('/<string:event_id>/instance/<string:instance_id>/complete', view_func=self.end_event_instance, methods=['POST'])
        self.blueprint.add_url_rule('/<string:event_id>/instance/last', view_func=self.getLastInstance, methods=['GET'])
        self.blueprint.add_url_rule('/<string:event_id>/instance/<string:event_instance_id>', view_func=self.getInstance, methods=['GET'])
        self.blueprint.add_url_rule('/<string:event_id>/instances', view_func=self.get_event_instances, methods=['GET'])
        self.blueprint.add_url_rule('/<string:event_id>/instances/count', view_func=self.get_event_instance_count, methods=['GET'])
        if self._delete_permissions_ is not None:
            self.blueprint.add_url_rule('/<string:event_id>/instance/<string:instance_id>', view_func=self.delete_event_instance, methods=['DELETE'])
        if self._purge_permissions_ is not None:
            self.blueprint.add_url_rule('/<string:event_id>/instances/purge', view_func=self.purge_instances, methods=['DELETE'])

    def _get_latest_event_instance_(self, event: Event) -> EventInstance | None:
        database = database_repository.DatabaseRepository.instance().get_model_db_repository(EventInstance)
        eventInstances: list[EventInstance] = database.get_by_and(event=event)
        if len(eventInstances) == 0:
            return None
        eventInstances.sort(key=lambda x: x.event_date, reverse=True)
        return eventInstances[0]

    @login_required
    def getInstance(self, event_id: str, event_instance_id: str):
        with self._read_permissions_.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(Event)
            event: Event | None = database.get_by_id(event_id)
            if event is None:
                return Response(status=404, response='Event not found')
            instance_db = database_repository.DatabaseRepository.instance().get_model_db_repository(EventInstance)
            event_instance: EventInstance | None = instance_db.get_by_id(event_instance_id)
            if event_instance is None:
                return Response(status=404, response='Event instance not found')
            if event_instance.event_id != event.id:
                return Response(status=404, response=f'Event instance with id [{event_instance.id}] is not part of event: {event.event_name}')
            return event_instance.to_response(), 200

    @login_required
    def getLastInstance(self, event_id: str):
        with self._read_permissions_.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(Event)
            event = database.get_by_id(event_id)
            if event is None:
                return Response(status=404, response='Event not found')
            event_instance = self._get_latest_event_instance_(event)
            if event_instance is None:
                return Response(status=404, response='No event instances found')
            return event_instance.to_response(), 200

    @login_required
    def start_event_instance(self, event_id: str):
        with self._write_permissions_.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(Event)
            event: Event | None = database.get_by_id(event_id)
            if event is None:
                return Response(status=404)
            if event.completed:
                return Response(status=400, response='Event is completed')
            interval: Interval | None = event.interval
            if interval is None or interval.repeat == 'none':
                event_instance: EventInstance | None = self._get_latest_event_instance_(event)
                if event_instance is not None:
                    return event_instance.to_response(), 200
                else:
                    event_instance = EventInstance(event=event, event_date=datetime.datetime.now(), completed=False, deleted=False)
                    event_instance = database.create(**event_instance.__dict__)
                return event_instance.to_response(), 201
            else:
                event_instance: EventInstance | None = self._get_latest_event_instance_(event)
                if event_instance is not None:
                    if event_instance.completed:
                        date = interval.get_next_date(event_instance.event_date)
                        event_instance = EventInstance(event=event, event_date=date, completed=False, deleted=False)
                        event_instance = database.create(**event_instance.__dict__)
                        return event_instance.to_response(), 201
                    return event_instance.to_response(), 200
                else:
                    date = interval.get_next_date(datetime.datetime.now())
                    event_instance = EventInstance(event=event, event_date=date, completed=False, deleted=False)
                    event_instance = database.create(**event_instance.__dict__)
                return event_instance.to_response(), 201
        
    @login_required
    def get_event_instances(self, event_id: str):
        with self._read_permissions_.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(Event)
            event = database.get_by_id(event_id)
            if event is None:
                return Response(status=404, response='Event not found')
            instance_db = database_repository.DatabaseRepository.instance().get_model_db_repository(EventInstance)
            event_instances: list[EventInstance] = instance_db.get_by_and(event=event)
            if len(event_instances) == 0:
                return Response(status=404, response="No event instances found")
            event_instances = [event_instance.to_response() for event_instance in event_instances]
            return event_instances

    @login_required
    def get_event_instance_count(self, event_id: str):
        with self._read_permissions_.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(Event)
            event = database.get_by_id(event_id)
            if event is None:
                return Response(status=404, response='Event not found')
            instance_db = database_repository.DatabaseRepository.instance().get_model_db_repository(EventInstance)
            count = instance_db.get_count(event=event)
            return {'count': count}, 200
        
    @login_required
    def end_event_instance(self, event_id: str, event_instance_id: str):
        with self._write_permissions_.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(Event)
            event = database.get_by_id(event_id)
            if event is None:
                return Response(status=404, response='Event not found')
            instance_db = database_repository.DatabaseRepository.instance().get_model_db_repository(EventInstance)
            event_instance: EventInstance | None = instance_db.get_by_id(event_instance_id)
            if event_instance is None:
                return Response(status=404, response='Event instance not found')
            event_instance.completed = True
            ei_dict = event_instance.__dict__
            if 'id' in ei_dict:
                del ei_dict['id']
            event_instance = instance_db.update(event_instance_id, **ei_dict)
            return event_instance.to_response(), 204

    @login_required
    def end_event(self, event_id: str):
        with self._write_permissions_.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(Event)
            event: Event | None = database.get_by_id(event_id)
            if event is None:
                return Response(status=404, response='Event not found')
            if event.completed:
                return event.to_response(), 200
            event_instance = self._get_latest_event_instance_(event)
            if event_instance is None:
                return event.to_response(), 200
            event_instance.completed = True
            ei_dict = event_instance.__dict__
            if 'id' in ei_dict:
                del ei_dict['id']
            instance_db = database_repository.DatabaseRepository.instance().get_model_db_repository(EventInstance)
            event_instance = instance_db.update(event_instance.id, **ei_dict)
            return event.to_response(), 204
    
    @login_required
    def delete_event_instance(self, event_id: str, event_instance_id: str):
        with self._delete_permissions_.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(Event)
            event = database.get_by_id(event_id)
            if event is None:
                return Response(status=404, response='Event not found')
            instance_db = database_repository.DatabaseRepository.instance().get_model_db_repository(EventInstance)
            event_instance: EventInstance | None = instance_db.get_by_id(event_instance_id)
            if event_instance is None:
                return Response(status=404, response='Event instance not found')
            instance_db.delete(event_instance_id)
            return Response(status=200)
    
    @login_required
    def purge_instances(self, event_id: str):
        with self._purge_permissions_.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(Event)
            event = database.get_by_id(event_id)
            if event is None:
                return Response(status=404, response='Event not found')
            instance_db = database_repository.DatabaseRepository.instance().get_model_db_repository(EventInstance)
            instance_db.purge(event=event)
            return Response(status=200)
