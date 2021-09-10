#cython: language_level=3

from libcpp.string cimport string
from libc.stdint cimport uint8_t
from libc.stdint cimport uint32_t
from libc.stdint cimport uint16_t


cdef extern from "../cpp_srcs/headers/RDPfile.h":

    cdef cppclass pixel_24bpp:
        unsigned char blue
        unsigned char green
        unsigned char red

    cdef cppclass bitmap_header:
        unsigned char b
        unsigned char m
        unsigned int total_size_in_bytes
        unsigned int reserved_fields
        unsigned int image_data_offset

    cdef cppclass dib_header:
        unsigned int dib_header_size
        unsigned int width_in_pixels
        unsigned int height_in_pixels
        unsigned short color_planes
        unsigned short dot_size
        unsigned int compression_method
        unsigned int image_size_bytes
        unsigned int horizontal_resolution
        unsigned int vertical_resolution
        unsigned int color_pallete_size
        unsigned int color_count

    cdef cppclass BMPfile:
        BMPfile(string) except +
        string path_
        string filename_
        int padding_
        bitmap_header* header_
        dib_header* detailed_header_
        pixel_24bpp** image_data_
        string get_path();
        string get_filename();
        int get_padding();
        void print_values (int);
        void generate_point_file();
        void generate_bmp_file();

    cdef cppclass RDPfile:
        RDPfile(BMPfile &bmp, double epsilon_error) except +
        BMPfile* bmp_
        double epsilon_error_
        double get_epsilon_error();
        void generate_input_rdp_data();

