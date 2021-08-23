#include <iostream>
#include "../headers/BMPfile.h"

using namespace std;
int main(){
    const string filename = "../images/large.bmp";
    BMPfile my_file {filename};
    my_file.generate_point_file();
    my_file.print_values(1);
    my_file.generate_bmp_file();
}