from app import SQL_DB
from app.models.base_model import BaseTable
from flask_principal import Permission, RoleNeed


admin_permission = Permission(RoleNeed('admin'))
student_read_permission = Permission(RoleNeed('student_read'))
student_write_permission = Permission(RoleNeed('student_write'))
point_read_permission = Permission(RoleNeed('point_read'))
point_write_permission = Permission(RoleNeed('point_write'))
event_read_permission = Permission(RoleNeed('event_read'))
event_write_permission = Permission(RoleNeed('event_write'))
reporter_read_permission = Permission(RoleNeed('reporter_read'))
reporter_write_permission = Permission(RoleNeed('reporter_write'))


class Privilege(BaseTable):
    name = SQL_DB.Column(SQL_DB.String(100), unique=True, nullable=False)
    role = SQL_DB.relationship('Role', back_populates='privileges')

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return f'<Privilege {self.name}>'