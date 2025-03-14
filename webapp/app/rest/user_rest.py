from flask import Response
from flask_login import login_required
from app.models.users_model import User, admin_permission
from app.repositories import database_repository
from app.request_model.user_request import UserRequest
from app.rest.generic_rest_api import GenericRestAPI


class UserRestAPI(GenericRestAPI[User]):
    def __init__(self):
        super().__init__(
            User, 
            'users', 
            UserRequest, 
            admin_permission, 
            admin_permission, 
            admin_permission, 
            admin_permission)
        self.blueprint.add_url_rule('/<string:id>/lock', view_func=self.lock_user, methods=['POST'])
        self.blueprint.add_url_rule('/<string:id>/unlock', view_func=self.unlock_user, methods=['POST'])

    @login_required
    def lock_user(user_id: str):
        with admin_permission.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_admin_db_repository()
            user = database.get_user_by_id(user_id)
            if user is None:
                return Response(status=404)
            if user.role.role_name == 'admin':
                role_users = database.get_users_by_role('admin')
                if len(role_users) == 1:
                    return Response(status=400, response='Cannot lock the only admin user')
                else:
                    accounts_locked_count = sum([1 for user in role_users if user.is_active is False])
                    if accounts_locked_count == len(role_users) - 1:
                        return Response(status=400, response='Cannot lock the last active admin user')
            user.is_active = False
            database.update_user(user)
            return Response(status=200)

    @login_required
    def unlock_user(user_id: str):
        with admin_permission.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_admin_db_repository()
            user = database.get_user_by_id(user_id)
            if user is None:
                return Response(status=404)
            user.is_active = True
            database.update_user(user)
            return Response(status=200)
    