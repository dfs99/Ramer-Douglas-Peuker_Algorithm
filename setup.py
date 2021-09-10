from setuptools import Extension, setup
from Cython.Build import cythonize

# Used to compile and use C++ code through Cython.
# command: python setup.py build_ext --inplace
extensions = [
    Extension("src.files_management.cython_bmp_rdp_files.bmp_rdp_files",
              sources=["src/files_management/cpp_srcs/srcs/BMPfile.cpp",
                       "src/files_management/cpp_srcs/srcs/RDPfile.cpp",
                       "src/files_management/cpp_srcs/srcs/BMPfileException.cpp",
                       "src/files_management/cpp_srcs/srcs/RDPfileException.cpp",
                       "src/files_management/cython_bmp_rdp_files/bmp_rdp_files.pyx"],
              library_dirs=["src/files_management/cpp_srcs/headers/BMPfile.h",
                            "src/files_management/cpp_srcs/headers/RDPfile.h"],
              language="c++"
              )
]
setup(ext_modules=cythonize(extensions))
