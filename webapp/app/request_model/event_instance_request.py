from typing import Optional
from pydantic import BaseModel, Field

from app.request_model.event_request import EventRequest


class EventInstanceRequest(BaseModel):
    id: Optional[str] = Field(default=None)
    event: Optional[EventRequest] = Field(default=None)
    event_date: Optional[str] = Field(default=None)

    def __post_init__(self):
        if self.event and isinstance(self.event, dict):
            self.event = EventRequest(**self.event)
        if self.id:
            self.id = self.id.lower()
            if len(self.id) != 36:
                raise ValueError("Invalid id")