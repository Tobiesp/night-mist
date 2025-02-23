from app import SQL_DB
from app.models.base_model import BaseTable
from app.models.privileges_model import Privilege


class Role(BaseTable):
    name = SQL_DB.Column(SQL_DB.String(100), unique=True, nullable=False)
    privileges: list[Privilege] = SQL_DB.relationship('Privilege', back_populates='role')
    users = SQL_DB.relationship('User', back_populates='role')

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Role {self.name}>'