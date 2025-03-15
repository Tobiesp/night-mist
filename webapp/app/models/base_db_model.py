
from __future__ import annotations
import datetime
import json
import uuid
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import UUID, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class Interval(BaseModel):
    repeat: str = Field(min_length=4, max_length=7, default='none')
    month_day: int = Field(ge=0, le=30, default=0)
    week_day: int = Field(ge=0, le=7, default=0)
    hour: int = Field(ge=0, le=23, default=0)
    minute: int = Field(ge=0, le=59, default=0)

    @field_validator('repeat')
    def validate_repeat(cls, value: str) -> str:
        test_value = value.lower() if value else ''
        if test_value not in ['daily', 'weekly', 'monthly', 'none']:
            raise ValueError('Repeat value must be either daily, weekly, or monthly')
        return value
    
    def to_json(self) -> str:
        data = {
            'repeat': self.repeat,
        }
        if self.repeat == 'monthly':
            data['month_day'] = self.month_day
        elif self.repeat == 'weekly':
            data['week_day'] = self.week_day
        if self.repeat in ['monthly', 'weekly', 'daily']:
            data['hour'] = self.hour
            data['minute'] = self.minute
            return json.dumps(data)
        
    def to_response(self) -> dict:
        data = {
            'repeat': self.repeat,
        }
        if self.repeat == 'monthly':
            data['month_day'] = self.month_day
        elif self.repeat == 'weekly':
            data['week_day'] = self.week_day
        if self.repeat in ['monthly', 'weekly', 'daily']:
            data['hour'] = self.hour
            data['minute'] = self.minute
            return data
    
    def from_json(self, data: str) -> Interval:
        json_data = json.loads(data)
        if isinstance(json_data, dict):
            self.repeat = json_data.get('repeat', 'none')
            self.month_day = json_data.get('month_day', 0)
            self.week_day = json_data.get('week_day', 0)
            self.hour = json_data.get('hour', 0)
            self.minute = json_data.get('minute', 0)
            return self
        else:
            raise ValueError('Invalid JSON data')
        
    def get_next_date(self, check_date: datetime) -> datetime:
        current_date: datetime = datetime.datetime.now()
        if self.repeat == 'none':
            return current_date
        if check_date >= current_date:
            return check_date
        elif self.repeat == 'daily':
            date = current_date.date()
            date = date + datetime.timedelta(days=1)
            return datetime.datetime.combine(date, datetime.time(self.hour, self.minute))
        elif self.repeat == 'weekly':
            # Get the next week day
            if self.week_day == 0:
                raise ValueError(f'Invalid week day: {self.week_day}')
            weekday = current_date.weekday() + 1
            expected_weekday = self.week_day
            diff_weekday = expected_weekday - weekday if expected_weekday > weekday else 7 - weekday + expected_weekday
            date = current_date.date() + datetime.timedelta(days=diff_weekday)
            return datetime.datetime.combine(date, datetime.time(self.hour, self.minute))
        elif self.repeat == 'monthly':
            if self.month_day == 0:
                raise ValueError(f'Invalid month day: {self.month_day}')
            month_day = current_date.day
            expected_month_day = self.month_day
            diff_month_day = expected_month_day - month_day if expected_month_day > month_day else 30 - month_day + expected_month_day
            date = current_date.date() + datetime.timedelta(days=diff_month_day)
            # Check month day is valid
            while date.day < expected_month_day:
                date = date + datetime.timedelta(days=1)
            while date.day > expected_month_day:
                date = date - datetime.timedelta(days=1)
            return datetime.datetime.combine(date, datetime.time(self.hour, self.minute))
        else:
            raise ValueError(f'Invalid repeat value: {self.repeat}')
        
    def is_event_passed(self, check_date: datetime) -> bool:
        return check_date < datetime.datetime.now()
        
    def __repr__(self):
        return f'<Interval: {self.repeat}>'


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
    def read_only_fields(self) -> list:
        return []
    
    @staticmethod
    def query_fields(self) -> list[dict[str, any]]:
        return []
    
    def to_json(self) -> str:
        return json.dumps(self.to_response())
    
    def to_response(self) -> dict:
        d = self.__dict__
        allowed_keys = []
        for key in d.keys():
            if not key.startswith('_') and key.find('_id') == -1 and key not in self.restricted_fields():
                allowed_keys.append(key)
        d = {key: d[key] for key in allowed_keys}
        for key, value in d.items():
            if isinstance(value, BaseDBModel):
                d[key] = value.to_response()
            if isinstance(value, Interval):
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