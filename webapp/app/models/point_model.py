from __future__ import annotations
from app.models import BASE
from sqlalchemy import UUID, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_db_model import BaseDBModel
from app.models.event_model import EventInstance, Point
from app.models.students_model import Student

class PointEarned(BaseDBModel, BASE):
    __tablename__ = 'points_earned_table'

    student_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('students_table.id'), nullable=False, index=True)
    student: Mapped[Student] = relationship('Student', primaryjoin='PointEarned.student_id == Student.id', lazy='immediate')
    event_instance_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('event_instances_table.id'), nullable=False, index=True)
    event_instance: Mapped[EventInstance] = relationship('EventInstance', primaryjoin='PointEarned.event_instance_id == EventInstance.id', lazy='immediate')
    point_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('points_table.id'), nullable=False, index=True)
    point: Mapped[Point] = relationship('Point', primaryjoin='PointEarned.point_id == Point.id', lazy='immediate')
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    @staticmethod
    def query_fields():
        query_fields: list[dict[str, any]] = BaseDBModel.query_fields()
        query_fields.append({'field': 'student', 'model': Student})
        query_fields.append({'field': 'event_instance', 'model': EventInstance})
        query_fields.append({'field': 'point', 'model': Point})
        return query_fields


class PointSpent(BaseDBModel, BASE):
    __tablename__ = 'points_spent_table'

    student_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('students_table.id'), nullable=False, index=True)
    student: Mapped[Student] = relationship('Student', primaryjoin='PointSpent.student_id == Student.id', lazy='immediate')
    event_instance_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('event_instances_table.id'), nullable=False, index=True)
    event_instance: Mapped[EventInstance] = relationship('EventInstance', primaryjoin='PointSpent.event_instance_id == EventInstance.id', lazy='immediate')
    points: Mapped[Point] = mapped_column(Integer, default=0)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)

    @staticmethod
    def query_fields():
        query_fields: list[dict[str, any]] = BaseDBModel.query_fields()
        query_fields.append({'field': 'student', 'model': Student})
        query_fields.append({'field': 'event_instance', 'model': EventInstance})
        return query_fields


class RunningTotal(BaseDBModel, BASE):
    __tablename__ = 'running_totals_table'

    student_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('students_table.id'), nullable=False, index=True)
    student: Mapped[Student] = relationship('Student', primaryjoin='RunningTotal.student_id == Student.id', lazy='immediate')
    total_points: Mapped[int] = mapped_column(Integer, default=0)

    @staticmethod
    def query_fields():
        query_fields: list[dict[str, any]] = BaseDBModel.query_fields()
        query_fields.append({'field': 'student', 'model': Student})
        return query_fields
