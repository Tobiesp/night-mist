from app.models.students_model import StudentGroup
from app.models.users_model import student_read_permission, admin_permission
from app.request_model.student_group_request import StudentGroupRequest
from app.rest.generic_rest_api import GenericRestAPI


class GroupRestAPI(GenericRestAPI[StudentGroup]):
    def __init__(self):
        super().__init__(
            StudentGroup,
            'student_groups',
            StudentGroupRequest,
            student_read_permission,
            admin_permission,
            admin_permission,
            admin_permission)
