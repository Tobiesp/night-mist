from typing import Optional

from app.models.users_model import User
from app.response_model.role_response import RoleResponse


class UserResponse():

    def __init__(self, user: Optional[User]):
        self._user_ = None
        if user is not None:
            self._user_ = user

    def get_response(self) -> dict | None:
        if self._user_ is None:
            return None
        return {
            'id': self._user_.id,
            'username': self._user_.username,
            'firstname': self._user_.firstname,
            'lastname': self._user_.lastname,
            'email': self._user_.email,
            'role': RoleResponse(self._user_.role).get_response(),
            'account_locked': self._user_.account_locked,
            'last_login': self._user_.last_login,
            'login_attempts': self._user_.login_attempts,
        }
    

class UserListResponse():

    def __init__(self, users: list[User]):
        self.users = users

    def get_response(self) -> list[dict]:
        return [UserResponse(user).get_response() for user in self.users]