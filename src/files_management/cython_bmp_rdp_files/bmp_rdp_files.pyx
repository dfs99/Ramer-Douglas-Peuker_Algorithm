# cython: language_level=3

from src.files_management.cython_bmp_rdp_files.bmp_rdp_files cimport RDPfile, BMPfile
from cython.operator cimport dereference as deref
from libcpp.string cimport string

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


cdef class PyRDPfile:
    cdef RDPfile* cpp_rdp

    def __cinit__(self, PyBMPfile file, double epsilon_error):
        self.cpp_rdp = new RDPfile(deref(file.cpp_bmp), epsilon_error)

    def __dealloc__(self):
        del self.cpp_rdp

    @property
    def epsilon_error(self):
        return deref(self.cpp_rdp).get_epsilon_error()

    def generate_input_rdp_data(self):
        """
        returns the rdp_file name.
        """
        return (deref(self.cpp_rdp).generate_input_rdp_data()).decode('utf-8')
