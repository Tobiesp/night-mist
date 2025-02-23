from flask import Flask
from flask_login import LoginManager, current_user

from app import SQL_DB
from app._env import parse
from app.models.users_model import User
from app.repositories import database_repository
from flask_principal import Principal, identity_loaded, UserNeed, RoleNeed


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(parse())
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    create_db(app)

    import_blueprints(app)

    Principal(app)

    login_manager = LoginManager(app)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(userid):
        datastore = database_repository.DatabaseRepository(SQL_DB)
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
            for privilege in role.privileges:
                identity.provides.add(RoleNeed(privilege.name))
    
    return app


def import_blueprints(app: Flask) -> Flask:
    # Import the blueprints here to avoid circular imports
    from app.rest.auth_rest import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


def create_db(app: Flask) -> None:
    SQL_DB.init_app(app)

    with app.app_context():
        SQL_DB.create_all()

def main():
    app = create_app()
    app.run()