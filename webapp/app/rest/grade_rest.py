from flask import Blueprint, Response, request
from app import LIMITER
from app.models.students_model import Grade
from app.models.users_model import student_read_permission, admin_permission
from app.repositories import database_repository
from app.request_model.grade_request import GradeRequest
from app.response_model.grade_response import GradeListResponse


grade_api = Blueprint('grade_api', __name__,url_prefix='/grades')


@grade_api.route('/', methods=['GET'])
@student_read_permission.require(http_exception=403)
def get_grades():
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    grades = database.get_all_grades()
    return Response(status=200, response=GradeListResponse(grades).get_response())


@grade_api.route('/<string:grade_id>', methods=['GET'])
@student_read_permission.require(http_exception=403)
def get_grade(grade_id: str):
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    grade = database.get_grade_by_id(grade_id)
    if grade is None:
        return Response(status=404)
    return Response(status=200, response=GradeListResponse(grade).get_response())


@grade_api.route('/', methods=['POST'])
@LIMITER.limit("20 per hour")
@admin_permission.require(http_exception=403)
def create_grade():
    json_data = request.get_json(silent=True) or None
    if json_data is None:
        return Response(status=400, response='Invalid request type')
    data = GradeRequest(**json_data)
    grade = Grade(**data)
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    grade = database.create_grade(grade)
    return Response(status=200, response=GradeListResponse(grade).get_response())


@grade_api.route('/<string:grade_id>', methods=['PUT'])
@LIMITER.limit("20 per hour")
@admin_permission.require(http_exception=403)
def update_grade(grade_id: str):
    json_data = request.get_json(silent=True) or None
    if json_data is None:
        return Response(status=400, response='Invalid request type')
    data = GradeRequest(**json_data)
    grade = Grade(grade_name=data.grade_name)
    grade.id = grade_id
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    grade = database.update_grade(grade)
    return Response(status=200, response=GradeListResponse(grade).get_response())


@grade_api.route('/<string:grade_id>', methods=['DELETE'])
@LIMITER.limit("20 per hour")
@admin_permission.require(http_exception=403)
def delete_grade(grade_id: str):
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    grade = database.get_grade_by_id(grade_id)
    if grade is None:
        return Response(status=404)
    database.delete_grade(grade)
    return Response(status=200)




