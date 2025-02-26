from pydantic import BaseModel, Field


class ForgotPasswordRequest(BaseModel):
    email: str = Field(min_length=6, max_length=100, pattern=r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    username: str = Field(min_length=4, max_length=100, pattern=r'^[a-zA-Z0-9_]*$')