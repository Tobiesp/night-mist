from flask import Response
from flask_login import login_required
from app.models.users_model import Role, User, admin_permission
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

    def _can_delete_check_(self, item_id: str):
        item = self._db_.get_by_id(item_id)
        if item is None:
            return True
        role_db = database_repository.DatabaseRepository.instance().get_model_db_repository(Role)
        admin_role = role_db.get_role_by_name('admin')
        if item.role == admin_role:
            admin_users = self._db_.get_by(role=admin_role)
            if len(admin_users) == 1:
                raise Exception('Cannot delete the only admin user')
            active_admin_users = [user for user in admin_users if user.is_active]
            if len(active_admin_users) == 1:
                raise Exception('Cannot delete the only admin user')
        return super()._can_delete_check_(item_id)
    
    def _can_update_check_(self, instance: any):
        # TODO: Add check to prevent only admin user from being updated to non-admin
        return super()._can_update_check_(instance)

    @login_required
    def lock_user(user_id: str):
        with admin_permission.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(User)
            user: User | None = database.get_by_id(user_id)
            if user is None:
                return Response(status=404)
            if user.role.role_name == 'admin':
                role_db = database_repository.DatabaseRepository.instance().get_model_db_repository(Role)
                admin_role = role_db.get_by(role_name='admin')
                role_users: list[User] = database.get_by(role=admin_role)
                if len(role_users) == 1:
                    return Response(status=400, response='Cannot lock the only admin user')
                else:
                    accounts_locked_count = sum([1 for user in role_users if user.is_active is False])
                    if accounts_locked_count == len(role_users) - 1:
                        return Response(status=400, response='Cannot lock the last active admin user')
            user.is_active = False
            database.update(user.id, **user.__dict__)
            return Response(status=200)

    @login_required
    def unlock_user(user_id: str):
        with admin_permission.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(User)
            user: User = database.get_by_id(user_id)
            if user is None:
                return Response(status=404)
            user.is_active = True
            database.update(user.id, **user.__dict__)
            return Response(status=200)
    