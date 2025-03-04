from pydantic import BaseModel, Field

from app.request_model.grade_request import GradeRequest


class StudentGroupRequest(BaseModel):
    group_name: str = Field(min_length=1, max_length=100)
    grades: list[GradeRequest] = Field(min_items=1, default_factory=list)

    def __post_init__(self):
        self.grades = [GradeRequest(**grade) for grade in self.grades if grade and isinstance(grade, dict)]