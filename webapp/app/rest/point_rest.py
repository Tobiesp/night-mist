from app.models.event_model import Point
from app.models.point_model import PointEarned, PointSpent, RunningTotal
from app.models.users_model import event_read_permission, event_write_permission, admin_permission, student_read_permission
from app.request_model.point_earned_request import PointEarnedRequest
from app.request_model.point_request import PointRequest
from app.request_model.point_spent_request import PointSpentRequest
from app.request_model.query_request import QueryRequest
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


class RunningTotalRestAPI(GenericRestAPI[RunningTotal]):
    def __init__(self):
        super().__init__(
            RunningTotal,
            'points/running-totals',
            RunningTotalRequest,
            student_read_permission,
            admin_permission,
            admin_permission,
            admin_permission)
