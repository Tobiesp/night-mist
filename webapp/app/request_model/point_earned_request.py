from typing import Optional
from pydantic import BaseModel, Field


class PointEarnedRequest(BaseModel):
    id: Optional[str] = Field(min_length=36, max_length=36)
    student: str = Field(min_length=36, max_length=36)
    eventInstance: str = Field(min_length=36, max_length=36)
    point: str = Field(min_length=36, max_length=36)

    def __post_init__(self):
        if self.id:
            self.id = self.id.lower()
            if len(self.id) != 36:
                raise ValueError(f"Invalid id: {self.id}")