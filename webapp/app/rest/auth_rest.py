from app import SQL_DB
from flask import Blueprint, Response, abort, current_app, request, session
from flask_login import current_user, login_user, logout_user, login_required
from flask_principal import Identity, AnonymousIdentity, identity_changed

from app.repositories import database_repository


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    json_data = request.get_json(silent=True) or {}

    username = json_data.get('username')
    password = json_data.get('password')

    datastore = database_repository.DatabaseRepository(SQL_DB)
    user = datastore.get_user_by_username(username)

    if user is None:
        abort(403)

    if not user.check_password(password):
        abort(403)

    login_user(user)
    # Tell Flask-Principal the identity changed
    identity_changed.send(current_app._get_current_object(),
                            identity=Identity(user.id))

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