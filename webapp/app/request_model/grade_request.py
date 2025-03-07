from typing import Optional
from pydantic import BaseModel, Field


class GradeRequest(BaseModel):
    id: Optional[str] = Field(default=None)
    grade_name: str = Field(min_length=1, max_length=30)

    def __post_init__(self):
        if self.id:
            self.id = self.id.lower()
            if len(self.id) != 36:
                raise ValueError(f"Invalid id: {self.id}")