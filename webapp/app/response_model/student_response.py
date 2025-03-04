from typing import Optional

from app.models.students_model import Student
from app.response_model.grade_response import GradeResponse
from app.response_model.student_group_response import StudentGroupResponse


class StudentResponse():

    def __init__(self, student: Optional[Student]):
        self._student_ = None
        if student is not None:
            self._student_ = student

    def get_response(self) -> dict | None:
        if self._student_ is None:
            return None
        return {
            'id': self._student_.id,
            'firstname': self._student_.firstname,
            'lastname': self._student_.lastname,
            'student_name': self._student_.student_name,
            'grade': GradeResponse(self._student_.grade).get_response(),
            'student_group': StudentGroupResponse(self._student_.student_group).get_response(),
        }
    

class StudentListResponse():

    def __init__(self, students: list[Student]):
        self.students = students

    def get_response(self) -> list[dict]:
        return [StudentResponse(student).get_response() for student in self.students]