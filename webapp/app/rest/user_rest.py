from flask import Blueprint, Response, request
from app.models.users_model import admin_permission
from app.repositories import database_repository
from app.request_model.user_request import UserRequest
from app.response_model.user_response import UserListResponse, UserResponse


user_api = Blueprint('user_api', __name__)


@user_api.route('/users', methods=['GET'])
@admin_permission.require(http_exception=403)
def get_users():
    database = database_repository.DatabaseRepository.instance()
    users = database.get_all_users()
    return Response(status=200, response=UserListResponse(users).get_response())


@user_api.route('/users/<string:user_id>', methods=['GET'])
@admin_permission.require(http_exception=403)
def get_user(user_id: str):
    database = database_repository.DatabaseRepository.instance()
    user = database.get_user_by_id(user_id)
    if user is None:
        return Response(status=404)
    return Response(status=200, response=UserResponse(user).get_response())


@user_api.route('/users', methods=['POST'])
@admin_permission.require(http_exception=403)
def create_user():
    json_data = request.get_json(silent=True) or {}
    try:
        user_request = UserRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance()
    user = database.create_user(user_request.username, user_request.password, user_request.firstname,
                                 user_request.lastname, user_request.email, user_request.role)
    return Response(status=200, response=UserResponse(user).get_response())


@user_api.route('/users/<string:user_id>', methods=['PUT'])
@admin_permission.require(http_exception=403)
def update_user(user_id: str):
    json_data = request.get_json(silent=True) or {}
    try:
        user_request = UserRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance()
    user = database.get_user_by_id(user_id)
    if user is None:
        return Response(status=404)
    user.username = user_request.username
    user.firstname = user_request.firstname
    user.lastname = user_request.lastname
    user.email = user_request.email
    user.role = user_request.role
    database.update_user(user)
    return Response(status=200, response=UserResponse(user).get_response())


@user_api.route('/users/<string:user_id>', methods=['DELETE'])
@admin_permission.require(http_exception=403)
def delete_user(user_id: str):
    database = database_repository.DatabaseRepository.instance()
    user = database.get_user_by_id(user_id)
    if user is None:
        return Response(status=404)
    database.delete_user(user)
    return Response(status=200)
    