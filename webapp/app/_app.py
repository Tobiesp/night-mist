from flask import Blueprint, Flask
from flask_login import LoginManager, current_user

import app.rest as rest_api
import pkgutil
import importlib

from app._env import Config, parse
from app.models.users_model import User
from app.repositories import database_repository
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed


def create_app() -> Flask:
    app = Flask(__name__)
    config: Config = parse()
    app.config.from_object(config)
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['TESTING'] = config.TESTING
    app.config['DEBUG'] = config.DEBUG
    app.config['CSRF_ENABLED'] = config.CSRF_ENABLED
    app.config['PORT'] = config.PORT
    app.config['HOST'] = config.HOST

    create_db(app)

    create_initial_roles(app)
    create_initial_admin(config.ADMIN_INITIAL_PASSWORD)

    create_email_servant()

    import_blueprints(app)

    Principal(app)

    login_manager = LoginManager(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(userid):
        datastore = database_repository.DatabaseRepository(None)
        # Return an instance of the User model
        return datastore.get_user_by_id(userid)
    
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        # Set the identity user object
        user = current_user if isinstance(current_user, User) else None
        if user is None:
            return
        identity.user = user

        

        # Add the UserNeed to the identity
        if hasattr(current_user, 'id'):
            identity.provides.add(UserNeed(current_user.id))

        # Assuming the User model has a list of roles, update the
        # identity with the roles that the user provides
        if hasattr(current_user, 'role'):
            role = current_user.role
            if role is None:
                return
            for privilege in role.priviledges:
                identity.provides.add(RoleNeed(privilege.name))
    
    return app


def import_blueprints(app: Flask) -> Flask:
    package = rest_api
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        module = importlib.import_module(f'{package.__name__}.{module_name}')
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, Blueprint):
                app.register_blueprint(attribute)
                break


def create_db(app: Flask) -> None:
    database_repository.DatabaseRepository.instance(app)


def create_initial_admin(password: str) -> None:
    datastore = database_repository.DatabaseRepository.instance()
    admin = datastore.get_user_by_username('skadmin')
    if admin is None:
        admin = User()
        admin.username = 'skadmin'
        admin.set_password(password)
        admin.firstname = 'Score-Keeper'
        admin.lastname = 'Admin'
        admin.email = 'admin@user.com'
        admin.role = datastore.get_role_by_name('admin')
        datastore.create_user(admin)


def create_initial_roles(app: Flask) -> None:
    datastore = database_repository.DatabaseRepository.instance()
    privileges = [
        'admin',
        'student_read',
        'student_write',
        'point_read',
        'point_write',
        'event_read',
        'event_write',
        'reporter_read',
        'reporter_write'
        ]
    for privilege in privileges:
        if datastore.get_privilege_by_name(privilege) is None:
            datastore.create_privilege(privilege)
    
    admin = datastore.get_role_by_name('admin')
    if admin is None:
        admin = datastore.create_role('admin', [datastore.get_privilege_by_name('admin')])
        datastore.update_role(admin)


def create_email_servant() -> None:
    EMAIL_SERVANT = None


def main():
    app = create_app()
    app.run()