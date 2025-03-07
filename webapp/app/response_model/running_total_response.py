from typing import Optional

from app.models.point_model import RunningTotal


class RunningTotalResponse():
    
    def __init__(self, running_total: Optional[RunningTotal]):
        if running_total is not None:
            self.id = running_total.id
            self.student_id = running_total.student_id
            self.total_points = running_total.total_points

    def get_response(self) -> dict:
        return {
            'id': self.id,
            'student_id': self.student_id,
            'total_points': self.total_points,
        }
    

class RunningTotalListResponse():
    
    def __init__(self, running_totals: list[RunningTotal]):
        self.running_totals = running_totals

    def get_response(self) -> list[dict]:
        return [RunningTotalResponse(running_total).get_response() for running_total in self.running_totals]