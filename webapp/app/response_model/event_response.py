from typing import Optional

from flask import Response, jsonify

from app.models.event_model import Event
from app.response_model.point_category_response import PointCategoryListResponse
from app.response_model.student_group_response import StudentGroupListResponse


class EventResponse():
    
    def __init__(self, event: Optional[Event]):
        self._event_ = None
        if event is not None:
            self._event_ = event

    def get_dict(self) -> dict | None:
        if self._event_ is None:
            return None
        return {
            'id': self._event_.id,
            'event_name': self._event_.event_name,
            'event_interval': self._event_.interval.to_dict(),
            'student_groups': StudentGroupListResponse(self._event_.student_groups).get_dict(),
            'point_categories': PointCategoryListResponse(self._event_.point_categories).get_dict(),
        }

    def get_response(self) -> Response:
        d = self.get_dict()
        if d is None:
            return Response(status=404)
        return jsonify(d)
    

class EventListResponse():
    
    def __init__(self, events: list[Event]):
        self.events = events

    def get_response(self) -> Response:
        return jsonify([EventResponse(event).get_dict() for event in self.events if event is not None])