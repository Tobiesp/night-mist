import uuid
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from app.models.students_model import Grade, Student, StudentGroup


class StudentDatabaseRepository:

    _app_ = None
    _db_ = None

    def __init__(self, app: Flask = None, db: SQLAlchemy = None): 
        self._db_ = db
        self._app_ = app
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_.session.close()

    def get_all_students(self) -> list[Student]:
        with self._app_.app_context():
            return self._db_.session.query(Student).all()
        
    def create_student(self, student: Student) -> Student:
        with self._app_.app_context():
            self._db_.session.add(student)
            self._db_.session.commit()
            return student
        
    def get_student_by_id(self, id: str) -> Student:
        uuid_id = uuid.UUID(id)
        with self._app_.app_context():
            return self._db_.session.query(Student).get(uuid_id)
        
    def get_student_by_name(self, firstname: str, lastname: str) -> Student:
        with self._app_.app_context():
            return self._db_.session.query(Student).filter((Student.firstname == firstname) & (Student.lastname == lastname)).first()
        
    def query_students(self, query: str) -> list[Student]:
        with self._app_.app_context():
            return self._db_.session.query(Student).filter(Student.firstname.ilike(f'%{query}%') | Student.lastname.ilike(f'%{query}%')).all()
        
    def update_student(self, student: Student) -> Student:
        with self._app_.app_context():
            s = self.get_student_by_id(student.id)
            s.firstname = student.firstname
            s.lastname = student.lastname
            s.grade = student.grade
            s.student_group = student.student_group
            self._db_.session.commit()
            return student
        
    def delete_student(self, student: Student) -> None:
        with self._app_.app_context():
            self._db_.session.delete(student)
            self._db_.session.commit()

    def get_student_count(self) -> int:
        with self._app_.app_context():
            return self._db_.session.query(func.count(Student.id)).scalar()
        
    def get_students_by_group(self, group_name: str) -> list[Student]:
        with self._app_.app_context():
            group = self.get_group_by_name(group_name)
            return self._db_.session.query(Student).filter(Student.student_group == group).all()
        
    def get_students_by_grade(self, grade_name: str) -> list[Student]:
        with self._app_.app_context():
            grade = self.get_grade_by_name(grade_name)
            return self._db_.session.query(Student).filter(Student.grade == grade).all()
        
    def get_students_by_group_id(self, id: str) -> list[Student]:
        with self._app_.app_context():
            group = self.get_group_by_id(id)
            return self._db_.session.query(Student).filter(Student.student_group == group).all()
        
    def get_students_by_grade_id(self, id: str) -> list[Student]:
        with self._app_.app_context():
            grade = self.get_grade_by_id(id)
            return self._db_.session.query(Student).filter(Student.grade == grade).all()
        
    def get_all_groups(self) -> list[str]:
        with self._app_.app_context():
            return self._db_.session.query(StudentGroup).distinct().all()
        
    def create_group(self, group: StudentGroup) -> StudentGroup:
        with self._app_.app_context():
            self._db_.session.add(group)
            self._db_.session.commit()
            return group
        
    def get_group_by_id(self, id: str) -> StudentGroup:
        uuid_id = uuid.UUID(id)
        with self._app_.app_context():
            return self._db_.session.query(StudentGroup).get(uuid_id)
        
    def get_group_by_name(self, name: str) -> StudentGroup:
        with self._app_.app_context():
            return self._db_.session.query(StudentGroup).filter(StudentGroup.group_name == name).first()
        
    def update_group(self, group: StudentGroup) -> StudentGroup:
        with self._app_.app_context():
            g = self.get_group_by_id(group.id)
            g.group_name = group.group_name
            g.grades = group.grades
            self._db_.session.commit()
            return group
        
    def delete_group(self, group: StudentGroup) -> None:
        with self._app_.app_context():
            count = self._db_.session.query(StudentGroup).count()
            if count == 1:
                raise Exception('Must have at least one group')
            self._db_.session.delete(group)
            self._db_.session.commit()

    def get_group_count(self) -> int:
        with self._app_.app_context():
            return self._db_.session.query(func.count(StudentGroup.id)).scalar()
        
    def get_all_grades(self) -> list[Grade]:
        with self._app_.app_context():
            return self._db_.session.query(Grade).all()
        
    def create_grade(self, grade: Grade) -> Grade:
        with self._app_.app_context():
            self._db_.session.add(grade)
            self._db_.session.commit()
            return grade
        
    def get_grade_by_id(self, id: str) -> Grade:
        uuid_id = uuid.UUID(id)
        with self._app_.app_context():
            return self._db_.session.query(Grade).get(uuid_id)
        
    def get_grade_by_name(self, name: str) -> Grade:
        with self._app_.app_context():
            return self._db_.session.query(Grade).filter(Grade.grade_name == name).first()
        
    def update_grade(self, grade: Grade) -> Grade:
        with self._app_.app_context():
            g = self.get_grade_by_id(grade.id)
            g.grade_name = grade.grade_name
            g.student_groups = grade.student_groups
            self._db_.session.commit()
            return grade
        
    def delete_grade(self, grade: Grade) -> None:
        with self._app_.app_context():
            count = self._db_.session.query(Grade).count()
            if count == 1:
                raise Exception('Must have at least one grade')
            self._db_.session.delete(grade)
            self._db_.session.commit()

    def get_grade_count(self) -> int:
        with self._app_.app_context():
            return self._db_.session.query(func.count(Grade.id)).scalar()
    