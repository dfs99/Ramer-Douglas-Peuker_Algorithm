import os
from src.data import Point
from src.files_management import Parser
from src.data import RamerDouglasPeukerPainter
from src.data import RamerDouglasPeukerAlgorithm


PATH_TO_STORE = os.getcwd()[:os.getcwd().find("Ramer-Douglas-Peuker_Algorithm")] + \
                    "Ramer-Douglas-Peuker_Algorithm/results"

current_parser = Parser('src/dataset/sin.txt')
epsilon_error, data = current_parser.extract_data()

rdp_instance = RamerDouglasPeukerAlgorithm(epsilon_error, data)
rdp_instance.plot_solver(0, len(rdp_instance.data_set) - 1)
rdp_instance.solution.sort(key=Point.order_points_x_coord)
painter = RamerDouglasPeukerPainter(rdp_instance.plot_data, rdp_instance.data_set, rdp_instance.solution)
painter.generate_animation(PATH_TO_STORE, "sin_function_fast_low_error", "GIF_EXTENSION", "FAST")
