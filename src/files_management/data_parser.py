import os
from src.data import Point
from src.exceptions import ParserException


class Parser:
    # comprobar que en unix funcione tmbn
    CURRENT_PATH = os.getcwd()[:os.getcwd().find("Ramer-Douglas-Peuker_Algorithm")] + 'Ramer-Douglas-Peuker_Algorithm/'
    FILE_EXTENSION = 'txt'
    __slots__ = '_file'

    def __init__(self, file_path):
        super(Parser, self).__setattr__('_file', Parser.__validate_file(file_path))

    @property
    def file(self):
        return self._file

    def extract_data(self, n_points=False):
        """
        By default it returns:
            -> epsilon error
            -> set that contains all the points instances.
                Note that there is no repeated points
        If arg :n_points: is True, it also returns
        the nº of points contained in the file.
        """
        data = set()
        with open(self.file, 'r', encoding='utf-8') as f:
            epsilon_error = float(f.readline())
            total_num_points = int(f.readline())
            for _ in range(0, total_num_points):
                current_line = f.readline()
                extract_coord = current_line.split(' ')
                new_point = Point(float(extract_coord[0]), float(extract_coord[1]))
                data.add(new_point)
        if n_points is True:
            return epsilon_error, data, total_num_points
        return epsilon_error, data

    @staticmethod
    def __validate_file(file):
        path = Parser.CURRENT_PATH + file
        if not os.path.exists(path):
            raise ParserException("ERROR: Path does not exist: " + str(path))
        if os.stat(path).st_size == 0:
            raise ParserException("ERROR: The file is empty.")
        if Parser.__get_file_extension(path) != Parser.FILE_EXTENSION:
            raise ParserException("ERROR: Wrong file extension.")
        return Parser.__validate_data(path)

    @staticmethod
    def __validate_data(file):
        try:
            with open(file, 'r', encoding='utf-8') as f:
                Parser.__validate_epsilon_error(f.readline())
                number_points_line = Parser.__validate_number_points(f.readline())
                for _ in range(0, number_points_line):
                    Parser.validate_lines(f.readline())
            return file
        except FileNotFoundError as error:
            raise ParserException("ERROR: The file cannot be opened.") from error

    @staticmethod
    def validate_lines(line):
        extract_data = line.split()
        if len(extract_data) > 2:
            raise ParserException("ERROR: Too many args to represent a Point.")
        elif len(extract_data) <= 1:
            raise ParserException("ERROR: Too few args to represent a Point.")
        try:
            float(extract_data[0])
            float(extract_data[1])
        except ValueError as error:
            raise ParserException("ERROR: Wrong data type (not float): '" + str(extract_data) + "' cannot be "
                "converted into a Point.") from error

    @staticmethod
    def __validate_epsilon_error(line):
        extract_data = line.split()
        if len(extract_data) > 1:
            raise ParserException("ERROR: Too many args for epsilon error.")
        elif len(extract_data) == 0:
            raise ParserException("ERROR: There is no value for epsilon error.")
        try:
            epsilon_error = float(extract_data[0])
        except ValueError as error:
            raise ParserException("ERROR: Wrong data type: '" + extract_data[0] + "' cannot be converted into float.") \
                from error
        return epsilon_error

    @staticmethod
    def __validate_number_points(line):
        extract_data = line.split()
        if len(extract_data) > 1:
            raise ParserException("ERROR: Too many args for number of points.")
        elif len(extract_data) == 0:
            raise ParserException("ERROR: There is no value for number of points.")
        try:
            number_points = int(extract_data[0])
            if number_points < 2:
                raise ParserException("ERROR: File must contain two or more points.")
        except ValueError as error:
            raise ParserException("ERROR: Wrong data type: '" + extract_data[0] + "' cannot be converted into "
                                                                                  "integer.") from error
        return number_points

    @staticmethod
    def __get_file_extension(file_path):
        return file_path.split('.')[1]
