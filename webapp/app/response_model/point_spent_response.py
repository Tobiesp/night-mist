from typing import Optional

from app.models.point_model import PointSpent


class PointSpentResponse():

    def __init__(self, point_spent: Optional[PointSpent]):
        if point_spent is not None:
            self.id = point_spent.id
            self.student_id = point_spent.student_id
            self.event_instance_id = point_spent.event_instance_id
            self.points = point_spent.points

    def get_response(self) -> dict:
        return {
            'id': self.id,
            'student_id': self.student_id,
            'event_instance_id': self.event_instance_id,
            'points': self.points,
        }
    

class PointSpentListResponse():

    def __init__(self, points_spent: list[PointSpent]):
        self.points_spent = points_spent

    def get_response(self) -> list[dict]:
        return [PointSpentResponse(point_spent).get_response() for point_spent in self.points_spent]