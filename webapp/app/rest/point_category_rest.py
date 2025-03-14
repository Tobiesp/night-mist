from app.models.event_model import PointCategory
from app.models.users_model import event_read_permission, event_write_permission, admin_permission
from app.request_model.point_category_request import PointCategoryRequest
from app.rest.generic_rest_api import GenericRestAPI


class PointCategoryRestAPI(GenericRestAPI[PointCategory]):
    def __init__(self):
        super().__init__(
            PointCategory,
            'point_categories',
            PointCategoryRequest,
            event_read_permission,
            event_write_permission,
            event_write_permission,
            admin_permission)