from flask import Blueprint, Response, request
from app.models.users_model import admin_permission
from app.repositories import database_repository
from app.request_model.role_request import RoleRequest
from app.response_model.role_response import RoleListResponse, RoleResponse


role_api = Blueprint('role_api', __name__,url_prefix='/roles')


@role_api.route('/', methods=['GET'])
@admin_permission.require(http_exception=403)
def get_roles():
    database = database_repository.DatabaseRepository.instance().get_admin_db_repository()
    roles = database.get_all_roles()
    return Response(status=200, response=RoleListResponse(roles).get_response())


@role_api.route('/<string:role_id>', methods=['GET'])
@admin_permission.require(http_exception=403)
def get_role(role_id: str):
    database = database_repository.DatabaseRepository.instance().get_admin_db_repository()
    role = database.get_role_by_id(role_id)
    if role is None:
        return Response(status=404)
    return Response(status=200, response=RoleResponse(role).get_response())


@role_api.route('', methods=['POST'])
@admin_permission.require(http_exception=403)
def create_role():
    json_data = request.get_json(silent=True) or {}
    try:
        role_request = RoleRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance().get_admin_db_repository()
    role = database.create_role(role_request.name)
    priviledges = database.get_all_privleges()
    role_priviledges = [p.priviledge_name for p in priviledges]
    for priviledge in priviledges:
        if priviledge.priviledge_name in role_priviledges:
            role.priviledges.append(priviledge)
    database.update_role(role)
    return Response(status=200, response=RoleResponse(role).get_response())


@role_api.route('/<string:role_id>', methods=['PUT'])
@admin_permission.require(http_exception=403)
def update_role(role_id: str):
    json_data = request.get_json(silent=True) or {}
    try:
        role_request = RoleRequest(**json_data)
    except TypeError:
        return Response(status=400, response='Invalid request type')
    except ValueError as ve:
        return Response(status=400, response=str(ve))
    database = database_repository.DatabaseRepository.instance().get_admin_db_repository()
    role = database.get_role_by_id(role_id)
    if role is None:
        return Response(status=404)
    role.role_name = role_request.name
    role.priviledges = []
    priviledges = database.get_all_privleges()
    role_priviledges = [p.name for p in role_request.priviledges]
    for priviledge in priviledges:
        if priviledge.priviledge_name in role_priviledges:
            role.priviledges.append(priviledge)
    database.update_role(role)
    return Response(status=200, response=RoleResponse(role).get_response())


@role_api.route('/<string:role_id>', methods=['DELETE'])
@admin_permission.require(http_exception=403)
def delete_role(role_id: str):
    database = database_repository.DatabaseRepository.instance().get_admin_db_repository()
    role = database.get_role_by_id(role_id)
    if role is None:
        return Response(status=404)
    database.delete_role(role)
    return Response(status=200)


@role_api.route('/query', methods=['GET'])
@admin_permission.require(http_exception=403)
def query_roles():
    request_args = request.args or {}
    filter_value = request_args.get('filter_value') or ''
    page_num = request_args.get('page_num') or 1
    page_size = request_args.get('page_size') or 100
    sort_active = request_args.get('sort_active') or ''
    sort_direction = request_args.get('sort_direction') or ''
    database = database_repository.DatabaseRepository.instance().get_admin_db_repository()
    roles = []
    if filter_value == '':
        roles = database.get_all_roles()
    else:
        roles = database.get_role_by_name(filter_value)
    if sort_active != '':
        if sort_direction == 'asc':
            roles = sorted(roles, key=lambda x: getattr(x, sort_active))
        else:
            roles = sorted(roles, key=lambda x: getattr(x, sort_active), reverse=True)
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    roles = roles[start_index:end_index]
    return Response(status=200, response=RoleListResponse(roles).get_response())


@role_api.route('/count', methods=['GET'])
@admin_permission.require(http_exception=403)
def count_roles():
    database = database_repository.DatabaseRepository.instance().get_admin_db_repository()
    roles = database.get_all_roles()
    return Response(status=200, response=len(roles))