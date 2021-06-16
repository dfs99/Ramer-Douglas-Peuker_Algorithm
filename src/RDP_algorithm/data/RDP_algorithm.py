from copy import deepcopy
from src.RDP_algorithm.data.point import Point
from src.RDP_algorithm.data.line import Line


class RamerDouglasPeukerAlgorithm:

    def __init__(self, epsilon_error: float, data: list):
        self.__current_data = deepcopy(data)
        self.__current_data.sort(key=order_points)
        self.__epsilon_error = epsilon_error

    @property
    def epsilon_error(self):
        return self.__epsilon_error

    @epsilon_error.setter
    def epsilon_error(self, new_epsilon_value):
        self.__epsilon_error = new_epsilon_value

    @property
    def current_data(self):
        return self.__current_data

    @staticmethod
    def get_distance(point: Point, line1: Line):
        line2 = Line.get_perpendicular_line_out_of_current_line(point, line1.get_perpendicular_line_gradient())
        intersection_point = Line.get_intersection_point(line1, line2)
        return Point.get_distance_between_2_points(point, intersection_point)

    def solve(self, data):
        # converts the data into a dictionary
        # in order to delete duplicates.
        result = self.__solve_algorithm(data)
        result = list(dict.fromkeys(result))
        result.sort(key=order_points)
        return result

    def __solve_algorithm(self, data):
        max_distance = 0
        start = 0
        end = len(data)-1
        for i in range(1, end):
            distance = RamerDouglasPeukerAlgorithm.get_distance(Point(data[i][0], data[i][1]),
                                                                Line(Point(data[start][0], data[start][1]),
                                                                Point(data[end][0], data[end][1])))
            print(i, " => ",  distance)
            if distance > max_distance:
                start = i
                max_distance = distance

        if max_distance > self.epsilon_error:
            print(data[:start+1])
            print(data[start:])
            left_result = self.solve(data[:start+1])
            right_result = self.solve(data[start:])
            result = left_result + right_result
        else:
            result = [data[0], data[end]]
        return result


def order_points(point: tuple):
    # given a point, it returns the value to be sorted
    # in this case, the x value.
    return point[0]


lista_examen = [(1.0, 1.0), (2.0, 3.0), (3.0, 1.5),
                (4.0, 5.0), (5.0, 4.0), (6.0, 2.0)]

l1 = [(1, 1), (2, 3), (4, 7), (5, 4), (6, 5)]
test = RamerDouglasPeukerAlgorithm(1.75, lista_examen)
print(test.current_data)
print(test.solve(test.current_data))
