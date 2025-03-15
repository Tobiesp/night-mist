import unittest
from datetime import datetime, timedelta
from app.models.event_model import Interval, Event, Point
from pydantic import ValidationError

class TestInterval(unittest.TestCase):

    def test_interval_validation(self):
        with self.assertRaises(ValidationError):
            Interval(repeat='invalid')

    def test_interval_to_json(self):
        interval = Interval(repeat='daily', hour=10, minute=30)
        expected_json = '{"repeat": "daily", "hour": 10, "minute": 30}'
        self.assertEqual(interval.to_json(), expected_json)

        interval = Interval(repeat='weekly', week_day=2, hour=10, minute=30)
        expected_json = '{"repeat": "weekly", "week_day": 2, "hour": 10, "minute": 30}'
        self.assertEqual(interval.to_json(), expected_json)

        interval = Interval(repeat='monthly', month_day=10, hour=10, minute=30)
        expected_json = '{"repeat": "monthly", "month_day": 10, "hour": 10, "minute": 30}'
        self.assertEqual(interval.to_json(), expected_json)

    def test_interval_from_json(self):
        interval = Interval().from_json('{"repeat": "daily", "hour": 10, "minute": 30}')
        self.assertEqual(interval.repeat, 'daily')
        self.assertEqual(interval.hour, 10)
        self.assertEqual(interval.minute, 30)

    def test_get_next_date(self):
        interval = Interval(repeat='daily', hour=10, minute=30)
        next_date = interval.get_next_date(datetime.now() - timedelta(days=1))
        excepted_date = datetime(year=datetime.now().year, month=(datetime.now() + timedelta(days=1)).month, day=(datetime.now() + timedelta(days=1)).day, hour=10, minute=30)
        self.assertEqual(next_date.strftime('%Y-%m-%d %H:%M'), excepted_date.strftime('%Y-%m-%d %H:%M'))

        interval = Interval(repeat='weekly', week_day=2, hour=10, minute=30)
        next_date = interval.get_next_date(datetime.now() - timedelta(days=1))
        excepted_date = datetime(year=datetime.now().year, month=(datetime.now() + timedelta(days=1)).month, day=(datetime.now() + timedelta(days=1)).day, hour=10, minute=30)
        while excepted_date.weekday() != 1:
            excepted_date += timedelta(days=1)
        self.assertEqual(next_date.strftime('%Y-%m-%d %H:%M'), excepted_date.strftime('%Y-%m-%d %H:%M'))

        interval = Interval(repeat='monthly', month_day=10, hour=10, minute=30)
        next_date = interval.get_next_date(datetime.now() - timedelta(days=1))
        excepted_date = datetime(year=datetime.now().year, month=(datetime.now() + timedelta(days=1)).month, day=(datetime.now() + timedelta(days=1)).day, hour=10, minute=30)
        while excepted_date.day != 10:
            excepted_date += timedelta(days=1)
        self.assertEqual(next_date.strftime('%Y-%m-%d %H:%M'), excepted_date.strftime('%Y-%m-%d %H:%M'))

    def test_is_event_passed(self):
        interval = Interval(repeat='daily', hour=10, minute=30)
        self.assertTrue(interval.is_event_passed(datetime.now() - timedelta(days=1)))
        self.assertFalse(interval.is_event_passed(datetime.now() + timedelta(days=1)))


class TestEvent(unittest.TestCase):

    def test_event_interval(self):
        event = Event(event_name='Test Event')
        interval = Interval(repeat='daily', hour=10, minute=30)
        event.interval = interval
        self.assertEqual(event.interval.repeat, 'daily')
        self.assertEqual(event.interval.hour, 10)
        self.assertEqual(event.interval.minute, 30)


class TestPoint(unittest.TestCase):

    def test_point_interval(self):
        point = Point(points=10)
        interval = Interval(repeat='daily', hour=10, minute=30)
        point.interval = interval
        self.assertEqual(point.interval.repeat, 'daily')
        self.assertEqual(point.interval.hour, 10)
        self.assertEqual(point.interval.minute, 30)


if __name__ == '__main__':
    unittest.main()