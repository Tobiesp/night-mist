from typing import Optional

from flask import Response, jsonify

from app.models.users_model import Priviledge


class PriviledgeResponse():

    def __init__(self, priviledge: Optional[Priviledge]):
        self._priviledge_ = None
        if priviledge is not None:
            self._priviledge_ = priviledge

    def get_dict(self) -> dict | None:
        if self._priviledge_ is None:
            return None
        return {
            'id': self._priviledge_.id,
            'name': self._priviledge_.priviledge_name
        }

    def get_response(self) -> Response:
        d = self.get_dict()
        if d is None:
            return Response(status=404)
        return jsonify(d)
    

class PriviledgeListResponse():

    def __init__(self, priviledges: list[Priviledge]):
        self.priviledges = priviledges

    def get_response(self) -> Response:
        return jsonify([PriviledgeResponse(priviledge).get_dict() for priviledge in self.priviledges if priviledge is not None])