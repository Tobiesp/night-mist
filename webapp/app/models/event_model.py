from __future__ import annotations
import datetime
import json
from typing import List
import uuid
from app.models import BASE
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String, Table, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from pydantic import BaseModel, Field, field_validator

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
    repeat = Field(min_length=4, max_length=7, default='none')
    month_day = Field(ge=0, le=30, default=0)
    week_day = Field(ge=0, le=7, default=0)
    hour = Field(ge=0, le=23, default=0)
    minute = Field(ge=0, le=59, default=0)

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
            return datetime.datetime.combine(date, datetime.time(self.hour, self.minute))
        else:
            raise ValueError(f'Invalid repeat value: {self.repeat}')
        
    def is_event_passed(self, check_date: datetime) -> bool:
        return check_date < datetime.datetime.now()
        
    def __repr__(self):
        return f'<Interval: {self.repeat}>'
    

class Point(BASE):
    __tablename__ = 'points_table'

    point_category_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('point_categories_table.id'), primary_key=True)
    student_group_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('student_groups_table.id'), primary_key=True)
    points = mapped_column(Integer, nullable=False, default=0)
    points_interval = mapped_column(String(100), nullable=True)
    student_group: Mapped[StudentGroup] = relationship('StudentGroup', back_populates='points', index=True)
    point_category: Mapped[PointCategory] = relationship('PointCategory', back_populates='points', index=True)
    deleted = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=True, )  # Ensure default value

    @property
    def interval(self) -> Interval:
        interval = Interval()
        return interval.from_json(self.points_interval)
    
    @interval.setter
    def interval(self, value: Interval):
        self.points_interval = value.to_json()


class PointCategory(BASE):
    __tablename__ = 'point_categories_table'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_name = mapped_column(String(100), unique=True, nullable=False, index=True)
    description = mapped_column(String(1024), nullable=True, index=True)
    points: Mapped[List[Point]] = relationship('Point', back_populates='point_category')
    deleted = mapped_column(Boolean, default=False)
    events: Mapped[List[Event]] = relationship(
        "Event",
        secondary=event_point_category_table,
        primaryjoin="PointCategory.id == event_point_category_table.c.point_category_id",
        secondaryjoin="Event.id == event_point_category_table.c.event_id",
        back_populates="point_categories",
        index=True
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=True, )  # Ensure default value


class Event(BASE):
    __tablename__ = 'events_table'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_name = mapped_column(String(100), unique=True, nullable=False, index=True)
    event_interval = mapped_column(String(100), nullable=True)
    deleted = mapped_column(Boolean, default=False)
    student_groups: Mapped[List[StudentGroup]] = relationship(
        "StudentGroup",
        secondary=event_student_group_table,
        primaryjoin="Event.id == event_student_group_table.c.event_id",
        secondaryjoin="StudentGroup.id == event_student_group_table.c.student_group_id", 
        index=True
    )
    point_categories: Mapped[List[PointCategory]] = relationship(
        "PointCategory",
        secondary=event_point_category_table,
        primaryjoin="Event.id == event_point_category_table.c.event_id",
        secondaryjoin="PointCategory.id == event_point_category_table.c.point_category_id",
        back_populates="events", 
        index=True
    )
    event_instances: Mapped[List[EventInstance]] = relationship('EventInstance', back_populates='events', index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=True, )  # Ensure default value

    @property
    def interval(self) -> Interval:
        interval = Interval()
        return interval.from_json(self.event_interval)
    
    @interval.setter
    def interval(self, value: Interval):
        self.event_interval = value.to_json()

    def __repr__(self):
        return f'<Event {self.event_name}>'
    

class EventInstance(BASE):
    __tablename__ = 'event_instances_table'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('events_table.id'), nullable=False)
    event: Mapped[Event] = relationship('Event', primaryjoin='EventInstance.event_id == Event.id', index=True)
    event_date = mapped_column(DateTime(timezone=True), nullable=False)
    completed = mapped_column(Boolean, default=False)
    deleted = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=True, )  # Ensure default value