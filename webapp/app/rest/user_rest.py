from flask import Response, request
from flask_login import current_user, login_required
from app.models.users_model import Role, User, admin_permission
from app.repositories import database_repository
from app.request_model.change_password_request import ChangePasswordRequest
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
        self.blueprint.add_url_rule('/change_password', view_func=self.change_password, methods=['POST'])

    def _can_delete_check_(self, item: User):
        if item is None:
            return True
        role_db = database_repository.DatabaseRepository.instance().get_model_db_repository(Role)
        admin_role = role_db.get_by_and(role_name='admin')
        if item.role == admin_role:
            admin_users = self._db_.get_by_and(role=admin_role)
            if len(admin_users) == 1:
                raise Exception('Cannot delete the only admin user')
            active_admin_users = [user for user in admin_users if user.is_active]
            if len(active_admin_users) == 1:
                raise Exception('Cannot delete the only admin user')
        return super()._can_delete_check_(item)
    
    def _can_update_check_(self, instance: User):
        admins = self._db_.get_by_and(role=instance.role)
        if len(admins) == 1:
            raise Exception('Cannot update the only admin user')
        admins = [admin for admin in admins if admin.is_active]
        if len(admins) == 1:
            raise Exception('Cannot update the only active admin user')
        return super()._can_update_check_(instance)

    @login_required
    def lock_user(self, id: str):
        print(f"lock_user: {id}")
        with admin_permission.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(User)
            user: User | None = database.get_by_id(id)
            if user is None:
                return Response(status=404)
            print(f"role: {user.role.role_name}")
            if user.role.role_name == 'admin':
                role_db = database_repository.DatabaseRepository.instance().get_model_db_repository(Role)
                admin_role = role_db.get_by_and_first(role_name='admin')
                role_users: list[User] = database.get_by_and(role=admin_role)
                print(f"admin user count: {len(role_users)}")
                if len(role_users) == 1:
                    return Response(status=400, response='Cannot lock the only admin user')
                else:
                    accounts_locked_count = sum([1 for user in role_users if user.is_active is False])
                    print(f"accounts_locked_count: {accounts_locked_count}")
                    if accounts_locked_count == len(role_users) - 1:
                        return Response(status=400, response='Cannot lock the last active admin user')
            user.is_active = False
            user_dict = user.__dict__
            if 'id' in user_dict:
                del user_dict['id']
            database.update(user.id, **user_dict)
            return Response(status=200)

    @login_required
    def unlock_user(self, id: str):
        with admin_permission.require(http_exception=403):
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(User)
            user: User = database.get_by_id(id)
            if user is None:
                return Response(status=404)
            user.is_active = True
            user_dict = user.__dict__
            if 'id' in user_dict:
                del user_dict['id']
            database.update(user.id, **user_dict)
            return Response(status=200)
        
    @login_required
    def change_password(self):
        user: User = current_user
        try:
            request_args = ChangePasswordRequest(request.args)
        except TypeError:
            return Response(status=400, response='Invalid request type')
        except ValueError as ve:
            return Response(status=400, response=str(ve))
        
        if user.check_password(request_args.password):
            user.set_password(request_args.new_password)
            database = database_repository.DatabaseRepository.instance().get_model_db_repository(User)
            user_dict = user.__dict__
            if 'id' in user_dict:
                del user_dict['id']
            database.update(user.id, **user_dict)
            return Response(status=200)
        else:
            return Response(status=400, response='Invalid password')
        
    