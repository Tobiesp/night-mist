from flask import Response
from app.models.event_model import Point
from app.models.point_model import PointEarned, PointSpent, RunningTotal
from app.models.students_model import Student
from app.models.users_model import event_read_permission, event_write_permission, admin_permission, student_read_permission
from app.repositories import database_repository
from app.request_model.point_earned_request import PointEarnedRequest
from app.request_model.point_request import PointRequest
from app.request_model.point_spent_request import PointSpentRequest
from app.request_model.running_total_request import RunningTotalRequest
from app.rest.generic_rest_api import GenericRestAPI


class PointRestAPI(GenericRestAPI[Point]):
    def __init__(self):
        super().__init__(
            Point,
            'points',
            PointRequest,
            event_read_permission,
            event_write_permission,
            event_write_permission,
            admin_permission)


class PointEarnedRestAPI(GenericRestAPI[PointEarned]):
    def __init__(self):
        super().__init__(
            PointEarned,
            'points/earned',
            PointEarnedRequest,
            event_read_permission,
            event_write_permission,
            event_write_permission,
            admin_permission)
        
    def create(self):
        with self._write_permissions_.require(http_exception=403):
            response, status_code = super().create()
            if status_code != 201:
                return response
            student = None
            if 'student' in response:
                student = response['student']['id']
            if student is not None:
                student_db = database_repository.DatabaseRepository.instance().get_model_db_repository(Student)
                student = student_db.get_by_id(student)
                if student is not None:
                    runningTotal_db = database_repository.DatabaseRepository.instance().get_model_db_repository(RunningTotal)
                    runningTotal = runningTotal_db.get_by_first(student=student)
                    if runningTotal is None:
                        runningTotal.total_points += response['point']['points']
                        clean_total = runningTotal.to_response()
                        if 'id' in clean_total:
                            del clean_total['id']
                        runningTotal_db.update(str(runningTotal.id), **clean_total.__dict__)
                    else:
                        runningTotal = RunningTotal(student=student, total_points=response['point']['points'])
                        runningTotal_db.create(**runningTotal.__dict__)
            return response
        
    def update(self, id):
        prev_point = self._db_.get_by_id(id)
        item = super().update(id)
        if isinstance(item, Response):
            return item
        point = self._db_.get_by_id(id)
        if point is None:
            return item
        student_db = database_repository.DatabaseRepository.instance().get_model_db_repository(Student)
        student = student_db.get_by_id(point.student.id)
        if student is not None:
            runningTotal_db = database_repository.DatabaseRepository.instance().get_model_db_repository(RunningTotal)
            runningTotal = runningTotal_db.get_by_first(student=student)
            if runningTotal is not None:
                runningTotal.total_points -= prev_point.point.points
                runningTotal.total_points += point.point.points
                clean_total = runningTotal.to_response()
                if 'id' in clean_total:
                    del clean_total['id']
                runningTotal_db.update(str(runningTotal.id), **clean_total.__dict__)
        return item
        
    def delete(self, id: str):
        with self._delete_permissions_.require(http_exception=403):
            response = super().delete(id)
            point_earned = self._db_.get_by_id(id)
            if point_earned is None:
                return Response(status=404)
            student_db = database_repository.DatabaseRepository.instance().get_model_db_repository(Student)
            student = student_db.get_by_id(point_earned.student.id)
            if student is not None:
                runningTotal_db = database_repository.DatabaseRepository.instance().get_model_db_repository(RunningTotal)
                runningTotal = runningTotal_db.get_by_first(student=student)
                if runningTotal is not None:
                    runningTotal.total_points -= point_earned.point.points
                    clean_total = runningTotal.to_response()
                    if 'id' in clean_total:
                        del clean_total['id']
                    runningTotal_db.update(str(runningTotal.id), **clean_total.__dict__)
            return response


class PointSpentRestAPI(GenericRestAPI[PointSpent]):
    def __init__(self):
        super().__init__(
            PointSpent,
            'points/spent',
            PointSpentRequest,
            event_read_permission,
            event_write_permission,
            event_write_permission,
            admin_permission)
        
    def create(self):
        with self._write_permissions_.require(http_exception=403):
            response, status_code = super().create()
            if status_code != 201:
                return response
            student = None
            if 'student' in response:
                student = response['student']['id']
            if student is not None:
                student_db = database_repository.DatabaseRepository.instance().get_model_db_repository(Student)
                student = student_db.get_by_id(student)
                if student is not None:
                    runningTotal_db = database_repository.DatabaseRepository.instance().get_model_db_repository(RunningTotal)
                    runningTotal = runningTotal_db.get_by_first(student=student)
                    if runningTotal is not None:
                        runningTotal.total_points -= response['points']
                        clean_total = runningTotal.to_response()
                        if 'id' in clean_total:
                            del clean_total['id']
                        runningTotal_db.update(str(runningTotal.id), **clean_total.__dict__)
            return response
        
    def update(self, id):
        prev_point = self._db_.get_by_id(id)
        item = super().update(id)
        if isinstance(item, Response):
            return item
        point = self._db_.get_by_id(id)
        if point is None:
            return item
        student_db = database_repository.DatabaseRepository.instance().get_model_db_repository(Student)
        student = student_db.get_by_id(point.student.id)
        if student is not None:
            runningTotal_db = database_repository.DatabaseRepository.instance().get_model_db_repository(RunningTotal)
            runningTotal = runningTotal_db.get_by_first(student=student)
            if runningTotal is not None:
                runningTotal.total_points += prev_point.points
                runningTotal.total_points -= point.points
                clean_total = runningTotal.to_response()
                if 'id' in clean_total:
                    del clean_total['id']
                runningTotal_db.update(str(runningTotal.id), **clean_total.__dict__)
        return item

    def delete(self, id: str):
        with self._delete_permissions_.require(http_exception=403):
            response = super().delete(id)
            point_spent = self._db_.get_by_id(id)
            if point_spent is None:
                return Response(status=404)
            student_db = database_repository.DatabaseRepository.instance().get_model_db_repository(Student)
            student = student_db.get_by_id(point_spent.student.id)
            if student is not None:
                runningTotal_db = database_repository.DatabaseRepository.instance().get_model_db_repository(RunningTotal)
                runningTotal = runningTotal_db.get_by_first(student=student)
                if runningTotal is not None:
                    runningTotal.total_points += point_spent.points
                    clean_total = runningTotal.to_response()
                    if 'id' in clean_total:
                        del clean_total['id']
                    runningTotal_db.update(str(runningTotal.id), **clean_total.__dict__)
            return response


class RunningTotalRestAPI(GenericRestAPI[RunningTotal]):
    def __init__(self):
        super().__init__(
            RunningTotal,
            'points/running-totals',
            RunningTotalRequest,
            student_read_permission,
            None,
            None,
            None)
