from __future__ import annotations
from typing import List
from app.models import BASE
from sqlalchemy import UUID, Column, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base_db_model import BaseDBModel

    

grade_student_group_table = Table(
    "grade_student_group_table",
    BASE.metadata,
    Column("grade_id", ForeignKey("grades_table.id"), primary_key=True),
    Column("student_group_id", ForeignKey("student_groups_table.id"), primary_key=True),
)


class Grade(BaseDBModel, BASE):
    __tablename__ = 'grades_table'

    grade_name = mapped_column(String(100), unique=True, nullable=False)
    students: Mapped[list] = relationship('Student', back_populates='grade')
    student_groups: Mapped[List[StudentGroup]] = relationship(
        "StudentGroup",
        secondary=grade_student_group_table,
        primaryjoin="Grade.id == grade_student_group_table.c.grade_id",
        secondaryjoin="StudentGroup.id == grade_student_group_table.c.student_group_id",
        back_populates="grades"
    )

    @staticmethod
    def query_fields(self):
        query_fields: list[dict[str, any]] = super().query_fields()
        query_fields.append({'field': 'grade_name', 'model': None})
        query_fields.append({'field': 'students', 'model': Student})
        query_fields.append({'field': 'student_groups', 'model': StudentGroup})
        return query_fields

    def __init__(self, grade_name: str):
        self.grade_name = grade_name

    def __repr__(self):
        return f'<Grade {self.grade_name}>'
    

class StudentGroup(BaseDBModel, BASE):
    __tablename__ = 'student_groups_table'

    group_name = mapped_column(String(100), unique=True, nullable=False)
    grades: Mapped[List[Grade]] = relationship(
        "Grade",
        secondary=grade_student_group_table,
        primaryjoin="StudentGroup.id == grade_student_group_table.c.student_group_id",
        secondaryjoin="Grade.id == grade_student_group_table.c.grade_id",
        back_populates="student_groups",
        lazy='immediate'
    )

    @staticmethod
    def query_fields(self):
        query_fields: list[dict[str, any]] = super().query_fields()
        query_fields.append({'field': 'group_name', 'model': None})
        query_fields.append({'field': 'grades', 'model': Grade})
        return query_fields

    def __init__(self, group_name: str, grades: list[Grade] = []):
        self.group_name = group_name
        self.grades = grades

    def __repr__(self):
        return f'<StudentGroup {self.group_name}>'

class Student(BaseDBModel, BASE):
    __tablename__ = 'students_table'

    firstname = mapped_column(String(100), nullable=False)
    lastname = mapped_column(String(100), nullable=False)
    # restriction that firstname and lastname together must be unique
    __table_args__ = (UniqueConstraint('firstname', 'lastname', name='unique_student_name'),)
    grade_id = mapped_column(UUID(as_uuid=True), ForeignKey('grades_table.id'))
    grade = relationship('Grade', back_populates='students', lazy='immediate')
    student_group_id = mapped_column(UUID(as_uuid=True), ForeignKey('student_groups_table.id'))
    student_group = relationship('StudentGroup', lazy='immediate')

    @staticmethod
    def query_fields(self):
        query_fields: list[dict[str, any]] = super().query_fields()
        query_fields.append({'field': 'firstname', 'model': None})
        query_fields.append({'field': 'lastname', 'model': None})
        query_fields.append({'field': 'grade', 'model': Grade})
        query_fields.append({'field': 'student_groups', 'model': StudentGroup})
        return query_fields

    @property
    def student_name(self) -> str:
        return f"{self.firstname} {self.lastname}"
    
    def __repr__(self):
        return f'<Student {self.student_name}>'
    
    def __eq__(self, other: Student) -> bool:
        return self.student_name == other.student_name