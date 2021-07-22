
class Point:
    """
    Is immutable.
    """

    def __init__(self, x: float, y: float):
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def __str__(self):
        return """
        Point: 
             hashable id:\t{2}
             x coord:\t{0}
             y coord:\t{1}
        """.format(self.x, self.y, self.__hash__())

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        if isinstance(other, Point):
            if self.x == other.x and self.y == other.y:
                return True
        return False

    """def __lt__(self, other):
        if isinstance(other, Point):
            if self.x < other.x:
                return self
        else:
            # excepcion
            return None
    """

    @staticmethod
    def get_distance_between_2_points(point1, point2):
        """
        sqrt( (x_i-x_j)² + (y_i-y_j)²)

        cython?
        """
        return float(((point2.x - point1.x)**2 + (point2.y - point1.y)**2)**(1/2))


def order_points(given_point):
    return given_point.x


aux = [Point(1.0, 3.0), Point(0.0, 30.0), Point(10.0, 4.0), Point(5.0, 2.0)]
for p in aux:
    print(p)
aux.sort(key=order_points)
print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
for p in aux:
    print(p)
