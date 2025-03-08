from typing import Optional

from app.models.event_model import PointCategory


class PointCategoryResponse():
    
    def __init__(self, point_category: Optional[PointCategory]):
        self._point_category_ = None
        if point_category is not None:
            self._point_category_ = point_category

    def get_response(self) -> dict | None:
        if self._point_category_ is None:
            return None
        return {
            'id': self._point_category_.id,
            'category_name': self._point_category_.category_name,
            'description': self._point_category_.description,
        }
    

class PointCategoryListResponse():
    
    def __init__(self, point_categories: list[PointCategory]):
        self.point_categories = point_categories

    def get_response(self) -> list[dict]:
        return [PointCategoryResponse(point_category).get_response() for point_category in self.point_categories]