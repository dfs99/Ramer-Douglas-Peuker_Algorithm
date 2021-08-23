#include <iostream>
#include <chrono>
#include "../headers/BMPfile.h"

using namespace std;
int main(){
    const string filename = "../images/spain_map.bmp";
    auto start = std::chrono::system_clock::now();
    try{
        BMPfile my_file {filename};
        my_file.generate_point_file();
        //my_file.print_values(1);
        my_file.generate_bmp_file();
    }catch (const exception & e) {
        cerr << e.what() << endl;
        return -1;
    }
    auto end = std::chrono::system_clock::now();
    std::chrono::duration<double>duration = end - start;
    auto milliseconds = std::chrono::duration_cast<std::chrono::milliseconds>(duration).count();
    cout << "ELapsed time:\t" << milliseconds << " ms " << endl;
    return 0;
}