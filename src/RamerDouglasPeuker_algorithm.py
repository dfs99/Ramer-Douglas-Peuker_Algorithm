import sys

# Import Python Objects created through Cython.
from bmp_rdp_files import PyBMPfile, PyRDPfile

"""
    RamerDouglasPeuker_algorithm    # generates an usage printout
    RamerDouglasPeuker_algorithm -h # generates a help menu.
    RamerDouglasPeuker_algorithm -gifbmp bmpfilename epsilonerror  # generates a gif
    RamerDouglasPeuker_algorithm -algbmp bmpfilename epsilonerror # generates just the points the algorithm gets.
    RamerDouglasPeuker_algorithm -algf filename #generates the points 
    RamerDouglasPeuker_algorithm -giff filename #generates a gif with the data 

"""

def main(*args, **kwargs):

    name = "./files_management/cpp_srcs/images/prueba1.bmp"
    epsilon_error = 1.3
    bmp_file = PyBMPfile(bytes(name, 'utf-8'))
    # bmp_file.generate_bmp_file()
    # bmp_file.generate_point_file()
    print("passing 0:\n")
    bmp_file.show_info(0)
    print("passing 1:\n")
    bmp_file.show_info(1)
    print("passing 2:\n")
    bmp_file.show_info(2)

    rdp_file = PyRDPfile(bmp_file, epsilon_error)
    print("Epsilon error: ", rdp_file.epsilon_error)
    rdp_file.generate_input_rdp_data()


if __name__ == '__main__':
    main(sys.argv[1:])
