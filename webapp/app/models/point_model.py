from __future__ import annotations
import uuid
from app.models import BASE
from sqlalchemy import UUID, Boolean, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.event_model import EventInstance, Point
from app.models.students_model import Student

class PointEarned(BASE):
    __tablename__ = 'points_earned_table'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('students_table.id'), nullable=False, index=True)
    student: Mapped[Student] = relationship('Student', primaryjoin='PointEarned.student_id == Student.id')
    event_instance_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('event_instances_table.id'), nullable=False, index=True)
    event_instance: Mapped[EventInstance] = relationship('EventInstance', primaryjoin='PointEarned.event_instance_id == EventInstance.id')
    point_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('points_table.id'), nullable=False, index=True)
    point: Mapped[Point] = relationship('Point', primaryjoin='PointEarned.point_id == Point.id')
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=True, )


class PointSpent(BASE):
    __tablename__ = 'points_spent_table'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('students_table.id'), nullable=False, index=True)
    student: Mapped[Student] = relationship('Student', primaryjoin='PointSpent.student_id == Student.id')
    event_instance_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('event_instances_table.id'), nullable=False, index=True)
    event_instance: Mapped[EventInstance] = relationship('EventInstance', primaryjoin='PointSpent.event_instance_id == EventInstance.id')
    points: Mapped[Point] = mapped_column(Integer, default=0)
    deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=True, )


class RunningTotal(BASE):
    __tablename__ = 'running_totals_table'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('students_table.id'), nullable=False, index=True)
    student: Mapped[Student] = relationship('Student', primaryjoin='RunningTotal.student_id == Student.id')
    total_points: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=True, )
