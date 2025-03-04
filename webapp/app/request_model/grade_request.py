from pydantic import BaseModel, Field


class GradeRequest(BaseModel):
    grade_name: str = Field(min_length=1, max_length=30)