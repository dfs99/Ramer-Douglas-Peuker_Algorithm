import sys
import bmpfile_data_structs
from src.data import Point
from src.files_management import Parser
from src.data import RamerDouglasPeukerPainter
from src.data import RamerDouglasPeukerAlgorithm
from src.files_management import PerformancePy


def main(argv):
    name = "./files_management/cpp_srcs/images/prueba1.bmp"
    file = bmpfile_data_structs.PyBMPfile(bytes(name, 'utf-8'))
    file.generate_bmp_file()
    file.generate_point_file()
    print("passing 0:\n")
    file.show_info(0)
    print("passing 1:\n")
    file.show_info(1)
    print("passing 2:\n")
    file.show_info(2)




if __name__ == '__main__':
    main(sys.argv[1:])



