from typing import Optional

from flask import Response, jsonify

from app.models.event_model import Point
from app.response_model.point_category_response import PointCategoryResponse
from app.response_model.student_group_response import StudentGroupResponse


class PointResponse():
    
    def __init__(self, point: Optional[Point]):
        self._point_ = None
        if point is not None:
            self._point_ = point

    def get_dict(self) -> dict | None:
        if self._point_ is None:
            return None
        return {
            'id': self._point_.id,
            'points': self._point_.points,
            'student_group': StudentGroupResponse(self._point_.student_group).get_dict(),
            'point_category': PointCategoryResponse(self._point_.point_category).get_dict(),
            'points_interval': self._point_.interval.to_dict(),
        }

    def get_response(self) -> Response:
        d = self.get_dict()
        if d is None:
            return Response(status=404)
        return jsonify(d)
    

class PointListResponse():
    
    def __init__(self, points: list[Point]):
        self.points = points

    def get_response(self) -> Response:
        return jsonify([PointResponse(point).get_dict() for point in self.points if point is not None])