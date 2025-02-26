from __future__ import annotations
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.models import BASE
from app.models.users_model import User, Role, Priviledge

class DatabaseRepository:

    _instance = None
    _app_ = None
    _db_ = None

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
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_.session.close()

    def get_all_privleges(self) -> list[Priviledge]:
        with self._app_.app_context():
            return self._db_.session.query(Priviledge).all()
    
    def create_privilege(self, name: str) -> Priviledge:
        with self._app_.app_context():
            privilege = Priviledge(priviledge_name=name)
            self._db_.session.add(privilege)
            self._db_.session.commit()
            return privilege
    
    def get_privilege_by_id(self, id: int) -> Priviledge:
        with self._app_.app_context():
            return self._db_.session.query(Priviledge).get(id)
    
    def get_privilege_by_name(self, name: str) -> Priviledge:
        with self._app_.app_context():
            return self._db_.session.query(Priviledge).filter_by(priviledge_name=name).first()
    
    def get_all_roles(self) -> list[Role]:
        with self._app_.app_context():
            return self._db_.session.query(Role).all()
    
    def create_role(self, name: str) -> Role:
        with self._app_.app_context():
            role = Role(role_name=name)
            self._db_.session.add(role)
            self._db_.session.commit()
            return role
    
    def update_role(self, role: Role) -> Role:
        with self._app_.app_context():
            self.get_role_by_name(role.role_name).priviledges = role.priviledges
            self._db_.session.commit()
            return role
    
    def delete_role(self, role: Role) -> None:
        with self._app_.app_context():
            self._db_.session.delete(role)
            self._db_.session.commit()
    
    def get_role_by_id(self, id: int) -> Role:
        with self._app_.app_context():
            return self._db_.session.query(Role).get(id)
    
    def get_role_by_name(self, name: str) -> Role:
        with self._app_.app_context():
            return self._db_.session.query(Role).filter_by(role_name=name).first()
    
    def get_user_by_email(self, email: str) -> User:
        with self._app_.app_context():
            return self._db_.session.query(User).filter_by(email=email).first()
    
    def get_all_users(self) -> list[User]:
        with self._app_.app_context():
            return self._db_.session.query(User).all()
    
    def create_user(self, user: User) -> User:
        with self._app_.app_context():
            self._db_.session.add(user)
            self._db_.session.commit()
            return user
    
    def update_user(self, user: User) -> User:
        with self._app_.app_context():
            self.get_user_by_username(user.username).firstname = user.firstname
            self.get_user_by_username(user.username).lastname = user.lastname
            self.get_user_by_username(user.username).email = user.email
            self.get_user_by_username(user.username).role = user.role
            self._db_.session.commit()
            return
    
    def delete_user(self, user: User) -> None:
        with self._app_.app_context():
            self._db_.session.delete(user)
            self._db_.session.commit
    
    def get_user_by_id(self, id: int) -> User:
        with self._app_.app_context():
            return self._db_.session.query(User).get(id)
    
    def get_user_by_username(self, username: str) -> User:
        with self._app_.app_context():
            return self._db_.session.query(User).filter_by(username=username).first()

