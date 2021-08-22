#include <iostream>
#include "../headers/BMPfile.h"

using namespace std;
int main(){
    const string filename = "../images/prueba3.bmp";
    BMPfile my_file {filename};
    my_file.generate_point_file();
    my_file.print_values();
    my_file.generate_bmp_file();
}