from typing import Optional

from app.models.users_model import Role


class RoleResponse():

    def __init__(self, role: Optional[Role]):
        if role is not None:
            self.id = role.id
            self.name = role.role_name

    def get_response(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }
    

class RoleListResponse():

    def __init__(self, roles: list[Role]):
        self.roles = roles

    def get_response(self) -> list[dict]:
        return [RoleResponse(role).get_response() for role in self.roles]