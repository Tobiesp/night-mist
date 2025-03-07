from typing import Optional
from pydantic import BaseModel, Field

from app.request_model.event_request import EventRequest
from app.request_model.point_request import PointRequest


class PointCategoryRequest(BaseModel):
    id: Optional[str] = Field(default=None)
    category_name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=1024)
    points: list[PointRequest] = Field(default=list)
    events: list[EventRequest] = Field(default=list)

    def __post_init__(self):
        if self.points and isinstance(self.points, list):
            self.points = [PointRequest(**point) for point in self.points if isinstance(point, dict)]
        if self.events and isinstance(self.events, list):
            self.events = [EventRequest(**event) for event in self.events if isinstance(event, dict)]
        if self.id:
            self.id = self.id.lower()
            if len(self.id) != 36:
                raise ValueError(f"Invalid id: {self.id}")