from src.exceptions.point_exception import PointException


class Point:
    """
    Point class is expected to be an immutable class.
    Monkey Patching does not work within the Point class.
    Thus, an Exception will be thrown if someone wants
    to add dynamically another attribute.
    In order to achieve this, Python __slots__ have been
    used. This will save memory space and will speed the
    access to attributes. [According to official documentation]

    Furthermore, in order to perform operations with sets,
    the class is also hashable, this means that two Point
    instances cannot contain the same coordinates because
    the objects will be treated as two identical objects.
    """

    __slots__ = '_x', '_y'

    def __init__(self, x, y):
        super(Point, self).__setattr__('_x', Point.__validate_coord(x))
        super(Point, self).__setattr__('_y', Point.__validate_coord(y))

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __str__(self):
        return """
        Point: 
             hashable id:\t{2}
             x coord:\t{0}
             y coord:\t{1}""".format(self.x, self.y, self.__hash__())

    def __hash__(self):
        data_block = str(self.x) + str(self.y)
        return hash(data_block)

    def __eq__(self, other):
        if isinstance(other, Point):
            if self.x == other.x and self.y == other.y:
                return True
        return False

    def __setattr__(self, key, value):
        raise PointException("Immutable Object Error: Point class cannot have more attributes nor change their values.")

    @staticmethod
    def get_distance_between_2_points(point1, point2):
        """
        sqrt( (x_i-x_j)² + (y_i-y_j)²)
        check it with cython to speed up.
        """
        return float((abs(point2.x - point1.x) ** 2 + abs(point2.y - point1.y) ** 2) ** (1 / 2))

    @staticmethod
    def __validate_coord(coord):
        if isinstance(coord, float):
            return coord
        raise PointException('Error: Point coordinates must be floats.')

    @classmethod
    def order_points_x_coord(cls, given_point):
        return given_point.x

    @classmethod
    def order_points_y_coord(cls, given_point):
        return given_point.y
