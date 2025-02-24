from app import send_email
from flask import Blueprint, Response, abort, current_app, request, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_principal import Identity, AnonymousIdentity, identity_changed

from app.models.users_model import User
from app.repositories import database_repository
from app.request_model.login_request import LoginRequest
from app.request_model.signup_request import SignupRequest
from app.request_model.forgot_password_request import ForgotPasswordRequest


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    json_data = request.get_json(silent=True) or {}

    try:
        login_request = LoginRequest(**json_data)
    except TypeError:
        abort(400)
    except ValueError:
        abort(403)

    datastore = database_repository.DatabaseRepository(None)
    user = datastore.get_user_by_username(login_request.username)

    if user is None:
        abort(403)

    if not user.check_password(login_request.password):
        abort(403)

    login_user(user)
    # Tell Flask-Principal the identity changed
    identity_changed.send(current_app._get_current_object(),
                            identity=Identity(user.id))

    return Response(status=200)


@auth.route('/signup', methods=['POST'])
def signup():
    json_data = request.get_json(silent=True) or {}

    try:
        signup_request = SignupRequest(**json_data)
    except TypeError as te:
        abort(abort(Response(status=400, response=str(te))))
    except ValueError as ve:
        abort(Response(status=400, response=str(ve)))

    datastore = database_repository.DatabaseRepository(None)
    user = datastore.get_user_by_username(signup_request.username)

    if user is not None:
        user = User(username=signup_request.username,
                    firstname=signup_request.firstname,
                    lastname=signup_request.lastname,
                    email=signup_request.email)
        user.role = None
        user.set_password(signup_request.password)
        datastore.create_user(user)
        send_email('Welcome to Score-Keeper', 'Welcome to Score-Keeper', user.email)
        return Response(status=200)
    else:
        abort(403)


@auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    json_data = request.get_json(silent=True) or {}

    try:
        forgot_password_request = ForgotPasswordRequest(**json_data)
    except TypeError:
        return Response(status=200)
    except ValueError:
        return Response(status=200)

    datastore = database_repository.DatabaseRepository(None)
    user = datastore.get_user_by_email(forgot_password_request.email)

    if user is None:
        return Response(status=200)

    # TODO: Create speacial link for password reset
    send_email('Password Reset', 'Please reset your password', user.email)
    return Response(status=200)
    

@auth.route('/logout')
@login_required
def logout():
    if not current_user.is_authenticated:
        return Response(status=200)
    # Remove the user information from the session
    logout_user()

    # Remove session keys set by Flask-Principal
    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)

    # Tell Flask-Principal the user is anonymous
    identity_changed.send(current_app._get_current_object(),
                          identity=AnonymousIdentity())

    return Response(status=200)