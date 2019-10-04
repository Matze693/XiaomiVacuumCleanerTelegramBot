import logging

from utility.point import Point


class Rectangle(object):
    """
    Simple class to store rectangle coordinates.
    """

    def __init__(self, first: Point, second: Point) -> None:
        """
        Initialize an object of class Rectangle.

        :param first: First point.
        :param second: Second point.
        """
        if first.x == second.x:
            message = 'X coordinates of points {}, {} identical for rectangle'.format(first, second)
            logging.error(message)
            raise ValueError(message)

        if first.y == second.y:
            message = 'Y coordinates of points {}, {} identical for rectangle'.format(first, second)
            logging.error(message)
            raise ValueError(message)

        self.bottom_left = Point(min(first.x, second.x), min(first.y, second.y))
        self.top_right = Point(max(first.x, second.x), max(first.y, second.y))

    def __str__(self) -> str:
        return '[{}, {}]'.format(self.bottom_left, self.top_right)
