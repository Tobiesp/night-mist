from __future__ import annotations
from typing import List
import uuid
from app.models import BASE
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, String, Table, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

    

grade_student_group_table = Table(
    "grade_student_group_table",
    BASE.metadata,
    Column("grade_id", ForeignKey("grades_table.id"), primary_key=True),
    Column("student_group_id", ForeignKey("student_groups_table.id"), primary_key=True),
)


class Grade(BASE):
    __tablename__ = 'grades_table'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    grade_name = mapped_column(String(100), unique=True, nullable=False)
    students: Mapped[list] = relationship('Student', back_populates='grade', index=True)
    student_groups: Mapped[List[StudentGroup]] = relationship(
        "StudentGroup",
        secondary=grade_student_group_table,
        primaryjoin="Grade.id == grade_student_group_table.c.grade_id",
        secondaryjoin="StudentGroup.id == grade_student_group_table.c.student_group_id",
        back_populates="grades",
        index=True
    )
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=True, )  # Ensure default value

    def __init__(self, grade_name: str):
        self.grade_name = grade_name

    def __repr__(self):
        return f'<Grade {self.grade_name}>'
    
    def __eq__(self, other: Grade) -> bool:
        return self.grade_name == other.grade_name
    

class StudentGroup(BASE):
    __tablename__ = 'student_groups_table'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    group_name = mapped_column(String(100), unique=True, nullable=False, index=True)
    grades: Mapped[List[Grade]] = relationship(
        "Grade",
        secondary=grade_student_group_table,
        primaryjoin="StudentGroup.id == grade_student_group_table.c.student_group_id",
        secondaryjoin="Grade.id == grade_student_group_table.c.grade_id",
        back_populates="student_groups"
    )
    deleted = mapped_column(Boolean, default=False)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=True, )  # Ensure default value

    def __init__(self, group_name: str, grades: list[Grade] = []):
        self.group_name = group_name
        self.grades = grades

    def __repr__(self):
        return f'<StudentGroup {self.group_name}>'
    
    def __eq__(self, other: StudentGroup) -> bool:
        return self.group_name == other.group_name

class Student(BASE):
    __tablename__ = 'students_table'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    firstname = mapped_column(String(100), nullable=False, index=True)
    lastname = mapped_column(String(100), nullable=False, index=True)
    # restriction that firstname and lastname together must be unique
    __table_args__ = (UniqueConstraint('firstname', 'lastname', name='unique_student_name'),)
    grade_id = mapped_column(UUID(as_uuid=True), ForeignKey('grades_table.id'))
    grade = relationship('Grade', back_populates='students')
    student_group_id = mapped_column(UUID(as_uuid=True), ForeignKey('student_groups_table.id'))
    student_group = relationship('StudentGroup')
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(), nullable=True, )  # Ensure default value

    @property
    def student_name(self) -> str:
        return f"{self.firstname} {self.lastname}"
    
    def __repr__(self):
        return f'<Student {self.student_name}>'
    
    def __eq__(self, other: Student) -> bool:
        return self.student_name == other.student_name