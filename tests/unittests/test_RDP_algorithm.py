from unittest import TestCase
from src.exceptions import RDPException
from src.data import RamerDouglasPeukerAlgorithm
from src.files_management import Parser
from src.data import Point


class TestRamerDouglasPeukerAlgorithm(TestCase):
    test_num = 0
    filename = "RDP_algorithm.py"

    def setUp(self) -> None:
        TestRamerDouglasPeukerAlgorithm.test_num += 1
        # print("""Test nº) {0}: Starting test...""".format(TestRamerDouglasPeukerAlgorithm.test_num))

    def tearDown(self) -> None:
        # print("\t\t\tending test...")
        pass

    @classmethod
    def setUpClass(cls):
        print("INITIALIZING " + TestRamerDouglasPeukerAlgorithm.filename + " TESTS:")

    @classmethod
    def tearDownClass(cls):
        print("ENDING " + TestRamerDouglasPeukerAlgorithm.filename + " TESTS.")

    def test_valid_rdp_data_tests(self):
        current_parser = Parser('src/dataset/data2.txt')
        epsilon_error, data = current_parser.extract_data()
        rdp_instance = RamerDouglasPeukerAlgorithm(epsilon_error, data)
        rdp_instance.solver(0, len(rdp_instance.data_set) - 1)
        #print(type(rdp_instance.solution))
        #print(type(rdp_instance.data_set))
        self.assertEqual(set(rdp_instance.solution), {Point(1.0, 1.0), Point(7.0, 1.0), Point(4.0, 7.0),
                                                      Point(6.0, 5.0), Point(5.0, 4.0)})


    def test_valid_rdp_plot_data_tests(self):
        current_parser = Parser('src/dataset/data2.txt')
        epsilon_error, data = current_parser.extract_data()
        rdp_instance = RamerDouglasPeukerAlgorithm(epsilon_error, data)
        rdp_instance.plot_solver(0, len(rdp_instance.data_set) - 1)
        # print(rdp_instance.plot_data)
        for step in rdp_instance.plot_data:
            #print("PASO ALGORITMO: ")
            #print(step[0], step[1])
            #print("ptos a comprobar")
            for point_list in step[2]:
                for p in point_list:
                    pass
                    # print(p)
        # print(len(rdp_instance.plot_data))

    def test_xd(self):
        current_parser = Parser('src/dataset/sin.txt')
        epsilon_error, data = current_parser.extract_data()
        rdp_instance = RamerDouglasPeukerAlgorithm(epsilon_error, data)
        rdp_instance.plot_solver(0, len(rdp_instance.data_set) - 1)
