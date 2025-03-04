from flask import Blueprint, Response, request
from app import LIMITER
from app.models.students_model import Grade, StudentGroup
from app.models.users_model import student_read_permission, admin_permission
from app.repositories import database_repository
from app.request_model.student_group_request import StudentGroupRequest
from app.response_model.student_group_response import StudentGroupListResponse


student_group_api = Blueprint('student_group_api', __name__,url_prefix='/student_groups')


@student_group_api.route('/', methods=['GET'])
@student_read_permission.require(http_exception=403)
def get_student_groups():
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    student_groups = database.get_all_groups()
    return Response(status=200, response=StudentGroupListResponse(student_groups).get_response())


@student_group_api.route('/<string:student_group_id>', methods=['GET'])
@student_read_permission.require(http_exception=403)
def get_student_group(student_group_id: str):
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    student_group = database.get_group_by_id(student_group_id)
    if student_group is None:
        return Response(status=404)
    return Response(status=200, response=StudentGroupListResponse(student_group).get_response())


@student_group_api.route('/', methods=['POST'])
@LIMITER.limit("20 per hour")
@admin_permission.require(http_exception=403)
def create_student_group():
    json_data = request.get_json(silent=True) or None
    if json_data is None:
        return Response(status=400, response='Invalid request type')
    data = StudentGroupRequest(**json_data)
    student_group = StudentGroup(**data)
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    student_group = database.create_group(student_group)
    return Response(status=200, response=StudentGroupListResponse(student_group).get_response())


@student_group_api.route('/<string:student_group_id>', methods=['PUT'])
@LIMITER.limit("20 per hour")
@admin_permission.require(http_exception=403)
def update_student_group(student_group_id: str):
    json_data = request.get_json(silent=True) or None
    if json_data is None:
        return Response(status=400, response='Invalid request type')
    data = StudentGroupRequest(**json_data)
    student_group = StudentGroup(data.group_name, grades=[Grade(**g) for g in data.grades])
    student_group.id = student_group_id
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    student_group = database.update_group(student_group)
    return Response(status=200, response=StudentGroupListResponse(student_group).get_response())


@student_group_api.route('/<string:student_group_id>', methods=['DELETE'])
@LIMITER.limit("20 per hour")
@admin_permission.require(http_exception=403)
def delete_student_group(student_group_id: str):
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    database.delete_group(student_group_id)
    return Response(status=200)
