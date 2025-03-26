from __future__ import annotations
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask_principal import Permission, RoleNeed
from typing import List

from app.models import BASE
from app.models.base_db_model import BaseDBModel


MAX_LOGIN_ATTEMPTS = 5


admin_permission = Permission(RoleNeed('admin'))
student_read_permission = Permission(RoleNeed('student_read'), RoleNeed('admin'), RoleNeed('student_write'))
student_write_permission = Permission(RoleNeed('student_write'), RoleNeed('admin'))
point_read_permission = Permission(RoleNeed('point_read'), RoleNeed('admin'), RoleNeed('point_write'))
point_write_permission = Permission(RoleNeed('point_write'), RoleNeed('admin'))
event_read_permission = Permission(RoleNeed('event_read'), RoleNeed('admin'), RoleNeed('event_write'))
event_write_permission = Permission(RoleNeed('event_write'), RoleNeed('admin'))
reporter_read_permission = Permission(RoleNeed('reporter_read'), RoleNeed('admin'), RoleNeed('reporter_write'))
reporter_write_permission = Permission(RoleNeed('reporter_write'), RoleNeed('admin'))


role_priviledge_table = Table(
    "role_priviledge_table",
    BASE.metadata,
    Column("role_id", ForeignKey("roles_table.id"), primary_key=True, index=True),
    Column("priviledge_id", ForeignKey("priviledges_table.id"), primary_key=True, index=True),
)


class Priviledge(BaseDBModel, BASE):
    __tablename__ = 'priviledges_table'

    priviledge_name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False, index=True)
    roles: Mapped[List[Role]] = relationship(
        "Role",
        secondary=role_priviledge_table,
        primaryjoin="Priviledge.id == role_priviledge_table.c.priviledge_id",
        secondaryjoin="Role.id == role_priviledge_table.c.role_id",
        back_populates="priviledges"
    )

    @staticmethod
    def query_fields():
        query_fields: list[dict[str, any]] = BaseDBModel.query_fields()
        query_fields.append({'field': 'priviledge_name', 'model': None})
        return query_fields

    def __init__(self, priviledge_name: str):
        self.priviledge_name = priviledge_name

    def __repr__(self):
        return f'<Privilege {self.priviledge_name}>'


class Role(BaseDBModel, BASE):
    __tablename__ = 'roles_table'

    role_name = mapped_column(String(100), unique=True, nullable=False, index=True)
    priviledges: Mapped[List[Priviledge]] = relationship(
        "Priviledge",
        secondary=role_priviledge_table,
        primaryjoin="Role.id == role_priviledge_table.c.role_id",
        secondaryjoin="Priviledge.id == role_priviledge_table.c.priviledge_id",
        back_populates="roles",
        lazy='immediate'
    )
    users: Mapped[List[User]] = relationship(
        "User",
        primaryjoin="Role.id == User.role_id",
        back_populates='role'
    )

    @staticmethod
    def query_fields():
        query_fields: list[dict[str, any]] = BaseDBModel.query_fields()
        query_fields.append({'field': 'role_name', 'model': None})
        query_fields.append({'field': 'priviledges', 'model': Priviledge})
        return query_fields

    def __repr__(self):
        return f'<Role {self.role_name}>'


class User(BaseDBModel, UserMixin, BASE):
    __tablename__ = 'users_table'
    
    username = mapped_column(String(100), unique=True, nullable=False, index=True)
    firstname = mapped_column(String(100), nullable=False, index=True)
    lastname = mapped_column(String(100), nullable=False, index=True)
    # unique constraint on combination of firstname and lastname
    __table_args__ = (
        UniqueConstraint('firstname', 'lastname', name='unique_name'),
    )
    email = mapped_column(String(200), unique=True, nullable=False, index=True)
    password_hash = mapped_column(String(200), nullable=False)
    role_id = mapped_column(ForeignKey('roles_table.id'), index=True)
    role: Mapped[Role] = relationship(primaryjoin="User.role_id == Role.id", back_populates='users', lazy='immediate')
    account_locked = mapped_column(Boolean, default=False)
    last_login: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=True)
    login_attempts = mapped_column(Integer, default=0)

    @staticmethod
    def query_fields():
        query_fields: list[dict[str, any]] = BaseDBModel.query_fields()
        query_fields.append({'field': 'username', 'model': None})
        query_fields.append({'field': 'firstname', 'model': None})
        query_fields.append({'field': 'lastname', 'model': None})
        query_fields.append({'field': 'email', 'model': None})
        query_fields.append({'field': 'role', 'model': Role})
        return query_fields
    
    @staticmethod
    def read_only_fields() -> list:
        return super().read_only_fields() + ['username']

    def set_password(self, password):
        print(f'Setting password: {password}')
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_active(self):
        return not self.account_locked
    
    def restricted_fields(self):
        return super().restricted_fields() + ['password_hash'] + ['role_id'] + ['login_attempts']
    
    def add_login_attempt(self):
        self.login_attempts += 1
        if self.login_attempts >= MAX_LOGIN_ATTEMPTS:
            self.account_locked = True
    
    def reset_login_attempts(self):
        self.login_attempts = 0
        self.account_locked = False

    def set_login_date(self):
        self.last_login = datetime.datetime.now()

    def lock_account(self):
        self.account_locked = True

    def unlock_account(self):
        self.account_locked = False
    
    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        if self is other:
            return True
        if self.id is None or other.id is None:
            return self.username == other.username
        return self.id == other.id and self.username == other.username

    def __repr__(self):
        return f"<User {self.username}>"
