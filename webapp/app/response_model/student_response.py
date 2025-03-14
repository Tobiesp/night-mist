from typing import Optional

from flask import Response, jsonify

from app.models.students_model import Student
from app.response_model.grade_response import GradeResponse
from app.response_model.student_group_response import StudentGroupResponse


class StudentResponse():

    def __init__(self, student: Optional[Student]):
        self._student_ = None
        if student is not None:
            self._student_ = student

    def get_dict(self) -> dict | None:
        if self._student_ is None:
            return None
        return {
            'id': self._student_.id,
            'firstname': self._student_.firstname,
            'lastname': self._student_.lastname,
            'student_name': self._student_.student_name,
            'grade': GradeResponse(self._student_.grade).get_dict(),
            'student_group': StudentGroupResponse(self._student_.student_group).get_dict(),
        }

    def get_response(self) -> Response:
        d = self.get_dict()
        if d is None:
            return Response(status=404)
        return jsonify(d)
    

class StudentListResponse():

    def __init__(self, students: list[Student]):
        self.students = students

    def get_response(self) -> Response:
        return jsonify([StudentResponse(student).get_dict() for student in self.students if student is not None])