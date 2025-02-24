from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(min_length=4, max_length=100, regex='^[a-zA-Z0-9_]*$')
    password: str = Field(min_length=8, max_length=30, regex='^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*])')