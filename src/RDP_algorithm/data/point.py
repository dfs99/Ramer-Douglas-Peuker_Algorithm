
class Point:

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
        return """Point - {2} [ x:\t{0}; y:\t{1} ]""".format(self.x, self.y, self.__hash__())

    def __hash__(self):
        return id(self)

    @staticmethod
    def get_distance_between_2_points(point1, point2):
        return float(((point2.x - point1.x)**2 + (point2.y - point1.y)**2)**(1/2))
