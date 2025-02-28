from __future__ import annotations
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.models import BASE
from app.repositories.admin_database_repository import AdminDatabaseRepository
from app.repositories.event_database_repository import EventDatabaseRepository
from app.repositories.point_database_repository import PointDatabaseRepository
from app.repositories.student_database_repository import StudentDatabaseRepository

class DatabaseRepository:

    _instance = None
    _app_ = None
    _db_ = None
    _admin_db_ = None
    _student_db_ = None
    _event_db_ = None
    _point_db_ = None

    @classmethod
    def instance(cls, app: Flask = None) -> DatabaseRepository:
        if cls._instance is None:
            cls._instance = cls(app)
        return cls._instance

    def __init__(self, app: Flask = None):
        if self._instance is None:
            self._db_ = SQLAlchemy(app)
            self._app_ = app
            with app.app_context():
                BASE.metadata.create_all(self._db_.engine)
                self._db_.session.commit()
            self._admin_db_ = AdminDatabaseRepository(self._app_, self._db_)
            self._student_db_ = StudentDatabaseRepository(self._app_, self._db_)
            self._event_db_ = EventDatabaseRepository(self._app_, self._db_)
            self._point_db_ = PointDatabaseRepository(self._app_, self._db_)

    def get_admin_db_repository(self) -> AdminDatabaseRepository:
        return self._admin_db_
    
    def get_student_db_repository(self) -> StudentDatabaseRepository:
        return self._student_db_
    
    def get_event_db_repository(self) -> EventDatabaseRepository:
        return self._event_db_
    
    def get_point_db_repository(self) -> PointDatabaseRepository:
        return self._point_db_