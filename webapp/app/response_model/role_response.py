from typing import Optional

from flask import Response, jsonify

from app.models.users_model import Role
from app.response_model.priviledge_response import PriviledgeResponse


class RoleResponse():

    def __init__(self, role: Optional[Role]):
        self._role_ = None
        if role is not None:
            self._role_ = role

    def get_dict(self) -> dict | None:
        if self._role_ is None:
            return None
        return {
            'id': self._role_.id,
            'role': self._role_.role_name,
            'priviledges': [PriviledgeResponse(priviledge).get_dict() for priviledge in self._role_.priviledges],
        }

    def get_response(self) -> Response:
        d = self.get_dict()
        if d is None:
            return Response(status=404)
        return jsonify(d)
    

class RoleListResponse():

    def __init__(self, roles: list[Role]):
        self.roles = roles

    def get_response(self) -> Response:
        return jsonify([RoleResponse(role).get_dict() for role in self.roles if role is not None])