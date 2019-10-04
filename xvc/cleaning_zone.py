from typing import List

from utility.rectangle import Rectangle
from xvc.fan_level import FanLevel


class CleaningZone(object):
    """
    Class to handle information about a cleaning zone.
    """

    def __init__(self,
                 rectangle: Rectangle,
                 iterations: int = 1,
                 fan_level: FanLevel = FanLevel.Balanced) -> None:
        """
        Initialize an object of class Point.

        :param rectangle: Rectangle dimensions.
        :param iterations: Cleaning iterations.
        :param fan_level: Fan level.
        """
        self.rectangle = rectangle
        self.iterations = iterations
        self.fan_level = fan_level

    def __str__(self) -> str:
        return '{{{} x {} at {}}}'.format(self.rectangle, self.iterations, self.fan_level)

    def get_list(self) -> List[int]:
        return [self.rectangle.bottom_left.x,
                self.rectangle.bottom_left.y,
                self.rectangle.top_right.x,
                self.rectangle.top_right.y,
                self.iterations]


class Door(CleaningZone):
    """
    Class to represent a door for zone cleaning.
    """

    def __init__(self, rectangle: Rectangle) -> None:
        """
        Initialize an object of class Door.

        :param rectangle: Door dimensions.
        """
        super().__init__(rectangle, 1, FanLevel.Quiet)


class Room(CleaningZone):
    """
    Marker class to represent a room for zone cleaning.
    """
    pass


class Area(CleaningZone):
    """
    Marker class to represent a area for zone cleaning.
    """
    pass
