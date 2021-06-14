import numpy as np
from point import Point
from ..exceptions.line_exception import LineException


class Line:
    """
    A line object is shaped with 2 points.
    There can be 2 types of lines.
        => Vertical: its general equation is: (1x + c = 0)
        => Non Vertical: its general equation is: (ax + 1y + c = 0)
    """

    def __init__(self, point1: Point, point2: Point = None, given_gradient=None):
        self.__point1 = point1
        self.__point2 = point2
        if given_gradient is None:
            self.__gradient = self.__get_gradient()
        else:
            self.__gradient = given_gradient
        self.__general_equation = self.__get_general_equation_form()

    @property
    def point1(self):
        return self.__point1

    @property
    def point2(self):
        return self.__point2

    @property
    def gradient(self):
        return self.__gradient

    @property
    def general_equation(self):
        return self.__general_equation

    def __get_gradient(self):
        """
        It figures out the slope / gradient out of the 2 given points.
        Through the following equation: m = (y2 - y1)/(x2 - x1)
        :return: the gradient.
        """
        if self.point2.x - self.point1.x == 0:
            gradient = None
        else:
            gradient = (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)
        return gradient

    def __get_general_equation_form(self):
        """
        It gets the general equation form using the following expression
                (y - y1) = m(x - x1)
        The general equation form => ax + by + c = 0
        """
        general_expression = []
        if self.gradient is not None:
            # [a, b, c]
            general_expression = [self.gradient, 1, (-self.gradient*self.point1.x) + self.point1.y]
        else:
            # vertical line.
            # [a, none, c] => x - c = 0, x = c
            general_expression = [1, None, -self.point1.x]
        return general_expression

    def get_perpendicular_line_gradient(self):
        """
        Given two Non vertical lines, they'll be perpendicular if m1*m2 = -1.
        Otherwise they won't be perpendicular.
        m1 will be represented with the current gradient.
        :return: the slope m2 in order to shape a perpendicular line.
        """
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

