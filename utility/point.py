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

    def __str__(self) -> str:
        return '(x: {}, y: {})'.format(self.x, self.y)
