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
        
    def _can_delete_check_(self, item: Grade):
        if item is None:
            return True
        if item.grade_name.lower() in ['none', 'graduated']:
            raise Exception('Cannot delete the grade: ' + item.grade_name)
        return super()._can_delete_check_(item)
    
    def _can_update_check_(self, instance: Grade):
        item = self._db_.get_by_id(instance.id)
        if item is not None and item.grade_value > 50 or item.grade_value < 0:
            raise Exception('Cannot update the grade. Grade value must be between 0 and 50: ' + item.grade_name)
        if item is None:
            return True
        if item.grade_name.lower() in ['none', 'graduated']:
            raise Exception('Cannot update the grade: ' + item.grade_name)
        return super()._can_update_check_(instance)




