from flask_login import login_required
from app.models.students_model import Student
from app.models.users_model import student_read_permission, student_write_permission, admin_permission
from app.repositories import database_repository
from app.request_model.student_request import StudentRequest
from app.rest.generic_rest_api import GenericRestAPI


class StudentRestAPI(GenericRestAPI[Student]):
    def __init__(self):
        super().__init__(
            Student,
            'students',
            StudentRequest,
            student_read_permission,
            student_write_permission,
            student_write_permission,
            admin_permission)
        self.blueprint.add_url_rule('/group/<string:group_id>', view_func=self.get_students_by_group, methods=['GET'])
        self.blueprint.add_url_rule('/grade/<string:grade_id>', view_func=self.get_students_by_grade, methods=['GET'])
        
    @login_required
    def get_students_by_group(group_id: str):
        with student_read_permission.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_student_db_repository()
            students = database.get_students_by_group_id(group_id)
            students = [student.to_dict() for student in students]
            return students

    @login_required
    def get_students_by_grade(grade_id: str):
        with student_read_permission.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_student_db_repository()
            students = database.get_students_by_grade_id(grade_id)
            students = [student.to_dict() for student in students]
            return students