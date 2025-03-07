from typing import Optional

from app.models.event_model import EventInstance
from app.response_model.event_response import EventResponse


class EventInstanceResponse():
    
    def __init__(self, event_instance: Optional[EventInstance]):
        self._event_instance_ = None
        if event_instance is not None:
            self._event_instance_ = event_instance

    def get_response(self) -> dict | None:
        if self._event_instance_ is None:
            return None
        return {
            'id': self._event_instance_.id,
            'event': EventResponse(self._event_instance_.event).get_response(),
            'event_date': str(self._event_instance_.event_date),
        }
    

class EventInstanceListResponse():
    
    def __init__(self, event_instances: list[EventInstance]):
        self.event_instances = event_instances

    def get_response(self) -> list[dict]:
        return [EventInstanceResponse(event_instance).get_response() for event_instance in self.event_instances]