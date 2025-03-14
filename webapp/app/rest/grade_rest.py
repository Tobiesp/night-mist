from app.models.students_model import Grade
from app.models.users_model import student_read_permission, admin_permission
from app.request_model.grade_request import GradeRequest
from app.rest.generic_rest_api import GenericRestAPI


class GradeRestAPI(GenericRestAPI[Grade]):
    def __init__(self):
        super().__init__(
            Grade,
            'grades',
            GradeRequest,
            student_read_permission,
            admin_permission,
            admin_permission,
            admin_permission)




