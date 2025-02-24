from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    username: str = Field(min_length=4, max_length=100, regex='^[a-zA-Z0-9_]*$')
    password: str = Field(min_length=8, max_length=30, regex='^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*])')
    repeat_password: str = Field(min_length=8, max_length=30, regex='^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[!@#$%^&*])')
    email: str = Field(min_length=6, max_length=100, regex='^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    full_name: str = Field(min_length=2, max_length=200)