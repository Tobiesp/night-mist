from typing import Optional
from pydantic import BaseModel, Field


class PrivilegeRequest(BaseModel):
    name: str = Field(min_length=4, max_length=100)
    id: str = Field(min_length=36, max_length=36)



class RoleRequest(BaseModel):
    id: Optional[str] = Field(default=None)
    name: str = Field(min_length=4, max_length=100)
    priviledges: list[PrivilegeRequest] = Field(default_factory=list)

    def __post_init__(self):
        self.priviledges = [PrivilegeRequest(**privilege) for privilege in self.priviledges]
        if self.id:
            self.id = self.id.lower()
            if len(self.id) != 36:
                raise ValueError("Invalid id")