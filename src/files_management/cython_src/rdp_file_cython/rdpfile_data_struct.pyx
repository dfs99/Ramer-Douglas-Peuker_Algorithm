# cython: language_level=3
from src.files_management.cython_src.rdp_file_cython.rdpfile_data_struct cimport RDPfile
# from src.files_management.cython_src.bmp_file_cython.bmpfile_data_structs cimport PyBMPfile

from cython.operator cimport dereference as deref

cdef class PyRDPfile:
    cdef RDPfile* cpp_rdp

    def __cinit__(self, PyBMPfile file, epsilon_error):
        self.cpp_rdp = new RDPfile(file.cpp_bmp, epsilon_error)

    def __dealloc__(self):
        # del self.__cpp_bmp
        del self.cpp_rdp

    @property
    def epsilon_error(self):
        return deref(self.cpp_rdp).get_epsilon_error()

    #@property
    #def bmp_file(self):
    #    return self.__cpp_bmp

    def generate_input_rdp_data(self):
        deref(self.cpp_rdp).generate_input_rdp_data()

        #double get_epsilon_error();
        #BMPfile* get_bmp_file();
        #void generate_input_rdp_data();
