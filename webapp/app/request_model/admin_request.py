from pydantic import BaseModel, Field


class AdminRequest(BaseModel):
    key: str = Field(min_length=8, max_length=30)
    value: str = Field()
    value_type: str = Field(min_length=3, max_length=30)

    def __post_init__(self):
        if self.value_type not in ['string', 'dict', 'list', 'bool', 'int', 'secret']:  
            raise ValueError('Invalid value type. Must be one of: string, dict, list, bool, int, secret')