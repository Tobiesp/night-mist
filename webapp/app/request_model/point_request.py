from typing import Optional
from pydantic import BaseModel, Field

from app.models.event_model import Interval
from app.request_model.point_category_request import PointCategoryRequest
from app.request_model.student_group_request import StudentGroupRequest


class PointRequest(BaseModel):
    id: Optional[str] = Field(default=None)
    points: int = Field(ge=-1)
    student_group: Optional[StudentGroupRequest] = None
    point_category: Optional[PointCategoryRequest] = None
    points_interval: Optional[Interval] = None

    def __post_init__(self):
        if self.student_group and isinstance(self.student_group, dict):
            self.student_group = StudentGroupRequest(**self.student_group)
        if self.point_category and isinstance(self.point_category, dict):
            self.point_category = PointCategoryRequest(**self.point_category)
        if self.points_interval and isinstance(self.points_interval, dict):
            self.points_interval = Interval(**self.points_interval)
        if self.id:
            self.id = self.id.lower()
            if len(self.id) != 36:
                raise ValueError(f"Invalid id: {self.id}")
