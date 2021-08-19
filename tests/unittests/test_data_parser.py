from unittest import TestCase
from src.files_management import Parser
from src.exceptions import ParserException


class TestParser(TestCase):
    test_num = 0
    filename = "data_parser.py"

    def setUp(self) -> None:
        TestParser.test_num += 1
        # print("""Test nº) {0}: Starting test...""".format(TestParser.test_num))

    def tearDown(self) -> None:
        # print("\t\t\tending test...")
        pass

    @classmethod
    def setUpClass(cls):
        print("INITIALIZING " + TestParser.filename + " TESTS:")

    @classmethod
    def tearDownClass(cls):
        print("ENDING " + TestParser.filename + " TESTS.")

    def test_valid_data_parser_tests(self):
        p = Parser("src/dataset/test_cases/valid_data.txt")
        epsilon, data = p.extract_data()
        self.assertEqual(epsilon, 0.75)
        self.assertEqual(len(data), 5)

    def test_valid_data_parser_with_n_points_tests(self):
        p = Parser("src/dataset/test_cases/valid_data1.txt")
        epsilon, data, n_points = p.extract_data(True)
        self.assertEqual(epsilon, 0.75)
        self.assertEqual(len(data), 5)
        self.assertEqual(n_points, 6)

    def test_valid_data_with_negative_points_tests(self):
        p = Parser("src/dataset/test_cases/valid_data_negative_points.txt")
        epsilon, data = p.extract_data()
        self.assertEqual(epsilon, 0.75)
        self.assertEqual(len(data), 3)

    def test_wrong_path_tests(self):
        with self.assertRaises(ParserException) as cm:
            Parser("non_existent_path/data1.txt")
        # WINDOWS
        #self.assertEqual(str(cm.exception),
        #                 "ERROR: Path does not exist: C:\\Users\\DIEGO\\PycharmProjects\\Ramer-Douglas-Peuker_Algorit"
        #                 "hm/non_existent_path/data1.txt")
        # LINUX
        self.assertEqual(str(cm.exception), "ERROR: Path does not exist: /home/diego/PycharmProjects/Ramer-Douglas-Peuker_Algorithm/non_existent_path/data1.txt")

    def test_wrong_epsilon_too_many_args_tests(self):
        with self.assertRaises(ParserException) as cm:
            Parser("src/dataset/test_cases/wrong_epsilon_error_too_many_args.txt")
        self.assertEqual(str(cm.exception), "ERROR: Too many args for epsilon error.")

    def test_wrong_epsilon_str_tests(self):
        with self.assertRaises(ParserException) as cm:
            Parser("src/dataset/test_cases/wrong_epsilon_error_str.txt")
        self.assertEqual(str(cm.exception), "ERROR: Wrong data type: 'hello' cannot be converted into float.")

    def test_wrong_n_points_value_too_many_args_tests(self):
        with self.assertRaises(ParserException) as cm:
            Parser("src/dataset/test_cases/wrong_n_points_value_too_many_args.txt")
        self.assertEqual(str(cm.exception), "ERROR: Too many args for number of points.")

    def test_wrong_n_points_value_str_tests(self):
        with self.assertRaises(ParserException) as cm:
            Parser("src/dataset/test_cases/wrong_n_points_value_str.txt")
        self.assertEqual(str(cm.exception), "ERROR: Wrong data type: 'bye' cannot be converted into integer.")

    def test_wrong_point_value_too_many_args_tests(self):
        with self.assertRaises(ParserException) as cm:
            Parser("src/dataset/test_cases/wrong_point_value_too_many_args.txt")
        self.assertEqual(str(cm.exception), "ERROR: Too many args to represent a Point.")

    def test_wrong_point_value_too_few_args_tests(self):
        with self.assertRaises(ParserException) as cm:
            Parser("src/dataset/test_cases/wrong_point_value_too_few_args.txt")
        self.assertEqual(str(cm.exception), "ERROR: Too few args to represent a Point.")

    def test_wrong_point_value_str_tests(self):
        with self.assertRaises(ParserException) as cm:
            Parser("src/dataset/test_cases/wrong_point_value_str.txt")
        self.assertEqual(str(cm.exception), "ERROR: Wrong data type (not float): '['wrong', '4.77']' cannot be converted into a Point.")

    def test_empty_file_tests(self):
        with self.assertRaises(ParserException) as cm:
            Parser("src/dataset/test_cases/empty_file.txt")
        self.assertEqual(str(cm.exception), "ERROR: The file is empty.")

    def test_wrong_file_extension_tests(self):
        with self.assertRaises(ParserException) as cm:
            Parser("src/dataset/test_cases/wrong_extension_file.csv")
        self.assertEqual(str(cm.exception), "ERROR: Wrong file extension.")

    def test_no_epsilon_error_value_tests(self):
        with self.assertRaises(ParserException) as cm:
            Parser("src/dataset/test_cases/no_epsilon_error.txt")
        self.assertEqual(str(cm.exception), "ERROR: There is no value for epsilon error.")

    def test_n_points_value_tests(self):
        with self.assertRaises(ParserException) as cm:
            Parser("src/dataset/test_cases/no_n_points_error.txt")
        self.assertEqual(str(cm.exception), "ERROR: There is no value for number of points.")

    def test_few_points_tests(self):
        with self.assertRaises(ParserException) as cm:
            Parser("src/dataset/test_cases/few_points.txt")
        self.assertEqual(str(cm.exception), "ERROR: File must contain two or more points.")
