from unittest import TestCase
from src.data.point import Point
from src.exceptions.point_exception import PointException


class TestPoint(TestCase):
    test_num = 0

    def setUp(self) -> None:
        TestPoint.test_num += 1
        print("""Test nº) {0}: Starting test...""".format(TestPoint.test_num))

    def tearDown(self) -> None:
        print("\t\t\tending test...")

    @classmethod
    def setUpClass(cls):
        print("INITIALIZING TESTS:")

    @classmethod
    def tearDownClass(cls):
        print("ENDING TESTS.")

    def test_generate_point_tests(self):
        p1 = Point(1.0, 2.0)
        self.assertEqual(p1.x, 1.0)
        self.assertEqual(p1.y, 2.0)

    def test_generate_wrong_point_tests(self):
        with self.assertRaises(PointException) as cm:
            p1 = Point(1, 2.0)
        self.assertEqual(str(cm.exception), "Error: Point coordinates must be floats.")

    def test_two_points_equal_tests(self):
        # mismo hash y mismos objetos.
        p1 = Point(1.0, 2.0)
        p2 = Point(1.0, 2.0)
        self.assertEqual(p1.__hash__(), p2.__hash__())
        self.assertEqual(p1, p2)

    def test_operation_with_sets_tests(self):
        p1 = Point(1.0, 2.0)
        p2 = Point(1.0, 2.0)
        p3 = Point(2.0, 2.0)
        p4 = Point(3.0, 2.0)
        set_test = {p1, p2, p3, p4}
        self.assertEqual(set_test, {p1, p3, p4})

    def test_immutable_obj_add_new_attr_tests(self):
        p4 = Point(1.0, 5.0)
        with self.assertRaises(PointException) as cm:
            p4.z = 3.0
        self.assertEqual(str(cm.exception), "Immutable Object Error: Point class cannot have more attributes nor "
                                            "change their values.")

    def test_immutable_obj_add_change_attr_tests(self):
        p4 = Point(1.0, 5.0)
        with self.assertRaises(PointException) as cm:
            p4.x = 3.0
        self.assertEqual(str(cm.exception), "Immutable Object Error: Point class cannot have more attributes nor "
                                            "change their values.")

    def test_immutable_obj_slots_tests(self):
        p4 = Point(1.0, 5.0)
        self.assertEqual(p4.__slots__, ('_x', '_y'))

    def test_immutable_obj_no_dict_tests(self):
        p4 = Point(1.0, 5.0)
        with self.assertRaises(AttributeError) as cm:
            print(p4.__dict__)
        self.assertEqual(str(cm.exception), "'Point' object has no attribute '__dict__'")

    def test_order_x_coord_points_tests(self):
        list_to_sort = [Point(1.0, 3.0), Point(0.0, 30.0), Point(10.0, 4.0), Point(5.0, 2.0)]
        list_to_sort.sort(key=Point.order_points_x_coord)
        self.assertEqual(list_to_sort, [Point(0.0, 30.0), Point(1.0, 3.0), Point(5.0, 2.0), Point(10.0, 4.0)])

    def test_order_y_coord_points_tests(self):
        list_to_sort = [Point(1.0, 3.0), Point(0.0, 30.0), Point(10.0, 4.0), Point(5.0, 2.0)]
        list_to_sort.sort(key=Point.order_points_y_coord)
        self.assertEqual(list_to_sort, [Point(5.0, 2.0), Point(1.0, 3.0), Point(10.0, 4.0), Point(0.0, 30.0)])

    def test_distance_between_two_diagonal_positive_points_tests(self):
        p1 = Point(1.0, 1.0)
        p2 = Point(2.0, 2.0)
        self.assertEqual(Point.get_distance_between_2_points(p1, p2), 1.4142135623730951)

    def test_distance_between_two_diagonal_negative_points_tests(self):
        p1 = Point(-1.0, -1.0)
        p2 = Point(-2.0, -2.0)
        self.assertEqual(Point.get_distance_between_2_points(p1, p2), 1.4142135623730951)

    def test_distance_between_positive_negative_diagonal_points_tests(self):
        p1 = Point(-1.0, -1.0)
        p2 = Point(2.0, 2.0)
        self.assertEqual(Point.get_distance_between_2_points(p1, p2), 4.242640687119285)

    def test_distance_between_positive_vertical_points_tests(self):
        p1 = Point(1.0, 1.0)
        p2 = Point(1.0, 5.0)
        self.assertEqual(Point.get_distance_between_2_points(p1, p2), 4.0)

    def test_distance_between_negative_vertical_points_tests(self):
        p1 = Point(-1.0, -1.0)
        p2 = Point(-1.0, -5.0)
        self.assertEqual(Point.get_distance_between_2_points(p1, p2), 4.0)

    def test_distance_between_positive_negative_vertical_points_tests(self):
        p1 = Point(1.0, 1.0)
        p2 = Point(1.0, -5.0)
        self.assertEqual(Point.get_distance_between_2_points(p1, p2), 6.0)

    def test_distance_between_positive_horizontal_points_tests(self):
        p1 = Point(1.0, 1.0)
        p2 = Point(5.0, 1.0)
        self.assertEqual(Point.get_distance_between_2_points(p1, p2), 4.0)

    def test_distance_between_negative_horizontal_points_tests(self):
        p1 = Point(-1.0, -1.0)
        p2 = Point(-5.0, -1.0)
        self.assertEqual(Point.get_distance_between_2_points(p1, p2), 4.0)

    def test_distance_between_positive_negative_horizontal_points_tests(self):
        p1 = Point(1.0, 1.0)
        p2 = Point(1.0, -5.0)
        self.assertEqual(Point.get_distance_between_2_points(p1, p2), 6.0)
