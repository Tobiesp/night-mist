from typing import Generic, TypeVar
import uuid

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.models.base_db_model import BaseDBModel


T = TypeVar('T', bound=BaseDBModel)

class BaseDatabaseRepository(Generic[T]):
    def __init__(self, model: Generic[T], app: Flask = None, db: SQLAlchemy = None):
        self.model = model
        self._app_ = app
        self._db_ = db
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_.session.close()

    def get_all(self) -> list[T]:
        with self._app_.app_context():
            items = []
            if hasattr(self.model, 'deleted'):
                items = self._db_.session.query(self.model).filter_by(deleted=False).all()
            else:
                items = self._db_.session.query(self.model).all()
            return items

    def get_by_id(self, id: str) -> T:
        uuid_id = uuid.UUID(id)
        with self._app_.app_context():
            return self._db_.session.query(self.model).get(uuid_id)

    def create(self, **kwargs) -> T:
        with self._app_.app_context():
            kwargs = {key: value for key, value in kwargs.items() if key in self.model.__dict__ and not key.startswith('_') and key != 'id'}
            new_instance = self.model(**kwargs)
            for key, value in kwargs.items():
                # check if value is a database model class
                if isinstance(value, BaseDBModel):
                    value = self._db_.session.query(value.__class__).get(value.id)
                # Check if value is a list of database model classes
                if isinstance(value, list):
                    value = [self._db_.session.query(item.__class__).get(item.id) for item in value]
            self._db_.session.add(new_instance)
            self._db_.session.commit()
            return new_instance

    def update(self, id: str, **kwargs) -> T:
        with self._app_.app_context():
            instance = self.get_by_id(id)
            kwargs = {key: value for key, value in kwargs.items() if key in self.model.__dict__ and not key.startswith('_') and key != 'id'}
            for key, value in kwargs.items():
                # check if value is a database model class
                if hasattr(value, 'id'):
                    value = self._db_.session.query(value.__class__).get(value.id)
                # Check if value is a list of database model classes
                if isinstance(value, list):
                    value = [self._db_.session.query(item.__class__).get(item.id) for item in value]
                setattr(instance, key, value)
            self._db_.session.commit()
            return instance

    def delete(self, id) -> T:
        with self._app_.app_context():
            instance = self.get_by_id(id)
            # Check if model has a deleted column
            if hasattr(instance, 'deleted'):
                instance.deleted = True
                self._db_.session.commit()
                return instance
        self._db_.session.delete(instance)
        self._db_.session.commit
        return instance
    
    def purge(self) -> None:
        with self._app_.app_context():
            if hasattr(self.model, 'deleted'):
                instances = self._db_.session.query(self.model).filter(self.model.deleted is True).all()
                for instance in instances:
                    self._db_.session.delete(instance)
                self._db_.session.commit()

    def get_count(self) -> int:
        with self._app_.app_context():
            if hasattr(self.model, 'deleted'):
                return self._db_.session.query(self.model).filter(self.model.deleted is False).count()
            return self._db_.session.query(self.model).count()
        
    def get_by(self, **kwargs) -> list[T]:
        with self._app_.app_context():
            if hasattr(self.model, 'deleted'):
                return self._db_.session.query(self.model).filter_by(deleted=False, **kwargs).all()
            return self._db_.session.query(self.model).filter_by(**kwargs).all()