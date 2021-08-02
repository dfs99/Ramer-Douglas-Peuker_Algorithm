import numpy as np
from src.data.point import Point
from src.exceptions.line_exception import LineException


class Line:
    """
    Line class:
    A line can be created through either:
        -> 2 Point instances.
        -> 1 Point instance and the given gradient and type.
        -> 1 Point instance and the given gradient.

    Important: If two points instances and kwargs are passed.
    The 2 points have preference over the kwargs and the line
    will be created using exclusively the points.

    The class supports three kinds of lines:
        -> VERTICAL
            -> gradient: None
        -> HORIZONTAL
            -> gradient: 0.0
        -> NON-VERTICAL
            -> gradient: any float.

    The class has its own Exception: LineException
    """

    LINE_TYPES = ["VERTICAL", "HORIZONTAL", "NON-VERTICAL"]
    KWARGS_LABELS = ['gradient', 'type']
    HORIZONTAL_GRADIENT = 0.0

    def __init__(self, point1, point2=None, **kwargs):
        kwargs = Line.__check_kwargs(kwargs)
        new_gradient = None
        new_type = None
        if kwargs is not None and point2 is None:
            if Line.KWARGS_LABELS[0] in kwargs.keys():
                new_gradient = kwargs[Line.KWARGS_LABELS[0]]
            if Line.KWARGS_LABELS[1] in kwargs.keys():
                new_type = kwargs[Line.KWARGS_LABELS[1]]
        self.__point1 = point1
        self.__point2 = point2
        self.__type = self.__set_type(new_type, new_gradient)
        self.__gradient = self.__set_gradient(new_gradient)
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

    @property
    def general_equation(self):
        return self.__general_equation

    def __set_type(self, new_type, new_gradient):
        """
        :return: the proper type. Otherwise LineException.
        """
        if new_type is None:
            if self.point2 is not None:
                if self.point1.x - self.point2.x == 0:
                    return Line.LINE_TYPES[0]
                elif self.point1.y - self.point2.y == 0:
                    return Line.LINE_TYPES[1]
                else:
                    return Line.LINE_TYPES[2]
            if new_gradient is None:
                return Line.LINE_TYPES[0]
            elif new_gradient == Line.HORIZONTAL_GRADIENT:
                return Line.LINE_TYPES[1]
            else:
                return Line.LINE_TYPES[2]
        else:
            return Line.validate_type(new_type)

    def __set_gradient(self, new_gradient):
        """
        It figures out the gradient out of the 2 given points
        for non-vertical lines through the following equation:
            m = (y2 - y1)/(x2 - x1)

        And for the horizontal lines, the gradient is set
        automatically to 0.0.

        :return: None for Vertical lines, otherwise the
                line's gradient which is 0.0 for Horizontal
                lines or any float for Non-vertical lines.
                If an exception occurs, LineException
        """
        if new_gradient is None:
            if self.type == Line.LINE_TYPES[2] and self.point2 is not None:
                return float((self.point2.y - self.point1.y) / (self.point2.x - self.point1.x))
            if self.type == Line.LINE_TYPES[1] and self.point2 is not None:
                return Line.HORIZONTAL_GRADIENT
        return self.__validate_gradient(new_gradient)

    def __validate_gradient(self, gradient):
        """
        Vertical line has None gradient.
        Horizontal line has 0.0 gradient.
        Non-Vertical line has any float gradient.

        :param gradient: given gradient
        :return: the given gradient or LineException.
        """
        if gradient is None and (self.type == Line.LINE_TYPES[1] or self.type == Line.LINE_TYPES[2]):
            raise LineException("ERROR: Gradient is only None for VERTICAL lines.")
        if not (isinstance(gradient, float) or gradient is None):
            raise LineException("ERROR: Gradient must be a float type.")
        if gradient != Line.HORIZONTAL_GRADIENT and self.type == Line.LINE_TYPES[1]:
            raise LineException("ERROR: Gradient for HORIZONTAL line is 0.0. Not: " + str(gradient))
        if gradient is not None and self.type == Line.LINE_TYPES[0]:
            raise LineException("ERROR: Gradient for VERTICAL line is None. Not: " + str(gradient))
        return gradient

    def __set_general_equation(self):
        """
        General expression:
            Non-vertical lines:
                y = mx + n
                ax + by + c = 0;
            Vertical lines:
                ax + c = 0
            Horizontal lines:
                y = n
                by + c = 0
        where:
            [a, b, c]

        :return: A list that contains the general expression form.
        """
        general_expression = []
        # vertical
        if self.type == Line.LINE_TYPES[0]:
            general_expression = [float(1), None, -self.point1.x]
        # horizontal
        elif self.type == Line.LINE_TYPES[1]:
            general_expression = [Line.HORIZONTAL_GRADIENT, float(1), -self.point1.y]
        # non-vertical
        elif self.type == Line.LINE_TYPES[2]:
            general_expression = [self.gradient, float(-1), -(self.gradient * self.point1.x) + self.point1.y]
        return general_expression

    def get_perpendicular_line(self, reference_point):
        """
        :param reference_point: the point through the line will be drawn.
        :return: a new line's instance or an exception.
        """
        # vertical
        if self.type == Line.LINE_TYPES[0]:
            return Line.generate_perpendicular_line(reference_point, Point(self.point1.x, reference_point.y), None)
        # horizontal
        elif self.type == Line.LINE_TYPES[1]:
            return Line.generate_perpendicular_line(reference_point, Point(reference_point.x, self.point1.y), None)
        # non-vertical
        elif self.type == Line.LINE_TYPES[2]:
            perpendicular_gradient = -1/self.gradient
            return Line.generate_perpendicular_line(reference_point, None, perpendicular_gradient)

    @classmethod
    def generate_perpendicular_line(cls, point1, point2, gradient):
        if point2 is None:
            return cls(point1, gradient=gradient)
        return cls(point1, point2)

    @staticmethod
    def __check_kwargs(kwargs):
        """
        :param kwargs: dict that contains kwargs.
        :return:
            -> None if there aren't any kwargs.
            -> LineException if wrong kwargs.
            -> dict that contains the kwargs.
        """
        if bool(kwargs):
            kwargs_validated = {}
            for key, value in kwargs.items():
                if key in Line.KWARGS_LABELS:
                    kwargs_validated[key] = value
                else:
                    raise LineException("ERROR: Non-existent kwarg parsed. Wrong kwarg: " + str(key) + ":" + str(value))
            return kwargs_validated
        else:
            return None

    @staticmethod
    def validate_type(current_type):
        if current_type not in Line.LINE_TYPES:
            raise LineException("ERROR: Non-existent line type: " + str(current_type) + " Valid types are: " +
                                str(Line.LINE_TYPES))
        return current_type

    @staticmethod
    def get_intersection_point(line1, line2):
        """
                    [a, b, c]
                    0   1   2

                    mx + -y + (y1-mx1)=0
                    ax + by + c=0
                    y = mx + (-mx1+y1)

                    empleando y despejando y=mx+n
        """
        if line1.type == "VERTICAL" and line2.type == "HORIZONTAL":
            return Point(line1.point1.x, line2.point1.y)
        elif line1.type == "HORIZONTAL" and line2.type == "VERTICAL":
            return Point(line2.point1.x, line1.point1.y)
        elif (line1.type == "HORIZONTAL" and line2.type == "NON-VERTICAL") or \
                (line1.type == "NON-VERTICAL" and line2.type == "HORIZONTAL"):
            if line1.type == "HORIZONTAL":
                slope = line2.general_equation[0]
                independent_term = line2.general_equation[2]
                y_coord = -line1.general_equation[2]
            else:
                slope = line1.general_equation[0]
                independent_term = line1.general_equation[2]
                y_coord = -line2.general_equation[2]
            x_coord = (y_coord - independent_term)/slope
            return Point(x_coord, y_coord)

        elif (line1.type == "VERTICAL" and line2.type == "NON-VERTICAL") or \
                (line1.type == "NON-VERTICAL" and line2.type == "VERTICAL"):
            if line1.type == "VERTICAL":
                slope = line2.general_equation[0]
                independent_term = line2.general_equation[2]
                x_coord = -line1.general_equation[2]
            else:
                slope = line1.general_equation[0]
                independent_term = line1.general_equation[2]
                x_coord = -line2.general_equation[2]
            y_coord = slope*x_coord + independent_term
            return Point(x_coord, y_coord)

        elif line1.type == "NON-VERTICAL" and line2.type == "NON-VERTICAL":
            # Through solving a system of linear equations with numpy
            # the intersection point is obtained.
            #    AX = B
            # where:
            #    A,X,B are matrices fulfilled with the general equation terms.
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
            point = np.linalg.inv(a).dot(b)

            # x is a vector [x, y] that contains the values like that.
            return Point(float(point[0]), float(point[1]))
        else:
            if line1.type == "VERTICAL" and line2.type == "VERTICAL":
                raise LineException("ERROR: Two vertical lines are parallel and will never cross each other.")
            elif line1.type == "HORIZONTAL" and line2.type == "HORIZONTAL":
                raise LineException("ERROR: Two horizontal lines are parallel and will never cross each other.")
