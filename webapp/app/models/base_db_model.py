
from __future__ import annotations
import json
import uuid
from sqlalchemy import UUID, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class BaseDBModel:
    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=True, )  # Ensure default value
    
    def __init__(self, **data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def __repr__(self):
        return f'<{self.__class__.__name__} {self.id}>'
    
    def __eq__(self, other: BaseDBModel) -> bool:
        for key, value in self.__dict__.items():
            if key == 'id':
                continue
            if key == 'created_at' or key == 'updated_at':
                continue
            if key not in other.__dict__:
                return False
            if value != getattr(other, key):
                return False
        return True
        
    def restricted_fields(self) -> list:
        return []
    
    @staticmethod
    def query_fields(self) -> list[dict[str, any]]:
        return []
    
    def to_json(self) -> str:
        return json.dumps(self.to_response())
    
    def to_response(self) -> dict:
        d = self.__dict__
        for field in self.restricted_fields():
            if field in d:
                del d[field]
        allowed_keys = []
        for key in d.keys():
            if not key.startswith('_'):
                allowed_keys.append(key)
        d = {key: d[key] for key in allowed_keys}
        for key, value in d.items():
            if isinstance(value, BaseDBModel):
                d[key] = value.to_response()
            elif isinstance(value, list):
                if len(value) > 0 and isinstance(value[0], BaseDBModel):
                    d[key] = [v.to_response() for v in value]
        return d
    
    def from_json(self, data: str) -> BaseDBModel:
        json_data = json.loads(data)
        if isinstance(json_data, dict):
            for key, value in json_data.items():
                setattr(self, key, value)
            return self
        else:
            raise ValueError('Invalid JSON data')