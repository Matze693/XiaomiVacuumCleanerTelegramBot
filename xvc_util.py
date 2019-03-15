from abc import abstractmethod, ABCMeta
from typing import List


class Point(object):
    """
    Simple class to store x and y coordinates.
    """

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize an object of class Point.

        :param x: Value of x coordinate.
        :param y: Value of y coordinate.
        """
        self.x = x
        self.y = y

    def get_list(self) -> List[int]:
        """
        Returns a list with essential data.

        :return: List with essential data.
        """
        return [self.x, self.y]

    def __str__(self) -> str:
        return '({}, {})'.format(self.x, self.y)


class XVCListable(metaclass=ABCMeta):
    """
    Abstract class to provide function to generate compatible list for zone cleaning.
    """

    @abstractmethod
    def get_list(self) -> List[int]:
        """
        Returns a list with essential data.

        :return: List with essential data.
        """
        raise NotImplementedError()


class Rectangle(XVCListable, metaclass=ABCMeta):
    """
    Abstract class to store coordinates of an rectangle.
    """

    def __init__(self, bottom_left: Point, top_right: Point, name: str = None) -> None:
        """
        Initialize an object of class Rectangle.

        :param bottom_left: Bottom left point.
        :param top_right: Top right point.
        :param name: Name of rectangle, default is None.
        """
        self.bottom_left = bottom_left
        self.top_right = top_right
        self.name = name

    def get_list(self) -> List[int]:
        """
        Returns a list with essential data.

        :return: List with essential data.
        """
        return self.bottom_left.get_list() + self.top_right.get_list()

    def __str__(self) -> str:
        string_builder = '{}: {{'.format(self.__class__.__name__)
        if self.name is not None:
            string_builder += '{}: '.format(self.name)
        string_builder += '[{}, {}]}}'.format(self.bottom_left, self.top_right)
        return string_builder


class Door(Rectangle):
    """
    Class to represent a door for zone cleaning.
    """

    def __init__(self, bottom_left: Point, top_right: Point, name: str) -> None:
        """
        Initialize an object of class Door.

        :param bottom_left: Bottom left point.
        :param top_right: Top right point.
        :param name: Name of rectangle.
        """
        super().__init__(bottom_left, top_right, name)

    def get_list(self) -> List[int]:
        """
        Returns a list with essential data.

        :return: List with essential data.
        """
        return self.bottom_left.get_list() + self.top_right.get_list() + [1]


class Room(Rectangle):
    """
    Class to represent a room for zone cleaning.
    """

    def __init__(self, bottom_left: Point, top_right: Point, name: str, number: int = 1) -> None:
        """
        Initialize an object of class Rectangle.

        :param bottom_left: Bottom left point.
        :param top_right: Top right point.
        :param name: Name of rectangle.
        :param number: Number of cleaning cycles.
        """
        super().__init__(bottom_left, top_right, name)
        self.number = number

    def get_list(self) -> List[int]:
        """
        Returns a list with essential data.

        :return: List with essential data.
        """
        return self.bottom_left.get_list() + self.top_right.get_list() + [self.number]


class Area(Room):
    """
    Class to represent a area for zone cleaning.
    """
    pass
