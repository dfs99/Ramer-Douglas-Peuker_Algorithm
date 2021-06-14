from unittest import TestCase
from src.main.python.code.data.line import Line
from src.main.python.code.data.point import Point


class TestLine(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls) -> None:
        pass

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_good_case_tests(self):
        point1 = Point(1.0, 2.0)
        point2 = Point(3.0, 7.0)
        new_line = Line(point1, point2)
        print("gradient: ", new_line.gradient)
        print("general equations: ", new_line.general_equation)
        self.assertEquals(new_line.gradient, new_line.gradient)
        self.assertEquals(new_line.general_equation, new_line.general_equation)
