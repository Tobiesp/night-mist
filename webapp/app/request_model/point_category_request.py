from typing import Optional
from pydantic import BaseModel, Field


class PointCategoryRequest(BaseModel):
    id: Optional[str] = Field(default=None)
    category_name: str = Field(min_length=2, max_length=100)
    description: str = Field(min_length=2, max_length=1024)

    def __post_init__(self):
        if self.id:
            self.id = self.id.lower()
            if len(self.id) != 36:
                raise ValueError(f"Invalid id: {self.id}")