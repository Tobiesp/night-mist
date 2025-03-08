from flask import Flask
from flask_login import LoginManager, current_user

from app import set_limter
from app.models.students_model import Grade

from app._env import Config, parse
from app.models.users_model import User
from app.repositories import admin_database_repository, database_repository
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


def create_app() -> Flask:
    app = Flask(__name__)
    config: Config = parse()
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
    app.config['SECRET_KEY'] = config.SECRET_KEY
    app.config['TESTING'] = config.TESTING
    app.config['DEBUG'] = config.DEBUG
    app.config['CSRF_ENABLED'] = config.CSRF_ENABLED
    app.config['SERVER_NAME'] = f'{config.HOST}:{config.PORT}'

    limiter = Limiter(
        get_remote_address,
        app=app,
        default_limits=["500 per day", "10 per minute"],
        storage_uri=config.LIMIT_STORAGE,
    )
    set_limter(limiter)

    create_db(app, config)

    create_email_servant(config)

    import_blueprints(app)

    Principal(app)

    login_manager = LoginManager(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(userid):
        datastore = admin_database_repository.AdminDatabaseRepository(None)
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
    from app.rest.admin_rest import admin_api
    app.register_blueprint(admin_api)

    from app.rest.auth_rest import auth_api
    app.register_blueprint(auth_api)

    from app.rest.event_rest import event_api
    app.register_blueprint(event_api)

    from app.rest.grade_rest import grade_api
    app.register_blueprint(grade_api)

    from app.rest.point_category_rest import point_category_api
    app.register_blueprint(point_category_api)

    from app.rest.point_rest import point_api
    app.register_blueprint(point_api)

    from app.rest.role_rest import role_api
    app.register_blueprint(role_api)

    from app.rest.student_group_rest import student_group_api
    app.register_blueprint(student_group_api)

    from app.rest.student_rest import student_api
    app.register_blueprint(student_api)

    from app.rest.user_rest import user_api
    app.register_blueprint(user_api)


def create_db(app: Flask, config: Config) -> None:
    database_repository.DatabaseRepository.instance(app)
    create_initial_roles()
    create_initial_admin(config.ADMIN_INITIAL_PASSWORD)
    create_initial_grades()


def create_initial_admin(password: str) -> None:
    datastore = database_repository.DatabaseRepository.instance().get_admin_db_repository()
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


def create_initial_grades() -> None:
    datastore = database_repository.DatabaseRepository.instance().get_student_db_repository()
    grades = [
        'k0',
        'k1',
        'k2',
        'k3',
        'k4',
        'k5',
        '1st',
        '2nd',
        '3rd',
        '4th',
        '5th',
        '6th',
        '7th',
        '8th',
        '9th',
        '10th',
        '11th',
        '12th',
        'graduated'
    ]
    for grade in grades:
        if datastore.get_grade_by_name(grade) is None:
            datastore.create_grade(Grade(grade_name=grade))


def create_initial_roles() -> None:
    datastore = database_repository.DatabaseRepository.instance().get_admin_db_repository()
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


def create_email_servant(config: Config) -> None:
    EMAIL_SERVANT = None


def main():
    app = create_app()
    app.run()