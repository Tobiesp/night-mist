from typing import Optional

from app.models.students_model import Grade


class GradeResponse():

    def __init__(self, grade: Optional[Grade]):
        self._grade_ = None
        if grade is not None:
            self._grade_ = grade

    def get_response(self) -> dict | None:
        if self._grade_ is None:
            return None
        return {
            'id': self._grade_.id,
            'grade_name': self._grade_.grade_name,
        }
    

class GradeListResponse():

    def __init__(self, grades: list[Grade]):
        self.grades = grades

    def get_response(self) -> list[dict]:
        return [GradeResponse(grade).get_response() for grade in self.grades]