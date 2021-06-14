import numpy as np
from line import Line


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

    @classmethod
    def get_intersection_point(cls, line1: Line, line2: Line):
        """
        Through solving a system of linear equations with numpy
        the intersection point is obtained.
            AX = B
        where:
            A,X,B are matrices fulfilled with the general equation terms.
        """
        fetch_a_matrix = [
            [line1.general_equation[0], line1.general_equation[1]],
            [line2.general_equation[0], line2.general_equation[1]]
        ]
        fetch_b_matrix = [
            [-line1.general_equation[2]],
            [-line2.general_equation[2]]
        ]

        a = np.array(fetch_a_matrix)
        b = np.array(fetch_b_matrix)
        x = np.linalg.inv(a).dot(b)

        # x is a vector [x, y] that contains the values like that.
        return cls(x[0],
                   x[1])
