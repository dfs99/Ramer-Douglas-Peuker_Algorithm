#include <iostream>
#include <chrono>
#include "../headers/BMPfile.h"
#include "../headers/RDPfile.h"


using namespace std;
int main(){
    const string filename = "../images/spain_map.bmp";
    auto start1 = std::chrono::system_clock::now();
    BMPfile my_file1 {filename};
    try{
        BMPfile my_file {filename};
        //my_file.generate_point_file();
        my_file.print_values(0);
        //my_file.generate_bmp_file();
    }catch (const exception & e) {
        cerr << e.what() << endl;
        return -1;
    }
    auto end1 = std::chrono::system_clock::now();
    std::chrono::duration<double>duration1 = end1 - start1;
    auto milliseconds1 = std::chrono::duration_cast<std::chrono::milliseconds>(duration1).count();
    cout << "Elapsed time bmp file:\t" << milliseconds1 << " ms " << endl;

    auto start2 = std::chrono::system_clock::now();
    try{
        RDPfile generator (my_file1, 0.123);
        generator.generate_input_rdp_data();
    } catch (const exception & e) {
        cerr << e.what() << endl;
        return -1;
    }
    auto end2 = std::chrono::system_clock::now();
    std::chrono::duration<double>duration2 = end2 - start2;
    auto milliseconds2 = std::chrono::duration_cast<std::chrono::milliseconds>(duration2).count();
    cout << "Elapsed time rdp generator:\t" << milliseconds2 << " ms " << endl;
    BMPfile* current_ptr;
    current_ptr = new BMPfile("../images/spain_map.bmp");
    current_ptr->generate_bmp_file();
    current_ptr->print_values(2);
    std::cout << "fiiinn << std::endl;
    return 0;
}
