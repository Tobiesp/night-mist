from flask_sqlalchemy import SQLAlchemy

from app.models.privileges_model import Privilege
from app.models.roles_model import Role
from app.models.users_model import User

class DatabaseRepository:
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def get_all_privleges(self) -> list[Privilege]:
        return self.db.session.query(Privilege).all()
    
    def create_privilege(self, name: str) -> Privilege:
        privilege = Privilege(name=name)
        self.db.session.add(privilege)
        self.db.session.commit()
        return privilege
    
    def get_privilege_by_id(self, id: int) -> Privilege:
        return self.db.session.query(Privilege).get(id)
    
    def get_privilege_by_name(self, name: str) -> Privilege:
        return self.db.session.query(Privilege).filter_by(name=name).first()
    
    def get_all_roles(self) -> list[Role]:
        return self.db.session.query(Role).all()
    
    def create_role(self, name: str) -> Role:
        role = Role(name=name)
        self.db.session.add(role)
        self.db.session.commit()
        return role
    
    def update_role(self, role: Role) -> Role:
        self.get_role_by_name(role.name).privileges = role.privileges
        self.db.session.commit()
        return role
    
    def delete_role(self, role: Role) -> None:
        self.db.session.delete(role)
        self.db.session.commit()
    
    def get_role_by_id(self, id: int) -> Role:
        return self.db.session.query(Role).get(id)
    
    def get_role_by_name(self, name: str) -> Role:
        return self.db.session.query(Role).filter_by(name=name).first()
    
    def get_all_users(self) -> list[User]:
        return self.db.session.query(User).all()
    
    def create_user(self, user: User) -> User:
        self.db.session.add(user)
        self.db.session.commit()
        return user
    
    def update_user(self, user: User) -> User:
        self.get_user_by_username(user.username).firstname = user.firstname
        self.get_user_by_username(user.username).lastname = user.lastname
        self.get_user_by_username(user.username).email = user.email
        self.get_user_by_username(user.username).role = user.role
        self.db.session.commit()
        return
    
    def delete_user(self, user: User) -> None:
        self.db.session.delete(user)
        self.db.session.commit
    
    def get_user_by_id(self, id: int) -> User:
        return self.db.session.query(User).get(id)
    
    def get_user_by_username(self, username: str) -> User:
        return self.db.session.query(User).filter_by(username=username).first()
    
