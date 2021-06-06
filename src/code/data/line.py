import numpy as np
from point import Point
from ..exceptions.line_exception import LineException

class StraightLine:
    """
    A line object is shaped with 2 points.
    """

    def __init__(self, point1: Point, point2: Point = None, given_gradient=None):
        # se pasan las referencias a los objetos únicamente
        # expression: y = ax + b
        self.__point1 = point1
        self.__point2 = point2

        if given_gradient is None:
            self.__gradient = self.get_gradient()
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

    def get_gradient(self):
        """
        It figures out the slope / gradient out of the 2 given points.
        Through the following equation: m = (y2 - y1)/(x2 - x1)
        :return: the gradient.
        """
        try:
            gradient = (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)
        except ZeroDivisionError as exception:
            # raise LineException("Linea no recta") from exception
            # vertical line
            gradient = None
        return gradient

    def __get_general_equation_form(self):
        """
        It gets the general equation form using the following expression
        with point1 attribute and puts into a 3-element List.
                (y - y1) = m(x - x1)
        The general equation form => ax + by + c = 0
        """
        general_expression = []
        if self.gradient is not None:
            general_expression = [self.gradient, 1, (-self.gradient*self.point1.x) + self.point1.y]
        else:
            # vertical line.
            general_expression = [self.point1.x, None, None]
        return general_expression

    def get_perpendicular_line_gradient(self):
        """
        Given two lines, they'll be perpendicular if m1*m2 = -1.
        Otherwise they won't be perpendicular.
        m1 will be represented with the current slope / gradient.
        :return: the slope m2 in order to shape a perpendicular line.
        """
        #TODO que pasa si la linea tiene pendiente 0? revisar este problema.
        # las lineas perpendiculares a una recta vertical y horizontal.
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

