from typing import Optional

from flask import Response, jsonify

from app.models.users_model import User
from app.response_model.role_response import RoleResponse


class UserResponse():

    def __init__(self, user: Optional[User]):
        self._user_ = None
        if user is not None:
            self._user_ = user

    def get_response(self) -> Response:
        d = self.get_dict()
        if d is None:
            return Response(status=404)
        return jsonify(d)
    
    def get_dict(self) -> dict | None:
        if self._user_ is None:
            return None
        return {
            'id': str(self._user_.id),
            'username': self._user_.username,
            'firstname': self._user_.firstname,
            'lastname': self._user_.lastname,
            'email': self._user_.email,
            'role': RoleResponse(self._user_.role).get_dict(),
            'account_locked': self._user_.account_locked,
            'last_login': self._user_.last_login,
            'login_attempts': self._user_.login_attempts,
        }
    

class UserListResponse():

    def __init__(self, users: list[User]):
        self.users = users

    def get_response(self) -> Response:
        return jsonify([UserResponse(user).get_dict() for user in self.users if user is not None])