import numpy as np
from src.data.point import Point


class Line2:
    LINE_TYPES = ["VERTICAL", "HORIZONTAL", "NON-VERTICAL"]
    def __init__(self, point1, point2):
        self.__point1 = point1
        self.__point2 = point2
        self.__type = self.__set_type()
        self.__gradient = self.__set_gradient()
        self.__general_equation = self.__set_general_equation()

    @property
    def point1(self):
        return self.__point1
    @property
    def point2(self):
        return self.__point2
    @property
    def type(self):
        return self.__type
    @property
    def gradient(self):
        return self.__gradient

    def __set_type(self):
        if self.point1.x - self.point2.x == 0:
            return Line2.LINE_TYPES[1]
        elif self.point1.y - self.point2.y == 0:
            return Line2.LINE_TYPES[0]
        else:
            return Line2.LINE_TYPES[2]

    def __set_gradient(self):
        if self.type == Line2.LINE_TYPES[2]:
            return (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)
        else:
            return None

    def __set_general_equation(self):
        general_expression = []
        # [a,b,c]
        # vertical
        if self.type == Line2.LINE_TYPES[0]:
            general_expression = [float(1), None, -self.point1.x]
        # horizontal
        elif self.type == Line2.LINE_TYPES[1]:
            general_expression = [None, float(1), -self.point1.y]
        # non-vertical
        elif self.type == Line2.LINE_TYPES[2]:
            # calculate the gradient.
            general_expression = [self.gradient, float(-1), -(self.gradient * self.point1.x) + self.point1.y]
        return general_expression

# =============================
class Line:
    """
    A Non vertical line object is shaped with 2 points.
    There can be 2 types of lines.
        => Vertical: its general equation is: (1x + c = 0)
        => Horizontal: its general equation is: (1y + c = 0)
        => Non Vertical: its general equation is: (ax + 1y + c = 0)
    """
    TYPES = ['HORIZONTAL', 'VERTICAL', 'NON-VERTICAL']

    def __init__(self, point1: Point, point2: Point = None, given_gradient=None):
        self.__point1 = point1
        self.__point2 = point2
        self.__type = self.__check_type()
        self.__gradient = self.__get_gradient(given_gradient)
        self.__general_equation = self.__get_general_equation_form()

    @property
    def point1(self):
        return self.__point1

    @property
    def point2(self):
        return self.__point2

    @property
    def type(self):
        return self.__type

    @property
    def gradient(self):
        return self.__gradient

    @property
    def general_equation(self):
        return self.__general_equation

    def __check_type(self):
        if not ((self.point1 is None) or (self.point2 is None)):
            if self.point1.x - self.point2.x == 0:
                return Line.TYPES[0]
            elif self.point1.y - self.point2.y == 0:
                return Line.TYPES[1]
        return Line.TYPES[2]

    def __print_general_equation(self):
        general_equation = self.general_equation
        msm = str(general_equation[0])+"x " + str(general_equation[1]) + "y " + str(general_equation[2]) + " = 0"
        return msm

    def __str__(self):
        return """
        Line:
            hashable id:\t{0}
            general equation:\t{1}
        """.format(self.__hash__(), self.__print_general_equation())

    def __hash__(self):
        return id(self)

    def __get_gradient(self, given_gradient):
        """
        It figures out the slope / gradient out of the 2 given points.
        Through the following equation: m = (y2 - y1)/(x2 - x1)
        :return: the gradient.
        """
        if given_gradient is not None:
            return given_gradient
        else:
            if self.point2.x - self.point1.x == 0:
                gradient = None
            elif self.point2.y - self.point1.y == 0:
                pass
            else:
                gradient = (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)
            return gradient

    def __get_general_equation_form(self):
        """
        It gets the general equation form using the following expression
                (y - y1) = m(x - x1)
                y-y1=mx -mx1
                -y + mx + (y1-mx1)=0
                mx + -y + (y1-mx1)=0

        The general equation form => ax + by + c = 0

        vertical.
        x-c = 0
        x = c

        horizontal.
        y = mx + c
        y = c

        """
        general_expression = []
        if self.__type == "VERTICAL":
            general_expression = [float(1), None, -self.point1.x]
        elif self.__type == "HORIZONTAL":
            general_expression = [None, float(1), -self.point1.y]
        elif self.__type == "NON-VERTICAL":
            if self.gradient is not None:
                # [a, b, c]
                general_expression = [self.gradient, float(-1), -(self.gradient*self.point1.x) + self.point1.y]
            # else:
                # vertical line.
                # [a, none, c] => x - c = 0, x = c
            #    general_expression = [float(1), None, -self.point1.x]

        return general_expression

    def get_perpendicular_line_gradient(self):
        """
        Given two Non vertical lines, they'll be perpendicular if m1*m2 = -1.
        Otherwise they won't be perpendicular.
        m1 will be represented with the current gradient.
        :return: the slope m2 in order to shape a perpendicular line.
        """

        if self.gradient is None:
            return None
        else:
            return - 1 / self.gradient

    @classmethod
    def get_perpendicular_line_out_of_current_line(cls, reference_point: Point, gradient):
        """
        It figures out the perpendicular line out of the current line passing
        through the reference point.
        :param gradient: the gradient that satisfies m1*m2 = -1
        :param reference_point:
        :return: The perpendicular line.
        """
        return cls(reference_point, None, gradient)

    @staticmethod
    def get_intersection_point(line1, line2):

        if (line1.type == "VERTICAL" and line2.type == "VERTICAL") or \
                (line1.type == "HORIZONTAL" and line2.type == "HORIZONTAL"):
            raise ValueError("MALOLO")
        elif line1.type == "VERTICAL" and line2.type == "HORIZONTAL":
            pass
        elif line1.type == "HORIZONTAL" and line2.type == "VERTICAL":
            pass
        # faltaría mñas combinaciones.
        else:
            # both non-vertical
            pass

        # Through solving a system of linear equations with numpy
        # the intersection point is obtained.
        #    AX = B
        # where:
        #    A,X,B are matrices fulfilled with the general equation terms.

        """
            [a, b, c]
            0   1   2
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
        return Point(x[0], x[1])
