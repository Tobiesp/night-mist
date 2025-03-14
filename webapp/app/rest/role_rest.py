from app.models.users_model import Role, admin_permission
from app.request_model.role_request import RoleRequest
from app.rest.generic_rest_api import GenericRestAPI


class RoleRestAPI(GenericRestAPI[Role]):

    def __init__(self):
        super().__init__(
            Role,
            'roles',
            RoleRequest,
            admin_permission,
            admin_permission,
            admin_permission,
            admin_permission)
