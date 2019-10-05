from unittest import TestCase
from unittest.mock import Mock

from miio import DeviceException

from utility.point import Point
from utility.rectangle import Rectangle
from xvc.cleaning_zone import CleaningZone, Door, Room, Area
from xvc.fan_level import FanLevel
from xvc.vacuum_wrapper import VacuumWrapper


class __PointTest(TestCase):

    def test_init(self):
        x, y = 1, 2
        point = Point(x, y)
        self.assertEqual(x, point.x)
        self.assertEqual(y, point.y)

    def test_str(self):
        point = Point(1, 2)
        self.assertEqual('(x: 1, y: 2)', str(point))


class __RectangleTest(TestCase):

    def test_init(self):
        first, second = Point(3, 2), Point(1, 4)
        rectangle = Rectangle(first, second)
        self.assertEqual(rectangle.bottom_left.x, 1)
        self.assertEqual(rectangle.bottom_left.y, 2)
        self.assertEqual(rectangle.top_right.x, 3)
        self.assertEqual(rectangle.top_right.y, 4)

        self.assertRaises(ValueError, lambda: Rectangle(Point(1, 2), Point(1, 3)))
        self.assertRaises(ValueError, lambda: Rectangle(Point(1, 2), Point(2, 2)))

    def test_str(self):
        rectangle = Rectangle(Point(1, 2), Point(3, 4))
        self.assertEqual('[(x: 1, y: 2), (x: 3, y: 4)]', str(rectangle))


class __CleaningZoneTest(TestCase):

    def test_init(self):
        rectangle = Rectangle(Point(1, 2), Point(3, 4))
        zone = CleaningZone(rectangle, 10)
        self.assertEqual(rectangle, zone.rectangle)
        self.assertEqual(10, zone.iterations)
        self.assertEqual(FanLevel.Balanced, zone.fan_level)

    def test_str(self):
        zone = CleaningZone(Rectangle(Point(1, 2), Point(3, 4)))
        self.assertEqual('{[(x: 1, y: 2), (x: 3, y: 4)] x 1 at FanLevel.Balanced}', str(zone))

    def test_get_list(self):
        zone = CleaningZone(Rectangle(Point(1, 2), Point(3, 4)))
        self.assertEqual([1, 2, 3, 4, 1], zone.get_list())


class __DoorTest(TestCase):

    def test_init(self):
        door = Door(Rectangle(Point(1, 2), Point(3, 4)))
        self.assertEqual(1, door.iterations)
        self.assertEqual(FanLevel.Quiet, door.fan_level)


class __RoomTest(TestCase):

    def test_init(self):
        door = Room(Rectangle(Point(1, 2), Point(3, 4)), 2)
        self.assertEqual(2, door.iterations)
        self.assertEqual(FanLevel.Balanced, door.fan_level)


class __AreaTest(TestCase):

    def test_init(self):
        door = Area(Rectangle(Point(1, 2), Point(3, 4)), 3)
        self.assertEqual(3, door.iterations)
        self.assertEqual(FanLevel.Balanced, door.fan_level)


class __VacuumWrapperTest(TestCase):

    def test_init(self):
        vacuum = Mock()
        vacuum.do_discover = Mock(side_effect=DeviceException())
        self.assertRaises(ConnectionError, lambda: VacuumWrapper(vacuum))
