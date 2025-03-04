from typing import Optional
from pydantic import BaseModel, Field

from app.request_model.grade_request import GradeRequest
from app.request_model.student_group_request import StudentGroupRequest


class StudentRequest(BaseModel):
    firstname: str = Field(min_length=2, max_length=100)
    lastname: str = Field(min_length=2, max_length=100)
    student_group: Optional[StudentGroupRequest] = None
    grade: Optional[GradeRequest] = None

    def __post_init__(self):
        if self.grade and isinstance(self.grade, dict):
            self.grade = GradeRequest(**self.grade)
        if self.student_group and isinstance(self.student_group, dict):
            self.student_group = StudentGroupRequest(**self.student_group)