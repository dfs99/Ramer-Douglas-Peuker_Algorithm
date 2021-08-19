from unittest import TestCase
from src.data.line import Line
from src.data.point import Point
from src.exceptions.line_exception import LineException


class TestLine(TestCase):
    test_num = 0
    filename = "line.py"

    def setUp(self) -> None:
        TestLine.test_num += 1
        # print("""Test nº) {0}: Starting test...""".format(TestLine.test_num))

    def tearDown(self) -> None:
        # print("\t\t\tending test...")
        pass

    @classmethod
    def setUpClass(cls):
        print("INITIALIZING " + TestLine.filename + " TESTS:")

    @classmethod
    def tearDownClass(cls):
        print("ENDING " + TestLine.filename + " TESTS.")

    """
    =================================================================
                        Tests to instance Lines
    =================================================================
    """

    def test_preference_order_tests(self):
        p1 = Point(1.0, 4.0)
        p2 = Point(3.0, 5.0)
        line = Line(p1, p2, gradient=1.998, type='NON-VERTICAL')
        self.assertEqual(line.general_equation, [0.5, -1.0, 3.5])
        self.assertEqual(line.type, 'NON-VERTICAL')

    def test_horizontal_line_tests(self):
        p1 = Point(1.0, 4.0)
        p2 = Point(3.0, 4.0)
        line = Line(p1, p2)
        self.assertEqual(line.general_equation, [0.0, 1.0, -4.0])
        self.assertEqual(line.type, 'HORIZONTAL')

    def test_horizontal_line_kwargs_tests(self):
        p1 = Point(3.0, 3.0)
        line = Line(p1, gradient=0.0, type='HORIZONTAL')
        self.assertEqual(line.general_equation, [0.0, 1.0, -3.0])
        self.assertEqual(line.type, 'HORIZONTAL')

    def test_vertical_line_tests(self):
        p1 = Point(3.0, 7.0)
        p2 = Point(3.0, 11.5)
        line = Line(p1, p2)
        self.assertEqual(line.general_equation, [1.0, None, -3.0])
        self.assertEqual(line.type, 'VERTICAL')

    def test_vertical_line_kwargs_tests(self):
        p1 = Point(2.0, 5.0)
        line = Line(p1, gradient=None, type='VERTICAL')
        self.assertEqual(line.general_equation, [1.0, None, -2.0])
        self.assertEqual(line.type, 'VERTICAL')

    def test_non_vertical_line_tests(self):
        p1 = Point(2.0, 5.5)
        p2 = Point(3.4, 9.2)
        line = Line(p1, p2)
        self.assertEqual(line.general_equation, [2.6428571428571423, -1.0, 0.2142857142857153])
        self.assertEqual(line.type, 'NON-VERTICAL')

    def test_non_vertical_kwargs_tests(self):
        p1 = Point(2.0, 5.5)
        line = Line(p1, gradient=1.6859, type='NON-VERTICAL')
        self.assertEqual(line.general_equation, [1.6859, -1.0, 2.1282])
        self.assertEqual(line.type, 'NON-VERTICAL')

    def test_wrong_kwargs_at_line(self):
        p1 = Point(2.0, 5.5)
        with self.assertRaises(LineException) as cm:
            Line(p1, slope=1.6859, kind='NON-VERTICAL')
        self.assertEqual(str(cm.exception), 'ERROR: Non-existent kwarg parsed. Wrong kwarg: slope:1.6859')

    def test_wrong_kwargs_type_value_tests(self):
        p1 = Point(2.0, 5.5)
        with self.assertRaises(LineException) as cm:
            Line(p1, gradient=1.6859, type='perpendicular')
        self.assertEqual(str(cm.exception), 'ERROR: Non-existent line type: perpendicular Valid types are: [' +
                         "'VERTICAL', 'HORIZONTAL', 'NON-VERTICAL']")

    def test_wrong_kwargs_gradient_float_tests(self):
        p1 = Point(2.0, 5.5)
        with self.assertRaises(LineException) as cm:
            Line(p1, gradient=1, type='NON-VERTICAL')
        self.assertEqual(str(cm.exception), "ERROR: Gradient must be a float type.")

    def test_wrong_kwargs_gradient_none_tests(self):
        p1 = Point(2.0, 1.0)
        with self.assertRaises(LineException) as cm:
            Line(p1, gradient=None, type='NON-VERTICAL')
        self.assertEqual(str(cm.exception), "ERROR: Gradient is only None for VERTICAL lines.")

    def test_wrong_kwargs_values_vertical_tests(self):
        p1 = Point(2.0, 1.0)
        with self.assertRaises(LineException) as cm:
            Line(p1, gradient=1.45, type='VERTICAL')
        self.assertEqual(str(cm.exception), "ERROR: Gradient for VERTICAL line is None. Not: 1.45")

    def test_wrong_kwargs_values_horizontal_tests(self):
        p1 = Point(2.0, 1.0)
        with self.assertRaises(LineException) as cm:
            Line(p1, gradient=1.45, type='HORIZONTAL')
        self.assertEqual(str(cm.exception), "ERROR: Gradient for HORIZONTAL line is 0.0. Not: 1.45")

    def test_using_only_kwargs_gradient_non_vertical_tests(self):
        p1 = Point(1.0, 4.0)
        line = Line(p1, gradient=1.98)
        self.assertEqual(line.general_equation, [1.98, -1.0, 2.02])
        self.assertEqual(line.type, 'NON-VERTICAL')

    def test_using_only_kwargs_gradient_vertical_tests(self):
        p1 = Point(1.0, 4.0)
        line = Line(p1, gradient=None)
        self.assertEqual(line.general_equation, [1.0, None, -1.0])
        self.assertEqual(line.type, 'VERTICAL')

    def test_using_only_kwargs_gradient_horizontal_tests(self):
        p1 = Point(2.0, 9.0)
        line = Line(p1, gradient=0.0)
        self.assertEqual(line.general_equation, [0.0, 1.0, -9.0])
        self.assertEqual(line.type, 'HORIZONTAL')

    """
        =================================================================
                        Tests to check Lines operations
        =================================================================
    """

    def test_perpendicular_vertical_line_tests(self):
        line1 = Line(Point(1.0, 1.0), gradient=None)
        line2 = line1.get_perpendicular_line(Point(3.0, 3.0))
        self.assertEqual(line2.general_equation, [0.0, 1.0, -3.0])
        self.assertEqual(line2.type, 'HORIZONTAL')

    def test_perpendicular_horizontal_line_tests(self):
        line1 = Line(Point(1.0, 1.0), gradient=0.0)
        line2 = line1.get_perpendicular_line(Point(3.0, 3.0))
        self.assertEqual(line2.general_equation, [1.0, None, -3.0])
        self.assertEqual(line2.type, 'VERTICAL')

    def test_perpendicular_non_vertical_line_tests(self):
        line1 = Line(Point(1.0, 1.0), gradient=1.5)
        line2 = line1.get_perpendicular_line(Point(3.0, 3.0))
        self.assertEqual(line2.general_equation, [-0.6666666666666666, -1.0, 5.0])
        self.assertEqual(line2.type, 'NON-VERTICAL')

    def test_intersection_point_two_vertical_lines_tests(self):
        line1 = Line(Point(1.0, 1.0), gradient=None)
        line2 = Line(Point(2.0, 2.0), gradient=None)
        with self.assertRaises(LineException) as cm:
            Line.get_intersection_point(line1, line2)
        self.assertEqual(str(cm.exception), 'ERROR: Two vertical lines are parallel and will never cross each other.')

    def test_intersection_point_two_horizontal_lines_tests(self):
        line1 = Line(Point(1.0, 1.0), gradient=0.0)
        line2 = Line(Point(2.0, 2.0), gradient=0.0)
        with self.assertRaises(LineException) as cm:
            Line.get_intersection_point(line1, line2)
        self.assertEqual(str(cm.exception), 'ERROR: Two horizontal lines are parallel and will never cross each other.')

    def test_intersection_point_vertical_horizontal_lines_tests(self):
        line1 = Line(Point(1.0, 3.0), gradient=0.0)
        line2 = Line(Point(2.0, 5.0), gradient=None)
        point = Line.get_intersection_point(line1, line2)
        self.assertEqual(point, Point(2.0, 3.0))

    def test_intersection_point_horizontal_vertical_lines_tests(self):
        line1 = Line(Point(2.0, 5.0), gradient=None)
        line2 = Line(Point(1.0, 3.0), gradient=0.0)
        point = Line.get_intersection_point(line1, line2)
        self.assertEqual(point, Point(2.0, 3.0))

    def test_intersection_point_horizontal_non_vertical_lines_tests(self):
        line1 = Line(Point(2.0, 5.0), gradient=0.0)
        line2 = Line(Point(1.0, 3.0), gradient=1.5)
        point = Line.get_intersection_point(line1, line2)
        self.assertEqual(point, Point(2.3333333333333335, 5.0))

    def test_intersection_point_non_vertical_horizontal_lines_tests(self):
        line1 = Line(Point(1.0, 3.0), gradient=1.5)
        line2 = Line(Point(2.0, 5.0), gradient=0.0)
        point = Line.get_intersection_point(line1, line2)
        self.assertEqual(point, Point(2.3333333333333335, 5.0))

    def test_intersection_point_vertical_non_vertical_lines_tests(self):
        line1 = Line(Point(2.0, 5.0), gradient=None)
        line2 = Line(Point(1.0, 3.0), gradient=1.5)
        point = Line.get_intersection_point(line1, line2)
        self.assertEqual(point, Point(2.0, 4.5))

    def test_intersection_point_non_vertical_vertical_lines_tests(self):
        line1 = Line(Point(1.0, 3.0), gradient=1.5)
        line2 = Line(Point(2.0, 5.0), gradient=None)
        point = Line.get_intersection_point(line1, line2)
        self.assertEqual(point, Point(2.0, 4.5))

    def test_intersection_point_two_non_vertical_lines_tests(self):
        line1 = Line(Point(1.0, 3.0), gradient=1.5)
        line2 = Line(Point(0.0, 0.0), Point(1.0, -1.0))
        point = Line.get_intersection_point(line1, line2)
        self.assertEqual(point, Point(-0.6, 0.6000000000000001))
