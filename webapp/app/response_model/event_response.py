from typing import Optional

from app.models.event_model import Event
from app.response_model.point_category_response import PointCategoryListResponse
from app.response_model.student_group_response import StudentGroupListResponse


class EventResponse():
    
    def __init__(self, event: Optional[Event]):
        self._event_ = None
        if event is not None:
            self._event_ = event

    def get_response(self) -> dict | None:
        if self._event_ is None:
            return None
        return {
            'id': self._event_.id,
            'event_name': self._event_.event_name,
            'event_interval': self._event_.interval.to_response(),
            'student_groups': StudentGroupListResponse(self._event_.student_groups).get_response(),
            'point_categories': PointCategoryListResponse(self._event_.point_categories).get_response(),
        }
    

class EventListResponse():
    
    def __init__(self, events: list[Event]):
        self.events = events

    def get_response(self) -> list[dict]:
        return [EventResponse(event).get_response() for event in self.events]