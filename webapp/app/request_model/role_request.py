from dataclasses import field
from pydantic import BaseModel


class PrivilegeRequest(BaseModel):
    name: str = field(min_length=4, max_length=100)
    id: str = field(min_length=4, max_length=100)



class RoleRequest(BaseModel):
    name: str = field(min_length=4, max_length=100)
    priviledges: list[PrivilegeRequest] = field(default_factory=list)

    def __post_init__(self):
        self.priviledges = [PrivilegeRequest(**privilege) for privilege in self.priviledges]