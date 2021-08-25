cdef extern from "../cpp_srcs/srcs/BMPfile.cpp"
    pass

cdef extern from "../cpp_srcs/headers/BMPfile.h"
    cdef cppclass BMPfile:
        BMPfile(string given path) except +
        std::string path_
        std::string filename_
        int padding_
        struct bitmap_header* header_
        struct dib_header* detailed_header_
        struct pixel_24bpp** image_data_
        std::string get_path() const noexcept;
        std::string get_filename() const noexcept;
        int get_padding() const noexcept;
        struct bitmap_header* get_header() const noexcept;
        struct pixel_24bpp** get_image_data() const noexcept;
        struct dib_header* get_detailed_header() const noexcept;
        void print_values (int code) const;
        void generate_point_file() const;
        void generate_bmp_file() const;
        int set_padding()
        bool is_exists(const std::string& path)
        std::string extract_filename_from_path()
        void get_data_buffer(std::vector<unsigned char>& buff)
        bool check_bmp_file()
        void init_header(std::vector<unsigned char>& buffer)
        void init_dib_header(std::vector<unsigned char>& buffer)
        void fetch_image(std::vector<unsigned char>& buffer)


