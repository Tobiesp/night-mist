from flask import Flask
from flask_login import LoginManager, current_user

from app import set_admin_secret, set_limter
from app.models.students_model import Grade

from app._env import Config, parse
from app.models.users_model import Priviledge, Role, User
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

    set_admin_secret(config.ADMIN_KEY)

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
        datastore = database_repository.DatabaseRepository.instance().get_model_db_repository(User)
        # Return an instance of the User model
        return datastore.get_by_id(userid)
    
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

    # add exception handling
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.exception(e)
        return {'error': 'Internal server error occured'}, 500 # Internal Server Error
    
    @app.errorhandler(404)
    def page_not_found(e):
        return {'error': str(e)}, 404 # Not
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return {'error': str(e)}, 405 # Method Not Allowed
    
    @app.errorhandler(403)
    def forbidden(e):
        return {'error': str(e)}, 403 # Forbidden
    
    @app.errorhandler(401)
    def unauthorized(e):
        return {'error': str(e)}, 401 # Unauthorized
    
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
    user_db = database_repository.DatabaseRepository.instance().get_model_db_repository(User)
    role_db = database_repository.DatabaseRepository.instance().get_model_db_repository(Role)
    admin: User | None = user_db.get_by_first(username='skadmin')
    if admin is None:
        admin = User()
        admin.username = 'skadmin'
        admin.set_password(password)
        admin.firstname = 'Score-Keeper'
        admin.lastname = 'Admin'
        admin.email = 'admin@user.com'
        admin.role = role_db.get_by_first(role_name='admin')
        user_db.create(**admin.__dict__)


def create_initial_grades() -> None:
    datastore = database_repository.DatabaseRepository.instance().get_model_db_repository(Grade)
    grades = [
        'None',
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
        if datastore.get_by_first(grade_name=grade) is None:
            datastore.create(**Grade(grade_name=grade).__dict__)


def create_initial_roles() -> None:
    priviledge_db = database_repository.DatabaseRepository.instance().get_model_db_repository(Priviledge)
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
        if priviledge_db.get_by_first(priviledge_name=priviledge) is None:
            priviledge_db.create(**Priviledge(priviledge_name=priviledge).__dict__)
    
    role_db = database_repository.DatabaseRepository.instance().get_model_db_repository(Role)
    admin: Role | None = role_db.get_by_first(role_name='admin')
    if admin is None:
        role_db.create(**Role(role_name='admin', priviledges=[priviledge_db.get_by_first(priviledge_name='admin')]).__dict__)


def create_email_servant(config: Config) -> None:
    EMAIL_SERVANT = None


def main():
    app = create_app()
    app.run(debug=app.config['DEBUG'])