import numpy as np


def order_points(point: tuple):
    # given a point, it returns the value to be sorted
    # in this case, the x value.
    return point[0]


class RamerDouglasPeukerAlgorithm(object):
    # class variable that holds the shared data.
    # It contains all the points to be plotted.
    historic_data = None

    def __init__(self, epsilon_error):
        # contains the data set passed.
        self.__current_data = []
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

    def get_farthest_point(self):
        # if none, there is no farthest point, thus the points cannot
        # be reduced. Otherwise, it will return a point.
        farthest_point = None
        # 1-.) If both, first and last points have the same y coordinates,
        #       use them as the pivot.
        if self.start_point[1] == self.end_point[1]:
            for point in self.__current_data:
                if point[1] > self.epsilon_error:
                    farthest_point = point
        else:
            # 2-.) Otherwise, we should get the distant with a Tales teorem.
            for point in self.__current_data:
                # get the height of the point.
                height = self.get_height(point)
                if abs(point[1] - height) > self.epsilon_error:
                    farthest_point = point
        return farthest_point

    def get_height(self, point):
        height_start_to_end = abs(self.start_point[1] - self.end_point[1])
        x_distance_between_start_and_end = abs(self.start_point[0] - self.end_point[0])
        x_distance_between_start_point = abs(self.start_point[0] - point[0])
        ratio = x_distance_between_start_and_end / x_distance_between_start_point
        height_start_to_point = height_start_to_end / ratio
        return height_start_to_point

    def ramer_douglas_peuker_algorithm(self):
        # inicializar los puntos extremos.
        self.initialize_start_end_points()
        # append those points to the result.
        self.__result.append(self.start_point)
        self.__result.append(self.end_point)

        point = self.get_farthest_point()
        while point is not None:
            self.__result.append(point)
            point = self.get_farthest_point()


    @classmethod
    def place_function(cls):
        # en principio poder hacer cualquier función que se le pase
        # como parámetro.
        cls.historic_data = None

    @staticmethod
    def get_points(data: list):
        axis_x = []
        axis_y = []
        for i in range(0, len(data)):
            axis_x.append(data[1][0])
            axis_y.append(data[i][1])
        return axis_x, axis_y


x = -7
y = -10
print('x: ', abs(x - y))

print(10 * np.pi)
x = np.linspace(0, 10 * np.pi, 100)
y = np.sin(x)
print(x)
print(y)
