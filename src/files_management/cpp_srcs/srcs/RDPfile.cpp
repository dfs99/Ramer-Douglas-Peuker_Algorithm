#include "../headers/RDPfile.h"
#include "../headers/BMPfile.h"
#include <iostream>
#include <fstream>
#include <cstdio>
#include <string>


const char* RDP_EXCEPT_FAIL_TO_DELETE = "Error, A problem has occurred while deleting BMP aux file.";

RDPfile::RDPfile(BMPfile &bmp, double epsilon_error): bmp_{&bmp}, epsilon_error_{epsilon_error}{}
RDPfile::~RDPfile(){ }

double RDPfile::get_epsilon_error() const noexcept { return RDPfile::epsilon_error_; }
BMPfile* RDPfile::get_bmp_file() const noexcept { return RDPfile::bmp_; }

std::string RDPfile::generate_input_rdp_data(){

    // generate input file.
    RDPfile::get_bmp_file()->generate_point_file();

    // extract raw name.
    size_t lastindex = RDPfile::get_bmp_file()->get_filename().find_last_of(".");
    std::string rawname = RDPfile::get_bmp_file()->get_filename().substr(0, lastindex);

    std::string output_filename = "rdp_data_" + rawname + ".txt";
    std::string input_filename = "res_" + rawname + ".txt";

    // generate output file
    std::ofstream output(output_filename, std::ios_base::binary);
    // paste epsilon error.
    output << RDPfile::get_epsilon_error();
    output.write("\n", sizeof(unsigned char));

    // get input data file
    std::ifstream input(input_filename, std::ios_base::binary);

    // copy paste data from ifstream to ofstream.
    output << input.rdbuf();
    //close fstreams.
    output.close();
    input.close();

    if (remove(input_filename.c_str()) != 0) throw RDPfileException(RDP_EXCEPT_FAIL_TO_DELETE);

    return output_filename;
}
