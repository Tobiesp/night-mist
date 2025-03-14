from flask import Blueprint
from flask_login import login_required

from app.repositories import database_repository
from app.response_model.priviledge_response import PriviledgeListResponse
from app.models.users_model import admin_permission


admin_api = Blueprint('admin_api', __name__)


@admin_api.route('/priviledges', methods=['GET'])
@login_required
@admin_permission.require(http_exception=403)
def get_priviledges():
    database = database_repository.DatabaseRepository.instance().get_admin_db_repository()
    priviledges = database.get_priviledges()
    return PriviledgeListResponse(priviledges).get_response()