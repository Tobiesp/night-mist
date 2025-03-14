from typing import Optional

from flask import Response, jsonify

from app.models.students_model import StudentGroup
from app.response_model.grade_response import GradeResponse


class StudentGroupResponse():

    def __init__(self, student_group: Optional[StudentGroup]):
        self._student_group_ = None
        if student_group is not None:
            self._student_group_ = student_group

    def get_dict(self) -> dict | None:
        if self._student_group_ is None:
            return None
        return {
            'id': self._student_group_.id,
            'group_name': self._student_group_.group_name,
            'grades': [GradeResponse(grade).get_dict() for grade in self._student_group_.grades],
        }

    def get_response(self) -> Response:
        d = self.get_dict()
        if d is None:
            return Response(status=404)
        return jsonify(d)
        

class StudentGroupListResponse():

    def __init__(self, student_groups: list[StudentGroup]):
        self.student_groups = student_groups

    def get_response(self) -> Response:
        return jsonify([StudentGroupResponse(student_group).get_dict() for student_group in self.student_groups if student_group is not None])