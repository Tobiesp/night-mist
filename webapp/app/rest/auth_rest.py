from app import LIMITER, send_email
from flask import Blueprint, Response, abort, current_app, request, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_principal import Identity, AnonymousIdentity, identity_changed

from app.models.users_model import User
from app.repositories import database_repository
from app.request_model.login_request import LoginRequest
from app.request_model.signup_request import SignupRequest
from app.request_model.forgot_password_request import ForgotPasswordRequest


auth_api = Blueprint('auth_api', __name__, static_folder='static', static_url_path='')


@auth_api.route('/index.html')
def index():
    return current_app.send_static_file('index.html')


@auth_api.route('/')
def home():
    return current_app.send_static_file('index.html')
    


@LIMITER.limit("20 per hour")
@auth_api.route('/login', methods=['POST'])
def login():
    json_data = request.get_json(silent=True) or {}

    try:
        login_request = LoginRequest(**json_data)
    except TypeError:
        abort(400)
    except ValueError:
        abort(400)

    datastore = database_repository.DatabaseRepository.instance().get_model_db_repository(User)
    user_list = datastore.get_by_and(username=login_request.username)
    if len(user_list) == 0:
        abort(403)

    user: User = user_list[0]

    if user is None:
        abort(403)

    if not user.is_active:
        abort(403, 'Account Locked. Please contact support')

    if not user.check_password(login_request.password):
        user.add_login_attempt()
        clean_user = user.to_response()
        if 'id' in clean_user:
            del clean_user['id']
        datastore.update(id=str(user.id), **clean_user)
        if user.login_attempts >= 3:
            user.lock_account()
            clean_user = user.to_response()
            if 'id' in clean_user:
                del clean_user['id']
            datastore.update(id=str(user.id), **clean_user)
            return Response(status=403, response='Account Locked. Please contact support')
        abort(403)

    user.reset_login_attempts()
    user.set_login_date()
    clean_user = user.to_response()
    if 'id' in clean_user:
        del clean_user['id']
    print(f'Updating user: {clean_user}')
    datastore.update(id=str(user.id), **clean_user)
    login_user(user)
    # Tell Flask-Principal the identity changed
    identity_changed.send(current_app._get_current_object(),
                            identity=Identity(user.id))

    return user.to_response()

@LIMITER.limit("4 per hour")
@auth_api.route('/signup', methods=['POST'])
def signup():
    json_data = request.get_json(silent=True) or {}

    try:
        signup_request = SignupRequest(**json_data)
    except TypeError as te:
        abort(abort(Response(status=400, response=str(te))))
    except ValueError as ve:
        abort(Response(status=400, response=str(ve)))

    datastore = database_repository.DatabaseRepository.instance().get_model_db_repository(User)
    user_list = datastore.get_by_and(username=signup_request.username)

    if len(user_list) == 0:
        user = User(username=signup_request.username,
                    firstname=signup_request.frist_name,
                    lastname=signup_request.last_name,
                    email=signup_request.email)
        user.role = None
        user.set_password(signup_request.password)
        datastore.create(**user.__dict__)
        send_email('Welcome to Score-Keeper', 'Welcome to Score-Keeper', user.email)
        return Response(status=200)
    else:
        abort(403)


@LIMITER.limit("4 per hour")
@auth_api.route('/forgot-password', methods=['POST'])
def forgot_password():
    json_data = request.get_json(silent=True) or {}

    try:
        forgot_password_request = ForgotPasswordRequest(**json_data)
    except TypeError:
        return Response(status=200)
    except ValueError:
        return Response(status=200)

    datastore = database_repository.DatabaseRepository.instance().get_model_db_repository(User)
    user = datastore.get_by_and(email=forgot_password_request.email)

    if user is None:
        return Response(status=200)

    # TODO: Create speacial link for password reset
    send_email('Password Reset', 'Please reset your password', user.email)
    return Response(status=200)
    

@auth_api.route('/logout')
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


@LIMITER.limit("20 per hour")
@auth_api.route('/current-user')
def get_current_user():
    if current_user.is_authenticated:
        return current_user.to_response()
    else:
        return Response(status=401)