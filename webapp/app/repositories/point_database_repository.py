import uuid
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from app.models.event_model import EventInstance, Point
from app.models.point_model import PointEarned, PointSpent, RunningTotal
from app.models.students_model import Student


class PointDatabaseRepository:

    _app_ = None
    _db_ = None

    def __init__(self, app: Flask = None, db: SQLAlchemy = None): 
        self._db_ = db
        self._app_ = app
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_.session.close()

    def get_all_points_earned(self) -> list[PointEarned]:
        with self._app_.app_context():
            return self._db_.session.query(PointEarned).where(PointEarned.deleted is False).all()
        
    def create_point_earned(self, point: PointEarned) -> PointEarned:
        with self._app_.app_context():
            self._db_.session.add(point)
            self._db_.session.commit()
            return point
        
    def get_point_earned_by_id(self, id: str) -> PointEarned:
        uuid_id = uuid.UUID(id)
        with self._app_.app_context():
            return self._db_.session.query(PointEarned).get(uuid_id)
        
    def get_points_earned_by_student(self, s: Student) -> list[PointEarned]:
        with self._app_.app_context():
            return self._db_.session.query(PointEarned).filter((PointEarned.student == s) & (PointEarned.deleted is False)).all()
        
    def get_points_earned_by_event_instance(self, event_instance: EventInstance) -> list[PointEarned]:
        with self._app_.app_context():
            return self._db_.session.query(PointEarned).filter((PointEarned.event_instance == event_instance) & (PointEarned.deleted is False)).all()
        
    def get_points_earned_by_point(self, point: Point) -> list[PointEarned]:
        with self._app_.app_context():
            return self._db_.session.query(PointEarned).filter((PointEarned.point == point) & (PointEarned.deleted is False)).all()
        
    def update_point_earned(self, point: PointEarned) -> PointEarned:
        with self._app_.app_context():
            p = self.get_point_earned_by_id(point.id)
            p.point = point.point
            p.student = point.student
            p.event_instance = point.event_instance
            self._db_.session.commit()
            return point
        
    def delete_point_earned(self, point: PointEarned) -> None:
        with self._app_.app_context():
            p = self._db_.session.query(PointEarned).filter_by(id=point.id).first()
            p.deleted = True
            self._db_.session.add(p)
            self._db_.session.commit()

    def purge_points_earned(self) -> None:
        with self._app_.app_context():
            points = self._db_.session.query(PointEarned).filter_by(deleted=True).all()
            for point in points:
                self._db_.session.delete(point)
            self._db_.session.commit()

    def get_point_earned_count(self) -> int:
        with self._app_.app_context():
            return self._db_.session.query(func.count(PointEarned.id)).filter_by(deleted=True).scalar()
        
    def get_all_points_spent(self) -> list[PointSpent]:
        with self._app_.app_context():
            return self._db_.session.query(PointSpent).where(PointSpent.deleted is False).all()
        
    def create_point_spent(self, point: PointSpent) -> PointSpent:
        with self._app_.app_context():
            self._db_.session.add(point)
            self._db_.session.commit()
            return point
        
    def get_point_spent_by_id(self, id: str) -> PointSpent:
        uuid_id = uuid.UUID(id)
        with self._app_.app_context():
            return self._db_.session.query(PointSpent).get(uuid_id)
        
    def get_points_spent_by_student(self, s: Student) -> list[PointSpent]:
        with self._app_.app_context():
            return self._db_.session.query(PointSpent).filter((PointSpent.student == s) & (PointSpent.deleted is False)).all()
        
    def get_points_spent_by_event_instance(self, event_instance: EventInstance) -> list[PointSpent]:
        with self._app_.app_context():
            return self._db_.session.query(PointSpent).filter((PointSpent.event_instance == event_instance) & (PointSpent.deleted is False)).all()
        
    def update_point_spent(self, point: PointSpent) -> PointSpent:
        with self._app_.app_context():
            p = self.get_point_spent_by_id(point.id)
            p.points = point.points
            p.student = point.student
            p.event_instance = point.event_instance
            self._db_.session.commit()
            return point
        
    def delete_point_spent(self, point: PointSpent) -> None:
        with self._app_.app_context():
            p = self._db_.session.query(PointSpent).filter_by(id=point.id).first()
            p.deleted = True
            self._db_.session.add(p)
            self._db_.session.commit()

    def purge_points_spent(self) -> None:
        with self._app_.app_context():
            points = self._db_.session.query(PointSpent).filter_by(deleted=True).all()
            for point in points:
                self._db_.session.delete(point)
            self._db_.session.commit()

    def get_point_spent_count(self) -> int:
        with self._app_.app_context():
            return self._db_.session.query(func.count(PointSpent.id)).where(PointSpent.deleted is False).scalar()
        
    def update_running_total_by_student(self, student: Student) -> int:
        with self._app_.app_context():
            earned = self._db_.session.query(func.sum(PointEarned.point.points)).filter((PointEarned.student == student) & (PointEarned.deleted is False)).scalar()
            spent = self._db_.session.query(func.sum(PointSpent.points)).filter((PointSpent.student == student) & (PointSpent.deleted is False)).scalar()
            total = earned - spent
            r = self.get_running_total_by_student(student)
            r.total_points = total
            self._db_.session.commit()
            return total
        
    def get_all_running_totals(self) -> list[RunningTotal]:
        with self._app_.app_context():
            return self._db_.session.query(RunningTotal).all()
        
    def get_running_total_by_id(self, id: str) -> RunningTotal:
        uuid_id = uuid.UUID(id)
        with self._app_.app_context():
            return self._db_.session.query(RunningTotal).get(uuid_id)
        
    def get_running_total_by_student(self, student: Student) -> RunningTotal:
        with self._app_.app_context():
            return self._db_.session.query(RunningTotal).filter((RunningTotal.student == student)).first()
        
    def create_running_total(self, running_total: RunningTotal) -> RunningTotal:
        with self._app_.app_context():
            self._db_.session.add(running_total)
            self._db_.session.commit()
            return running_total
        
    def update_running_total(self, running_total: RunningTotal) -> RunningTotal:
        with self._app_.app_context():
            r = self.get_running_total_by_id(running_total.id)
            r.total_points = running_total.total_points
            self._db_.session.commit()
            return running_total
        
    def delete_running_total(self, running_total: RunningTotal) -> None:
        with self._app_.app_context():
            r = self._db_.session.query(RunningTotal).filter_by(id=running_total.id).first()
            self._db_.session.delete(r)
            self._db_.session.commit()
