from typing import Optional

from flask import Response, jsonify

from app.models.point_model import PointEarned


class PointEarnedResponse():

    def __init__(self, point_earned: Optional[PointEarned]):
        self._point_earned = None
        if point_earned is not None:
            self._point_earned = point_earned

    def get_dict(self) -> dict | None:
        if self._point_earned is None:
            return None
        return {
            'id': self._point_earned.id,
            'student_id': self._point_earned.student_id,
            'event_instance_id': self._point_earned.event_instance_id,
            'point_id': self._point_earned.point_id,
        }

    def get_response(self) -> Response:
        d = self.get_dict()
        if d is None:
            return Response(status=404)
        return jsonify(d)
    

class PointEarnedListResponse():

    def __init__(self, points_earned: list[PointEarned]):
        self.points_earned = points_earned

    def get_response(self) -> Response:
        return jsonify([PointEarnedResponse(point_earned).get_dict() for point_earned in self.points_earned if point_earned is not None])