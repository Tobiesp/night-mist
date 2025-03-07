from typing import Optional
from pydantic import BaseModel, Field

from app.models.event_model import Interval
from app.request_model.point_category_request import PointCategoryRequest
from app.request_model.student_group_request import StudentGroupRequest


class EventRequest(BaseModel):
    id: Optional[str] = Field(default=None)
    event_name: str = Field(min_length=2, max_length=100)
    event_interval: Optional[Interval] = None
    student_groups: list[StudentGroupRequest] = Field(default=list)
    point_categories: list[PointCategoryRequest] = Field(default=list)

    def __post_init__(self):
        if self.event_interval and isinstance(self.event_interval, dict):
            self.event_interval = Interval(**self.event_interval)
        if self.student_groups and isinstance(self.student_groups, list):
            self.student_groups = [StudentGroupRequest(**group) for group in self.student_groups if isinstance(group, dict)]
        if self.point_categories and isinstance(self.point_categories, list):
            self.point_categories = [PointCategoryRequest(**category) for category in self.point_categories if isinstance(category, dict)]
        if self.id:
            self.id = self.id.lower()
            if len(self.id) != 36:
                raise ValueError(f"Invalid id: {self.id}")