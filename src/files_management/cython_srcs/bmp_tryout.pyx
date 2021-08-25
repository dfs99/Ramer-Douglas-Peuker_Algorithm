# distutils: language = c++

from bmp_file cimport BMPfile

cdef class pyBMPfile:
    cdef BMPfile c_bmp_file
    def __cinit__(self, path):
        self.c_bmp_file = BMPfile(path)
