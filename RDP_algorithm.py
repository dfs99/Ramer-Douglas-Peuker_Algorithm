import numpy as np
from copy import deepcopy


def order_points(point: tuple):
    # given a point, it returns the value to be sorted
    # in this case, the x value.
    return point[0]


class RamerDouglasPeukerAlgorithm:

    def __init__(self, epsilon_error, data):
        # contains the data set passed.
        self.__current_data = deepcopy(data)
        self.__result = []
        self.__epsilon_error = epsilon_error
        self.__start_point = None
        self.__end_point = None

    @property
    def epsilon_error(self):
        return self.__epsilon_error

    @epsilon_error.setter
    def epsilon_error(self, new_epsilon_value):
        self.__epsilon_error = new_epsilon_value

    @property
    def start_point(self):
        return self.__start_point

    @property
    def end_point(self):
        return self.__end_point

    @property
    def result(self):
        return self.__result

    @property
    def current_data(self):
        return self.__current_data

    def initialize_start_end_points(self):
        self.__start_point, self.__end_point = self.get_extreme_points()

    def get_extreme_points(self):
        # It will get the two extreme points.
        # just check x axis. Thus, all the points
        # will be ordered.
        # 1-.) Check the nº of points.
        if len(self.__current_data) > 1:
            # 2-.) order the list.
            self.__current_data.sort(key=order_points)
            # 3-.) return both, the first and last point.
            return self.__current_data[0], self.__current_data[-1]
        else:
            # create an exception.
            raise TypeError(self)

    def get_farthest_point(self, start, end):
        """
            Devuelve el pto más alejado, el indice de este en la lista, el margen a comparar con epsilon.
        """
        # if none, there is no farthest point, thus the points cannot
        # be reduced. Otherwise, it will return a point.
        farthest_point = None
        index = -1
        max_value = -1
        # 1-.) If both, first and last points have the same y coordinates,
        #       use them as the pivot.
        if self.start_point[1] == self.end_point[1]:
            for i in range(start, end):
                if (self.current_data[i] is not self.start_point) and (self.current_data[i] is not self.end_point):
                    height = self.get_height(self.current_data[i])
                    if height > max_value:
                        farthest_point = self.current_data[i]
                        max_value = height
                        index = i
        else:
            # 2-.) Otherwise, we should get the distant with a Tales teorem.
            for i in range(start, end):
                if (self.current_data[i] is not self.start_point) and (self.current_data[i] is not self.end_point):
                    print('x' * 10)
                    height = self.get_height(self.current_data[i])
                    print('x' * 10)
                    if height > max_value:
                        farthest_point = self.current_data[i]
                        max_value = height
                        index = i

        return farthest_point, index, max_value

    def get_height(self, point):
        print(point)
        height_start_to_end = abs(self.start_point[1] - self.end_point[1])
        print('h_S_T', height_start_to_end)
        x_distance_between_start_and_end = abs(self.start_point[0] - self.end_point[0])
        print('x_s_e', x_distance_between_start_and_end)
        x_distance_between_start_point = abs(self.start_point[0] - point[0])
        print('x_s_p', x_distance_between_start_point)
        ratio = x_distance_between_start_and_end / x_distance_between_start_point
        height_start_to_point = height_start_to_end / ratio
        print(height_start_to_point)
        return height_start_to_point

    def ramer_douglas_peuker_algorithm(self):
        # inicializar los puntos extremos.
        self.initialize_start_end_points()
        # append those points to the result.
        self.__result.append(self.start_point)
        self.__result.append(self.end_point)

        start_index = 0
        end_index = len(self.current_data)

        self.__aux_rdp_algorithm(start_index, end_index)

    def __aux_rdp_algorithm(self, start_index, end_index):
        print('indices: ', start_index, end_index)
        point, index, max_diff = self.get_farthest_point(start_index, end_index)
        print(point, index, max_diff)
        if point is not None and index != -1 and max_diff != -1:
            if max_diff < self.epsilon_error:
                return []
            else:
                self.result.append(point)
            # self.result.append(point)
                a = self.__aux_rdp_algorithm(start_index, index)
                b = self.__aux_rdp_algorithm(index, end_index)
                return a + b

    @staticmethod
    def get_points(data: list):
        axis_x = []
        axis_y = []
        for i in range(0, len(data)):
            axis_x.append(data[1][0])
            axis_y.append(data[i][1])
        return axis_x, axis_y


test = RamerDouglasPeukerAlgorithm(1, [(1, 1), (2, 3), (4, 7), (4, 5), (6, 5)])
test.ramer_douglas_peuker_algorithm()
print(test.result)