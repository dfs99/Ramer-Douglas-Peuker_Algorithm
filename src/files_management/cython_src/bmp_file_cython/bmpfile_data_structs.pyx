# cython: language_level=3

from src.files_management.cython_src.bmp_file_cython.bmpfile_data_structs cimport BMPfile

from cython.operator cimport dereference as deref
from libcpp.string cimport string
from libcpp.vector cimport vector


cdef class PyBMPfile:
    cdef BMPfile *cpp_bmp
    def __cinit__(self, path):
        self.cpp_bmp = new BMPfile(path)

    def __dealloc__(self):
        del self.cpp_bmp

    @property
    def path(self):
        return deref(self.cpp_bmp).get_path()

    @property
    def filename(self):
        return deref(self.cpp_bmp).get_filename()

    @property
    def padding(self):
        return deref(self.cpp_bmp).get_padding()

    def show_info(self, ivalue):
        deref(self.cpp_bmp).print_values(ivalue)

    def generate_point_file(self):
        deref(self.cpp_bmp).generate_point_file()

    def generate_bmp_file(self):
        deref(self.cpp_bmp).generate_bmp_file()

        #int set_padding()
        #bool is_exists(const std::string& path)
        #std::string extract_filename_from_path()
        #void get_data_buffer(std::vector<unsigned char>& buff)
        #bool check_bmp_file()
        #void init_header(std::vector<unsigned char>& buffer)
        #void init_dib_header(std::vector<unsigned char>& buffer)
        #void fetch_image(std::vector<unsigned char>& buffer)

        #struct bitmap_header* get_header() const noexcept;
        #struct pixel_24bpp** get_image_data() const noexcept;
        #struct dib_header* get_detailed_header() const noexcept;