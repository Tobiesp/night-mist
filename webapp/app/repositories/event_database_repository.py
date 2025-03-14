import datetime
import uuid
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

from app.models.event_model import Event, EventInstance, Point, PointCategory
from app.models.point_model import PointEarned, PointSpent
from app.models.students_model import StudentGroup


class EventDatabaseRepository:

    _app_ = None
    _db_ = None

    def __init__(self, app: Flask = None, db: SQLAlchemy = None): 
        self._db_ = db
        self._app_ = app
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self._db_.session.close()

    def get_all_events(self) -> list[Event]:
        with self._app_.app_context():
            return self._db_.session.query(Event).where(Event.deleted is False).all()
        
    def create_event(self, event: Event) -> Event:
        with self._app_.app_context():
            self._db_.session.add(event)
            self._db_.session.commit()
            return event
        
    def get_event_by_id(self, id: str) -> Event:
        uuid_id = uuid.UUID(id)
        with self._app_.app_context():
            return self._db_.session.query(Event).get(uuid_id)
        
    def get_event_by_name(self, name: str) -> Event:
        with self._app_.app_context():
            return self._db_.session.query(Event).filter((Event.event_name == name) | (Event.deleted is False)).first()
        
    def update_event(self, event: Event) -> Event:
        with self._app_.app_context():
            e = self.get_event_by_id(event.id)
            e.event_name = event.event_name
            e.event_interval = event.event_interval
            e.deleted = event.deleted
            e.point_categories = event.point_categories
            e.student_groups = event.student_groups
            self._db_.session.commit()
            return event
        
    def delete_event(self, event: Event) -> None:
        with self._app_.app_context():
            e = self._db_.session.query(Event).filter_by(id=event.id).first()
            e.deleted = True
            self._db_.session.add(e)
            self._db_.session.commit()

    def purge_events(self) -> None:
        with self._app_.app_context():
            events = self._db_.session.query(Event).filter_by(deleted=True).all()
            for event in events:
                self._db_.session.delete(event)
            self._db_.session.commit()

    def get_event_count(self) -> int:
        with self._app_.app_context():
            return self._db_.session.query(func.count(Event.id)).where(Event.deleted is False).scalar()
        
    def get_all_points(self) -> list[Point]:
        with self._app_.app_context():
            return self._db_.session.query(Point).where(Point.deleted is False).all()
        
    def get_point_by_id(self, id: str) -> Point:
        uuid_id = uuid.UUID(id)
        with self._app_.app_context():
            return self._db_.session.query(Point).get(uuid_id)
        
    def get_point_by_point_category_and_student_group(self, point_category: PointCategory, student_group: StudentGroup) -> Point:
        with self._app_.app_context():
            pc_id = point_category.id
            sg_id = student_group.id
            return self._db_.session.query(Point).filter((Point.point_category_id == pc_id) & (Point.student_group_id == sg_id) & (Point.deleted is False)).first()
        
    def create_point(self, point: Point) -> Point:
        with self._app_.app_context():
            self._db_.session.add(point)
            self._db_.session.commit()
            return point
        
    def update_point(self, point: Point) -> Point:
        with self._app_.app_context():
            p = self.get_point_by_id(point.id)
            p.points = point.points
            p.point_category = point.point_category
            p.student_group = point.student_group
            p.interval = point.interval
            self._db_.session.commit()
            return point
        
    def delete_point(self, point: Point) -> None:
        with self._app_.app_context():
            p = self._db_.session.query(Point).filter_by(id=point.id).first()
            p.deleted = True
            self._db_.session.add(p)
            self._db_.session.commit()

    def purge_points(self) -> None:
        with self._app_.app_context():
            points = self._db_.session.query(Point).filter_by(deleted=True).all()
            for point in points:
                self._db_.session.delete(point)
            self._db_.session.commit

    def get_point_count(self) -> int:
        with self._app_.app_context():
            return self._db_.session.query(func.count(Point.id)).filter_by(deleted=False).scalar()
        
    def get_all_point_categories(self) -> list[PointCategory]:
        with self._app_.app_context():
            return self._db_.session.query(PointCategory).filter_by(deleted=False).all()
        
    def get_point_category_by_id(self, id: str) -> PointCategory:
        uuid_id = uuid.UUID(id)
        with self._app_.app_context():
            return self._db_.session.query(PointCategory).get(uuid_id)
        
    def get_point_category_by_name(self, name: str) -> PointCategory:
        with self._app_.app_context():
            return self._db_.session.query(PointCategory).filter((PointCategory.category_name == name) & (PointCategory.deleted is False)).first()
        
    def create_point_category(self, point_category: PointCategory) -> PointCategory:
        with self._app_.app_context():
            self._db_.session.add(point_category)
            self._db_.session.commit()
            return point_category
        
    def update_point_category(self, point_category: PointCategory) -> PointCategory:
        with self._app_.app_context():
            pc = self.get_point_category_by_id(point_category.id)
            pc.category_name = point_category.category_name
            pc.title = point_category.title
            pc.description = point_category.description
            pc.points = point_category.points
            self._db_.session.commit()
            return point_category
        
    def delete_point_category(self, point_category: PointCategory) -> None:
        with self._app_.app_context():
            pc = self._db_.session.query(PointCategory).filter_by(id=point_category.id).first()
            pc.deleted = True
            self._db_.session.add(pc)
            for event in pc.events:
                event.point_categories.remove(pc)
                self._db_.session.add(event)
            for point in pc.points:
                point.deleted = True
                self._db_.session.add(point)
            self._db_.session.commit()

    def purge_point_categories(self) -> None:
        with self._app_.app_context():
            point_categories = self._db_.session.query(PointCategory).filter_by(deleted=True).all()
            for point_category in point_categories:
                self._db_.session.delete(point_category)
            self._db_.session.commit()

    def get_point_category_count(self) -> int:
        with self._app_.app_context():
            return self._db_.session.query(func.count(PointCategory.id)).filter_by(deleted=True).scalar()
        
    def get_all_event_instances(self) -> list[EventInstance]:
        with self._app_.app_context():
            return self._db_.session.query(EventInstance).filter_by(deleted=True).all()
        
    def get_event_instance_by_id(self, id: str) -> EventInstance:
        uuid_id = uuid.UUID(id)
        with self._app_.app_context():
            return self._db_.session.query(EventInstance).get(uuid_id)
        
    def get_event_instances_by_event(self, event: Event) -> list[EventInstance]:
        with self._app_.app_context():
            return self._db_.session.query(EventInstance).filter((EventInstance.event == event) & (EventInstance.deleted is False)).all()
        
    def get_incomplete_event_instances_for_event(self, event: Event) -> list[EventInstance]:
        with self._app_.app_context():
            return self._db_.session.query(EventInstance).filter((EventInstance.event == event) & (EventInstance.completed is False) & (EventInstance.deleted is False)).all()
        
    def start_event_instance_for_event(self, event: Event, event_date: datetime) -> EventInstance:
        with self._app_.app_context():
            ei = EventInstance(event=event)
            ei.event_date = event_date
            self._db_.session.add(ei)
            self._db_.session.commit()
            return ei
        
    def create_event_instance(self, event_instance: EventInstance) -> EventInstance:
        with self._app_.app_context():
            self._db_.session.add(event_instance)
            self._db_.session.commit()
            return event_instance
        
    def update_event_instance(self, event_instance: EventInstance) -> EventInstance:
        with self._app_.app_context():
            ei = self.get_event_instance_by_id(event_instance.id)
            ei.event = event_instance.event
            ei.deleted = event_instance.deleted
            ei.completed = event_instance.completed
            ei.event_date = event_instance.event_date
            self._db_.session.commit()
            return event_instance
        
    def complete_event_instance(self, event_instance: EventInstance) -> EventInstance:
        with self._app_.app_context():
            ei = self.get_event_instance_by_id(event_instance.id)
            ei.completed = True
            self._db_.session.commit()
            return ei
        
    def delete_event_instance(self, event_instance: EventInstance) -> None:
        with self._app_.app_context():
            ei = self._db_.session.query(EventInstance).filter_by(id=event_instance.id).first()
            ei.deleted = True
            self._db_.session.add(ei)
            point_earned = self._db_.session.query(PointEarned).filter_by(event_instance_id=event_instance.id).all()
            for pe in point_earned:
                pe.deleted = True
                self._db_.session.add(pe)
            point_spent = self._db_.session.query(PointSpent).filter_by(event_instance_id=event_instance.id).all()
            for ps in point_spent:
                ps.deleted = True
                self._db_.session.add(ps)
            self._db_.session.commit()

    def purge_event_instances(self) -> None:
        with self._app_.app_context():
            event_instances = self._db_.session.query(EventInstance).filter_by(deleted=True).all()
            for event_instance in event_instances:
                self._db_.session.delete(event_instance)
            self._db_.session.commit()

    def get_event_instance_count_by_event(self, event_id: str) -> int:
        with self._app_.app_context():
            event = self.get_event_by_id(event_id)
            return self._db_.session.query(func.count(EventInstance.id)).filter((EventInstance.event == event) & (EventInstance.deleted is False)).scalar()

    def get_event_instance_count(self) -> int:
        with self._app_.app_context():
            return self._db_.session.query(func.count(EventInstance.id)).filter_by(deleted=True).scalar()

    def get_latest_event_instance(self, event: Event) -> EventInstance:
        with self._app_.app_context():
            return self._db_.session.query(EventInstance).filter((EventInstance.event == event) & (EventInstance.deleted is False)).order_by(EventInstance.event_date.desc()).first()
