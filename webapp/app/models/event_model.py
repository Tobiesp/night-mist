from __future__ import annotations
import datetime
import json
from typing import List
from app.models import BASE
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel, Field, field_validator

from app.models.base_db_model import BaseDBModel
from app.models.students_model import StudentGroup
    

event_student_group_table = Table(
    "event_student_group_table",
    BASE.metadata,
    Column("event_id", ForeignKey("events_table.id"), primary_key=True),
    Column("student_group_id", ForeignKey("student_groups_table.id"), primary_key=True),
)
    

event_point_category_table = Table(
    "event_point_category_table",
    BASE.metadata,
    Column("event_id", ForeignKey("events_table.id"), primary_key=True),
    Column("point_category_id", ForeignKey("events_table.id"), primary_key=True),
)


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
    

class Point(BaseDBModel, BASE):
    __tablename__ = 'points_table'

    point_category_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('point_categories_table.id'), primary_key=True)
    student_group_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('student_groups_table.id'), primary_key=True)
    __table_args__ = (UniqueConstraint('point_category_id', 'student_group_id', name='point_category_student_group_uc'),)
    points: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    points_interval: Mapped[str] = mapped_column(String(100), nullable=True)
    student_group: Mapped[StudentGroup] = relationship('StudentGroup', primaryjoin='Point.student_group_id == StudentGroup.id', lazy='immediate')
    point_category: Mapped[PointCategory] = relationship('PointCategory', primaryjoin='Point.point_category_id == PointCategory.id', lazy='immediate')
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    @property
    def interval(self) -> Interval:
        interval = Interval()
        return interval.from_json(self.points_interval)
    
    @interval.setter
    def interval(self, value: Interval):
        self.points_interval = value.to_json()

    @staticmethod
    def query_fields(self):
        query_fields: list[dict[str, any]] = super().query_fields()
        query_fields.append({'field': 'point_category', 'model': PointCategory})
        query_fields.append({'field': 'student_group', 'model': StudentGroup})
        return query_fields


class PointCategory(BaseDBModel, BASE):
    __tablename__ = 'point_categories_table'

    category_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    description: Mapped[str] = mapped_column(String(1024), nullable=True)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    @staticmethod
    def query_fields(self):
        query_fields: list[dict[str, any]] = super().query_fields()
        query_fields.append({'field': 'category_name', 'model': None})
        return query_fields


class Event(BaseDBModel, BASE):
    __tablename__ = 'events_table'

    event_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    event_interval: Mapped[str] = mapped_column(String(100), nullable=True)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    student_groups: Mapped[List[StudentGroup]] = relationship(
        "StudentGroup",
        secondary=event_student_group_table,
        primaryjoin="Event.id == event_student_group_table.c.event_id",
        secondaryjoin="StudentGroup.id == event_student_group_table.c.student_group_id", 
        lazy='immediate'
    )
    point_categories: Mapped[List[PointCategory]] = relationship(
        "PointCategory",
        secondary=event_point_category_table,
        primaryjoin="Event.id == event_point_category_table.c.event_id",
        secondaryjoin="PointCategory.id == event_point_category_table.c.point_category_id", 
        lazy='immediate'
    )

    @staticmethod
    def query_fields(self):
        query_fields: list[dict[str, any]] = super().query_fields()
        query_fields.append({'field': 'event_name', 'model': None})
        query_fields.append({'field': 'student_groups', 'model': StudentGroup})
        query_fields.append({'field': 'point_categories', 'model': PointCategory})
        return query_fields

    @property
    def interval(self) -> Interval:
        interval = Interval()
        return interval.from_json(self.event_interval)
    
    @interval.setter
    def interval(self, value: Interval):
        self.event_interval = value.to_json()

    def __repr__(self):
        return f'<Event {self.event_name}>'
    

class EventInstance(BaseDBModel, BASE):
    __tablename__ = 'event_instances_table'

    event_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('events_table.id'), nullable=False, index=True)
    event: Mapped[Event] = relationship('Event', primaryjoin='EventInstance.event_id == Event.id', lazy='immediate')
    event_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    @staticmethod
    def query_fields(self):
        query_fields: list[dict[str, any]] = super().query_fields()
        query_fields.append({'field': 'event', 'model': Event})
        return query_fields