from typing import Optional

from flask import Response, jsonify

from app.models.point_model import PointSpent


class PointSpentResponse():

    def __init__(self, point_spent: Optional[PointSpent]):
        self._point_spent_ = None
        if point_spent is not None:
            self._point_spent_ = point_spent

    def get_dict(self) -> dict | None:
        if self._point_spent_ is None:
            return None
        return {
            'id': self._point_spent_.id,
            'student_id': self._point_spent_.student_id,
            'event_instance_id': self._point_spent_.event_instance_id,
            'points': self._point_spent_.points,
        }

    def get_response(self) -> Response:
        d = self.get_dict()
        if d is None:
            return Response(status=404)
        return jsonify(d)
    

class PointSpentListResponse():

    def __init__(self, points_spent: list[PointSpent]):
        self.points_spent = points_spent

    def get_response(self) -> Response:
        return jsonify([PointSpentResponse(point_spent).get_dict() for point_spent in self.points_spent if point_spent is not None])