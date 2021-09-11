import os
import sys
from src.data import Point
from src.files_management import Parser
from src.data import RamerDouglasPeukerPainter
from src.data import RamerDouglasPeukerAlgorithm
from src.exceptions import ParserException
# Import Python Objects created through Cython.
# Already compiled files.
from bmp_rdp_files import PyBMPfile, PyRDPfile


# TODO: opcion probada y funcionando f
# bash RamerDouglasPeukerAlgorithm.sh -f src/files_management/cpp_srcs/images/prueba8.bmp 1.4
#       opcion probada y funcionando x
# bash RamerDouglasPeukerAlgorithm.sh -x rdp_data_prueba8.txt

OPTIONS_FLAGS = {
    'b': 2,
    'f': 2,
    't': 1,
    'x': 1
}
PATH_TO_STORE = os.getcwd()[:os.getcwd().find("Ramer-Douglas-Peuker_Algorithm")] + \
                "Ramer-Douglas-Peuker_Algorithm/results"


def extract_path_and_filename(path):
    """
    Given a path, returns the directory and the file.
    """
    inv_path = path[::-1]
    start_index = 0
    end_index = inv_path.find('/')
    if end_index == -1:
        extracted_filename = inv_path[start_index:][::-1]
    else:
        extracted_filename = inv_path[start_index:end_index][::-1]
    extracted_path = path[:path.find(extracted_filename)]
    return extracted_path, extracted_filename


def solve_and_dump_into_txt(alg_inst: RamerDouglasPeukerAlgorithm,
                            path_to_store: str,
                            file_name: str):
    """
    Solves the algorithm and dumps the solution into
    a txt file.
    """
    alg_inst.solver(0, len(alg_inst.data_set) - 1)
    res_path = path_to_store + "/alg_result_" + \
        file_name[:file_name.find('.')] + '.txt'
    with open(res_path, 'w', encoding='utf-8') as f:
        f.write("=" * 25)
        f.write('\n')
        f.write("Algorithm result from:"
                "\nfile:\t{0}"
                "\nepsilon error:\t{1}".format(file_name, alg_inst.epsilon_error))
        f.write('\n')
        f.write("=" * 25)
        f.write('\n')
        for point in alg_inst.solution:
            f.write(str(point.x) + " " + str(point.y))
            f.write('\n')


def solve_and_generate_gif(alg_inst: RamerDouglasPeukerAlgorithm,
                           path_to_store: str,
                           file_name: str):
    """
    Solves the algorithm and generates a gif showing
    the process it took to perform the simplification.
    """
    alg_inst.plot_solver(0, len(alg_inst.data_set) - 1)
    alg_inst.solution.sort(key=Point.order_points_x_coord)
    # Generate gif.
    painter = RamerDouglasPeukerPainter(
        alg_inst.plot_data,
        alg_inst.data_set,
        alg_inst.solution
    )
    # TODO: Se le puede pasar la velocidad a la que
    # se genera el gif.
    painter.generate_animation(
        path_to_store,
        file_name[:file_name.find('.')] + "_gif_result",
        "GIF_EXTENSION",
        "FAST"
    )


def parse_and_extract_from_rdp_file(rdp_file_name: str):
    current_parser = None
    try:
        current_parser = Parser(rdp_file_name)
    except ParserException as ex:
        print(ex.message)
        exit(1)
    eps_error, data_block = current_parser.extract_data()
    return eps_error, data_block


def generate_rdp_file(file_name: str,
                      epsilon_error: float):
    rdp_name = None
    try:
        # manages any cpp exception @ constructors and
        # generates the rdp file.
        bmp_file = PyBMPfile(bytes(file_name, 'utf-8'))
        rdp_file = PyRDPfile(bmp_file, epsilon_error)
        rdp_name = str(rdp_file.generate_input_rdp_data())
    except RuntimeError as ex:
        print("Error: A cpp Exception has been thrown!")
        print(str(ex))
        exit(1)
    return rdp_name


def main(args: list):
    flag = args[0]
    if OPTIONS_FLAGS[flag] == len(args) - 1:
        if (flag == 'b') or (flag == 'f'):
            # 1-.) get args.
            file_name = args[1]
            epsilon_error = float(args[2])
            # 2-.) generate rdp file.
            rdp_name = generate_rdp_file(file_name, epsilon_error)
            path_n, file_n = extract_path_and_filename(file_name)
            # 3-.) parse rdp file.
            eps_error, data_block = parse_and_extract_from_rdp_file(rdp_name)
            # 4-.) Generate algorithm.
            alg_inst = RamerDouglasPeukerAlgorithm(eps_error, data_block)
            # 4.1-.) generate gif.
            if flag == 'b':
                solve_and_generate_gif(alg_inst, PATH_TO_STORE, file_n)
            # 4.2-.) generate text file.
            if flag == 'f':
                solve_and_dump_into_txt(alg_inst, PATH_TO_STORE, file_n)

        elif (flag == 't') or (flag == 'x'):
            # 1-.) get args.
            file_name = args[1]
            # 2-.) parse rdp file.
            eps_error, data_block = parse_and_extract_from_rdp_file(file_name)
            # 3-.) Generate algorithm.
            alg_inst = RamerDouglasPeukerAlgorithm(eps_error, data_block)
            path_n, file_n = extract_path_and_filename(file_name)
            # 3.1-.) generate gif.
            if flag == 't':
                solve_and_generate_gif(alg_inst, PATH_TO_STORE, file_n)
            # 3.2-.) generate text file.
            if flag == 'x':
                solve_and_dump_into_txt(alg_inst, PATH_TO_STORE, file_n)
    else:
        print("ERROR: Wrong number of arguments.")
        exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])

