from flask import Blueprint, Response

from app.repositories import database_repository
from app.response_model.priviledge_response import PriviledgeListResponse
from app.models.users_model import admin_permission


admin = Blueprint('admin_api', __name__)


@admin.route('/priviledges', methods=['GET'])
@admin_permission.require(http_exception=403)
def get_priviledges():
    database = database_repository.DatabaseRepository.instance()
    priviledges = database.get_priviledges()
    return Response(status=200, response=PriviledgeListResponse(priviledges).get_response())