from flask import Flask
from flask_login import LoginManager, current_user

from app import set_limter
from app.models.students_model import Grade

from app._env import Config, parse
from app.models.users_model import User
from app.repositories import database_repository
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS


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

    CORS(app, supports_credentials=True)

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
        datastore = database_repository.DatabaseRepository.instance().get_admin_db_repository()
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
                identity.provides.add(RoleNeed(privilege.priviledge_name))
                print(f'Identity: {identity.provides}')
    
    return app


def import_blueprints(app: Flask) -> Flask:
    from app.rest.admin_rest import admin_api
    app.register_blueprint(admin_api)

    from app.rest.auth_rest import auth_api
    app.register_blueprint(auth_api)

    from app.rest.event_rest import EventRestAPI, EventInstanceRestAPI
    event_api = EventRestAPI()
    event_instance_api = EventInstanceRestAPI()
    app.register_blueprint(event_api.blueprint)
    app.register_blueprint(event_instance_api.blueprint)

    from app.rest.grade_rest import GradeRestAPI
    grade_api = GradeRestAPI()
    app.register_blueprint(grade_api.blueprint)

    from app.rest.point_category_rest import PointCategoryRestAPI
    point_category_api = PointCategoryRestAPI()
    app.register_blueprint(point_category_api.blueprint)

    from app.rest.point_rest import PointRestAPI, PointEarnedRestAPI, PointSpentRestAPI, RunningTotalRestAPI
    point_api = PointRestAPI()
    point_earned_api = PointEarnedRestAPI()
    point_spent_api = PointSpentRestAPI()
    running_total_api = RunningTotalRestAPI()
    app.register_blueprint(point_api.blueprint)
    app.register_blueprint(point_earned_api.blueprint)
    app.register_blueprint(point_spent_api.blueprint)
    app.register_blueprint(running_total_api.blueprint)

    from app.rest.role_rest import RoleRestAPI
    role_api = RoleRestAPI()
    app.register_blueprint(role_api.blueprint)

    from app.rest.student_group_rest import GroupRestAPI
    student_group_api = GroupRestAPI()
    app.register_blueprint(student_group_api.blueprint)

    from app.rest.student_rest import StudentRestAPI
    student_api = StudentRestAPI()
    app.register_blueprint(student_api.blueprint)

    from app.rest.user_rest import UserRestAPI
    user_api = UserRestAPI()
    app.register_blueprint(user_api.blueprint)


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
    priviledges = [
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
    for priviledge in priviledges:
        if datastore.get_privilege_by_name(priviledge) is None:
            datastore.create_privilege(priviledge)
    
    admin = datastore.get_role_by_name('admin')
    if admin is None:
        datastore.create_role('admin', [datastore.get_privilege_by_name('admin')])


def create_email_servant(config: Config) -> None:
    EMAIL_SERVANT = None


def main():
    app = create_app()
    app.run(debug=app.config['DEBUG'])