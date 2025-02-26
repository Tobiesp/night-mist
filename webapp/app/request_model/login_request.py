from pydantic import BaseModel, Field, field_validator

class LoginRequest(BaseModel):
    username: str = Field(min_length=4, max_length=100, pattern='^[a-zA-Z0-9_]*$')
    password: str = Field(min_length=8, max_length=30)

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        if not any(char in '!@#$%^&*' for char in value):
            raise ValueError('Password must contain at least one special character')
        return value