from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from app import SQL_DB
from app.models.base_model import BaseTable
from app.models.roles_model import Role


class User(UserMixin, BaseTable):
    username = SQL_DB.Column(SQL_DB.String(100), unique=True, nullable=False)
    firstname = SQL_DB.Column(SQL_DB.String(100), nullable=False)
    lastname = SQL_DB.Column(SQL_DB.String(100), nullable=False)
    email = SQL_DB.Column(SQL_DB.String(200), unique=True, nullable=False)
    password_hash = SQL_DB.Column(SQL_DB.String(200), nullable=False)
    role: Optional[Role] = SQL_DB.relationship('Role', back_populates='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"
