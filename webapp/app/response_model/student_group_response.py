from typing import Optional

from app.models.students_model import StudentGroup
from app.response_model.grade_response import GradeResponse


class StudentGroupResponse():

    def __init__(self, student_group: Optional[StudentGroup]):
        self._student_group_ = None
        if student_group is not None:
            self._student_group_ = student_group

    def get_response(self) -> dict | None:
        if self._student_group_ is None:
            return None
        return {
            'id': self._student_group_.id,
            'group_name': self._student_group_.group_name,
            'grades': [GradeResponse(grade) for grade in self._student_group_.grades],
        }
    

class StudentGroupListResponse():

    def __init__(self, student_groups: list[StudentGroup]):
        self.student_groups = student_groups

    def get_response(self) -> list[dict]:
        return [StudentGroupResponse(student_group).get_response() for student_group in self.student_groups]