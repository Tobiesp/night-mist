from flask import Blueprint, Response, request
from app import LIMITER
from app.models.students_model import Student
from app.models.users_model import student_read_permission, student_write_permission
from app.repositories import database_repository
from app.request_model.student_request import StudentRequest
from app.response_model.student_response import StudentListResponse


student_api = Blueprint('student_api', __name__,url_prefix='/students')


@student_api.route('/', methods=['GET'])
@student_read_permission.require(http_exception=403)
def get_students():
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    students = database.get_all_students()
    return Response(status=200, response=StudentListResponse(students).get_response())


@student_api.route('/<string:student_id>', methods=['GET'])
@student_read_permission.require(http_exception=403)
def get_student(student_id: str):
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    student = database.get_student_by_id(student_id)
    if student is None:
        return Response(status=404)
    return Response(status=200, response=StudentListResponse(student).get_response())


@student_api.route('/', methods=['POST'])
@LIMITER.limit("20 per hour")
@student_write_permission.require(http_exception=403)
def create_student():
    json_data = request.get_json(silent=True) or None
    if json_data is None:
        return Response(status=400, response='Invalid request type')
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    data = StudentRequest(**json_data)
    student = Student()
    student.firstname = data.firstname
    student.lastname = data.lastname
    grade = database.get_grade_by_name(data.grade.grade_name)
    if grade is None:
        return Response(status=400, response='Invalid grade')
    student.grade = grade
    student_group = database.get_group_by_name(data.student_group.group_name)
    if student_group is None:
        return Response(status=400, response='Invalid student group')
    student.student_group = student_group
    student = database.create_student(student)
    return Response(status=200, response=StudentListResponse(student).get_response())


@student_api.route('/<string:student_id>', methods=['PUT'])
@LIMITER.limit("20 per hour")
@student_write_permission.require(http_exception=403)
def update_student(student_id: str):
    json_data = request.get_json(silent=True) or None
    if json_data is None:
        return Response(status=400, response='Invalid request type')
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    data = StudentRequest(**json_data)
    student = Student()
    student.id = student_id
    student.firstname = data.firstname
    student.lastname = data.lastname
    grade = database.get_grade_by_name(data.grade.grade_name)
    if grade is None:
        return Response(status=400, response='Invalid grade')
    student.grade = grade
    student_group = database.get_group_by_name(data.student_group.group_name)
    if student_group is None:
        return Response(status=400, response='Invalid student group')
    student.group = student_group
    student = database.update_student(student)
    return Response(status=200, response=StudentListResponse(student).get_response())


@student_api.route('/<string:student_id>', methods=['DELETE'])
@LIMITER.limit("20 per hour")
@student_write_permission.require(http_exception=403)
def delete_student(student_id: str):
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    student = database.get_student_by_id(student_id)
    if student is None:
        return Response(status=404)
    database.delete_student(student)
    return Response(status=200)


@student_api.route('/query', methods=['GET'])
@student_read_permission.require(http_exception=403)
def query_students():
    request_args = request.args or {}
    filter_value = request_args.get('filter_value') or ''
    page_num = request_args.get('page_num') or 1
    page_size = request_args.get('page_size') or 100
    sort_active = request_args.get('sort_active') or ''
    sort_direction = request_args.get('sort_direction') or ''
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    students = []
    if filter_value == '':
        students = database.get_all_students()
    else:
        students = database.query_students(filter_value)
    if sort_active != '':
        if sort_direction == 'asc':
            students = sorted(students, key=lambda x: getattr(x, sort_active))
        else:
            students = sorted(students, key=lambda x: getattr(x, sort_active), reverse=True)
    start_index = (page_num - 1) * page_size
    end_index = start_index + page_size
    students = students[start_index:end_index]
    return Response(status=200, response=StudentListResponse(students).get_response())


@student_api.route('/count/', methods=['GET'])
@student_read_permission.require(http_exception=403)
def count_students():
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    count = database.get_student_count()
    return Response(status=200, response={'count': count})


@student_api.route('/group/<string:group_id>', methods=['GET'])
@student_read_permission.require(http_exception=403)
def get_students_by_group(group_id: str):
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    students = database.get_students_by_group_id(group_id)
    return Response(status=200, response=StudentListResponse(students).get_response())


@student_api.route('/grade/<string:grade_id>', methods=['GET'])
@student_read_permission.require(http_exception=403)
def get_students_by_grade(grade_id: str):
    database = database_repository.DatabaseRepository.instance().get_student_db_repository()
    students = database.get_students_by_grade_id(grade_id)
    return Response(status=200, response=StudentListResponse(students).get_response())