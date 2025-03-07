from typing import Optional
from pydantic import Field
from app.request_model.role_request import RoleRequest
from app.request_model.signup_request import SignupRequest


class UserRequest(SignupRequest):
    id: Optional[str] = Field(default=None)
    role: Optional[RoleRequest] = None

    def __post_init__(self):
        if self.role and isinstance(self.role, dict):
            self.role = RoleRequest(**self.role)
        if self.id:
            self.id = self.id.lower()
            if len(self.id) != 36:
                raise ValueError(f"Invalid id: {self.id}")
    