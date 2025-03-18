from app.models.admin_model import Admin
from app.models.users_model import Priviledge, admin_permission
from app.request_model.admin_request import AdminRequest
from app.rest.generic_rest_api import GenericRestAPI


class PriviledgeRestAPI(GenericRestAPI[Priviledge]):
    def __init__(self):
        super().__init__(
            Priviledge,
            'priviledges',
            None,
            admin_permission,
            None,
            None,
            None)


class AdminRestAPI(GenericRestAPI[Admin]):
    def __init__(self):
        super().__init__(
            Admin,
            'admin',
            AdminRequest,
            admin_permission,
            admin_permission,
            admin_permission,
            admin_permission)