from __future__ import annotations
from typing import List
from app.models import BASE
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_db_model import BaseDBModel, Interval
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
    def query_fields():
        query_fields: list[dict[str, any]] = super().query_fields()
        query_fields.append({'field': 'point_category', 'model': PointCategory})
        query_fields.append({'field': 'student_group', 'model': StudentGroup})
        return query_fields
    
    def restricted_fields(self):
        return super().restricted_fields() + ['points_interval'] + ['point_category_id'] + ['student_group_id']


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