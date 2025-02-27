from pydantic import BaseModel, Field


class PrivilegeRequest(BaseModel):
    name: str = Field(min_length=4, max_length=100)
    id: str = Field(min_length=4, max_length=100)



class RoleRequest(BaseModel):
    name: str = Field(min_length=4, max_length=100)
    priviledges: list[PrivilegeRequest] = Field(default_factory=list)

    def __post_init__(self):
        self.priviledges = [PrivilegeRequest(**privilege) for privilege in self.priviledges]