from typing import Optional

from flask import Response, jsonify

from app.models.students_model import Grade


class GradeResponse():

    def __init__(self, grade: Optional[Grade]):
        self._grade_ = None
        if grade is not None:
            self._grade_ = grade

    def get_dict(self) -> dict | None:
        if self._grade_ is None:
            return None
        return {
            'id': self._grade_.id,
            'grade_name': self._grade_.grade_name,
        }

    def get_response(self) -> Response:
        d = self.get_dict()
        if d is None:
            return Response(status=404)
        return jsonify(d)
    

class GradeListResponse():

    def __init__(self, grades: list[Grade]):
        self.grades = grades

    def get_response(self) -> Response:
        return jsonify([GradeResponse(grade).get_dict() for grade in self.grades if grade is not None])