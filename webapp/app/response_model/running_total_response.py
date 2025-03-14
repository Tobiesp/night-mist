from typing import Optional

from flask import Response, jsonify

from app.models.point_model import RunningTotal


class RunningTotalResponse():
    
    def __init__(self, running_total: Optional[RunningTotal]):
        self._running_total = None
        if running_total is not None:
            self._running_total = running_total

    def get_dict(self) -> dict | None:
        if self._running_total is None:
            return None
        return {
            'id': self._running_total.id,
            'student_id': self._running_total.student_id,
            'total_points': self._running_total.total_points,
        }

    def get_response(self) -> Response:
        d = self.get_dict()
        if d is None:
            return Response(status=404)
        return jsonify(d)
    

class RunningTotalListResponse():
    
    def __init__(self, running_totals: list[RunningTotal]):
        self.running_totals = running_totals

    def get_response(self) -> Response:
        return jsonify([RunningTotalResponse(running_total).get_dict() for running_total in self.running_totals if running_total is not None])