from typing import Optional

from app.models.point_model import PointSpent


class PointSpentResponse():

    def __init__(self, point_earned: Optional[PointSpent]):
        if point_earned is not None:
            self.id = point_earned.id
            self.student_id = point_earned.student_id
            self.event_instance_id = point_earned.event_instance_id
            self.point_id = point_earned.point_id

    def get_response(self) -> dict:
        return {
            'id': self.id,
            'student_id': self.student_id,
            'event_instance_id': self.event_instance_id,
            'point_id': self.point_id,
        }
    

class PointSpentListResponse():

    def __init__(self, points_earned: list[PointSpent]):
        self.points_earned = points_earned

    def get_response(self) -> list[dict]:
        return [PointSpentResponse(point_earned).get_response() for point_earned in self.points_earned]