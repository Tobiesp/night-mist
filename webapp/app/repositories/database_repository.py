from __future__ import annotations
from typing import Generic, TypeVar
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.models import BASE
from app.models.base_db_model import BaseDBModel
from app.repositories.base_database_repository import BaseDatabaseRepository

T = TypeVar('T', bound=BaseDBModel)

class DatabaseRepository:

    _instance = None
    _app_ = None
    _db_ = None
    _model_db_: dict[str, BaseDatabaseRepository] = {}
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

    def get_model_db_repository(self, model: Generic[T]) -> BaseDatabaseRepository:
        if model.__name__ not in self._model_db_:
            self._model_db_[model.__name__] = BaseDatabaseRepository(model, self._app_, self._db_)
        return self._model_db_[model.__name__]