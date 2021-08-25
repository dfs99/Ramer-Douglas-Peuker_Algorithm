import statistics
from src.data import Point
from src.data import Line
from src.files_management import PerformancePy
from src.exceptions import RDPException


class RamerDouglasPeukerAlgorithm:
    X_COORD = 'x'
    Y_COORD = 'y'

    def __init__(self, epsilon_error, data_set, order_data='x'):
        self.__data_set = list(data_set)
        if order_data == RamerDouglasPeukerAlgorithm.X_COORD:
            self.__data_set.sort(key=Point.order_points_x_coord)
        elif order_data == RamerDouglasPeukerAlgorithm.Y_COORD:
            self.__data_set.sort(key=Point.order_points_y_coord)
        else:
            raise RDPException('ERROR: Points can be only sorted through x and y coordinates. Not ' + str(order_data))
        self.__epsilon_error = epsilon_error
        self.__solution = [self.data_set[0], self.data_set[len(self.data_set) - 1]]
        self.__plot_data = []
        """
            [
                [ptos que forman la linea,  [[par de ptos forman perpendicular con booleano indicando si es elegido], [], ... ]]
            ]
        """

    @property
    def epsilon_error(self):
        return self.__epsilon_error

    @epsilon_error.setter
    def epsilon_error(self, new_epsilon_value):
        self.__epsilon_error = new_epsilon_value

    @property
    def data_set(self):
        return self.__data_set

    @property
    def solution(self):
        return self.__solution

    @property
    def plot_data(self):
        return self.__plot_data

    def __append_point(self, point):
        position = len(self.solution)-1
        self.__solution.insert(position, point)

    def flush_solution(self):
        self.__solution = []

    def initialize_solution(self):
        self.__solution = [self.data_set[0], self.data_set[len(self.data_set) - 1]]

    @staticmethod
    def get_distance(point: Point, line1: Line):
        line2 = line1.get_perpendicular_line(point)
        intersection_point = Line.get_intersection_point(line1, line2)
        d = Point.get_distance_between_2_points(point, intersection_point)
        #print("#################################\n "
        #      "get distance between", point, intersection_point, "distance: " + str(d),
        #      "\n ===============================================")
        return d, intersection_point

    def solver(self, start_point, end_point):
        max_distance = 0
        start = start_point
        end = end_point
        intersection_point = None
        line = None
        x = self.data_set[start:end+1]
        # print("start_i" + str(start) + " end_i" + str(end) + " " + str(self.data_set[start:end+1]))
        # print(len(x))
        if len(x) > 2:
            line = Line(self.data_set[start], self.data_set[end])
            # print("points used for the line: ", self.data_set[start], self.data_set[end], "*"*20)
        for i in range(start+1, end):
            # try:
            current_distance, intersection_point = RamerDouglasPeukerAlgorithm.get_distance(self.data_set[i],
                                                                        line)
            # except AttributeError as e:
            #    raise RDPException("start_i" + str(start) + " end_i" + str(end) + " " + str(self.data_set[start:end+1]))
            if current_distance > max_distance:
                start = i
                max_distance = current_distance
        if max_distance > self.epsilon_error:
            # print('inter_p', intersection_point, 'point_dataset', self.data_set[start])
            self.__append_point(self.data_set[start])
            self.solver(start_point, start)
            self.solver(start, end)

    def plot_solver(self, start_point, end_point):
        max_distance = 0
        start = start_point
        end = end_point
        line = None
        plot_data_index = 0
        data_subset = self.data_set[start:end+1]
        if len(data_subset) > 2:
            line = Line(self.data_set[start], self.data_set[end])
            self.__plot_data.append([self.data_set[start_point], self.data_set[end], []])
            plot_data_index = len(self.__plot_data)-1
        for i in range(start+1, end):
            current_distance, intersection_point = RamerDouglasPeukerAlgorithm.get_distance(self.data_set[i], line)
            self.__plot_data[plot_data_index][2].append([self.data_set[i], intersection_point, False])
            if current_distance > max_distance:
                start = i
                max_distance = current_distance
        if max_distance > self.epsilon_error:
            self.__append_point(self.data_set[start])
            for point_list in self.__plot_data[plot_data_index][2]:
                if self.data_set[start] in point_list:
                    # print("pto mas alejado:")
                    # print(point_list[0])
                    # print(point_list[1])
                    point_list[2] = True
            self.plot_solver(start_point, start)
            self.plot_solver(start, end)

    @PerformancePy.benchmark
    def __get_solver_statistics(self):
        """
        Executes one time the algorithm and measures its performance.
        :return: The solution
        """
        self.solver(0, len(self.data_set) - 1)
        return self.solution

    def get_solver_statistics(self, n_times):
        """
        Executes n times the algorithm and gets some statistics.
        Each time the algorithm is executed, the solution is flushed
        and starts initializing again.

        :param n_times: times to execute.
        """
        total_times = []
        for i in range(0, n_times):
            self.flush_solution()
            self.initialize_solution()
            results = self.__get_solver_statistics()
            total_times.append(results[0])

        stats = """
                   =========================================
                   |---------------------------------------|
                   |              STATISTICS               |
                   |---------------------------------------|
                   | Initial nº points:\t{0}
                   | Final nº points:\t{1}
                   | nº times executed:\t{2}
                   | mean value:\t{3} ms
                   | max value:\t{4} ms
                   | min value:\t{5} ms
                   =========================================
        """.format(
            len(self.data_set), len(self.solution), n_times, statistics.mean(total_times), max(total_times),
            min(total_times))
        print(stats)
