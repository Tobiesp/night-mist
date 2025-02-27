from typing import Optional

from app.models.users_model import Priviledge


class PriviledgeResponse():

    def __init__(self, priviledge: Optional[Priviledge]):
        if priviledge is not None:
            self.name = priviledge.priviledge_name
            self.id = priviledge.id

    def get_response(self) -> dict:
        return {
            'id': self.id,
            'name': self.name
        }
    

class PriviledgeListResponse():

    def __init__(self, priviledges: list[Priviledge]):
        self.priviledges = priviledges

    def get_response(self) -> list[dict]:
        return [PriviledgeResponse(priviledge).get_response() for priviledge in self.priviledges]