from typing import Optional

from flask import Response, jsonify

from app.models.event_model import PointCategory


class PointCategoryResponse():
    
    def __init__(self, point_category: Optional[PointCategory]):
        self._point_category_ = None
        if point_category is not None:
            self._point_category_ = point_category

    def get_dict(self) -> dict | None:
        if self._point_category_ is None:
            return None
        return {
            'id': self._point_category_.id,
            'category_name': self._point_category_.category_name,
            'description': self._point_category_.description,
        }

    def get_response(self) -> Response:
        d = self.get_dict()
        if d is None:
            return Response(status=404)
        return jsonify(d)
    

class PointCategoryListResponse():
    
    def __init__(self, point_categories: list[PointCategory]):
        self.point_categories = point_categories

    def get_response(self) -> Response:
        return jsonify([PointCategoryResponse(point_category).get_dict() for point_category in self.point_categorie if point_category is not None])