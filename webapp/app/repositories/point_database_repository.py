from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from app.models.event_model import EventInstance
from app.models.point_model import PointEarned, PointSpent
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
            return self._db_.session.query(PointEarned).all()
        
    def create_point_earned(self, point: PointEarned) -> PointEarned:
        with self._app_.app_context():
            self._db_.session.add(point)
            self._db_.session.commit()
            return point
        
    def get_point_earned_by_id(self, id: int) -> PointEarned:
        with self._app_.app_context():
            return self._db_.session.query(PointEarned).get(id)
        
    def get_point_earned_by_student(self, s: Student) -> PointEarned:
        with self._app_.app_context():
            return self._db_.session.query(PointEarned).filter_by(student=s).first()
        
    def get_points_earned_by_event_instance(self, event_instance: EventInstance) -> list[PointEarned]:
        with self._app_.app_context():
            return self._db_.session.query(PointEarned).filter_by(event_instance=event_instance).all()
        
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
            return self._db_.session.query(func.count(PointEarned.id)).scalar()
        
    def get_all_points_spent(self) -> list[PointSpent]:
        with self._app_.app_context():
            return self._db_.session.query(PointSpent).all()
        
    def create_point_spent(self, point: PointSpent) -> PointSpent:
        with self._app_.app_context():
            self._db_.session.add(point)
            self._db_.session.commit()
            return point
        
    def get_point_spent_by_id(self, id: int) -> PointSpent:
        with self._app_.app_context():
            return self._db_.session.query(PointSpent).get(id)
        
    def get_point_spent_by_student(self, s: Student) -> PointSpent:
        with self._app_.app_context():
            return self._db_.session.query(PointSpent).filter_by(student=s).first()
        
    def get_points_spent_by_event_instance(self, event_instance: EventInstance) -> list[PointSpent]:
        with self._app_.app_context():
            return self._db_.session.query(PointSpent).filter_by(event_instance=event_instance).all()
        
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
            return self._db_.session.query(func.count(PointSpent.id)).scalar()
