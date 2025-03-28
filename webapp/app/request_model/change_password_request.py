from pydantic import BaseModel, Field, field_validator


class ChangePasswordRequest(BaseModel):
    password: str = Field(min_length=8, max_length=30)
    new_password: str = Field(min_length=8, max_length=30)
    repeat_password: str = Field(min_length=8, max_length=30)

    @field_validator('new_password')
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

    @field_validator('repeat_password')
    def validate_repeat_password(cls, value: str) -> str:
        if not any(char.isupper() for char in value):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(char.islower() for char in value):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one digit')
        if not any(char in '!@#$%^&*' for char in value):
            raise ValueError('Password must contain at least one special character')
        if value != cls.password:
            raise ValueError('Passwords do not match')
        return value