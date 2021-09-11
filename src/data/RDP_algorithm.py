import statistics
from src.data import Point
from src.data import Line
from src.files_management import PerformancePy
from src.exceptions import RDPException, LineException


class RamerDouglasPeukerAlgorithm:

    def __init__(self, epsilon_error, data_set):
        self.__data_set = list(data_set)
        # first order points through y coord, afterwards apply x coord
        self.__data_set.sort(key=Point.order_points_y_coord)
        self.__data_set.sort(key=Point.order_points_x_coord)
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
        intersection_point = None
        try:
            intersection_point = Line.get_intersection_point(line1, line2)
        except LineException as ex:
            print(str(ex))
            exit(1)
        d = Point.get_distance_between_2_points(point, intersection_point)
        return d, intersection_point

    def solver(self, start_point, end_point):
        max_distance = 0
        start = start_point
        end = end_point
        line = None
        if len(self.data_set[start:end+1]) > 2:
            line = Line(self.data_set[start], self.data_set[end])
        for i in range(start+1, end):
            current_distance, intersection_point = RamerDouglasPeukerAlgorithm.get_distance(self.data_set[i], line)
            if current_distance > max_distance:
                start = i
                max_distance = current_distance
        if max_distance > self.epsilon_error:
            self.__append_point(self.data_set[start])
            self.solver(start_point, start)
            self.solver(start, end)

    def plot_solver(self, start_point, end_point):
        max_distance = 0
        start = start_point
        end = end_point
        line = None
        plot_data_index = 0
        if len(self.data_set[start:end+1]) > 2:
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
