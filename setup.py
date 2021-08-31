# from distutils.core import setup
from setuptools import Extension, setup
from Cython.Build import cythonize

#with open("README.md") as f:
#    long_description = f.read()

## command: python setup.py build_ext --inplace
"""Extension("src.files_management.cython_src.bmp_file_cython.bmpfile_data_structs",
              sources=["src/files_management/cpp_srcs/srcs/BMPfile.cpp",
                       "src/files_management/cpp_srcs/srcs/BMPfileException.cpp",
                       "src/files_management/cython_src/bmp_file_cython/bmpfile_data_structs.pyx"],
              library_dirs=["src/files_management/cpp_srcs/headers/BMPfile.h"],
              language="c++"
              ),"""
extensions = [

    Extension("src.files_management.cython_src.rdp_file_cython.rdpfile_data_struct",
              sources=["src/files_management/cpp_srcs/srcs/BMPfile.cpp",
                       "src/files_management/cpp_srcs/srcs/RDPfile.cpp",
                       "src/files_management/cpp_srcs/srcs/BMPfileException.cpp",
                       "src/files_management/cpp_srcs/srcs/RDPfileException.cpp",
                       "src/files_management/cython_src/rdp_file_cython/rdpfile_data_struct.pyx"],
              library_dirs=["src/files_management/cpp_srcs/headers/BMPfile.h",
                            "src/files_management/cpp_srcs/headers/RDPfile.h"],
              language="c++"
              )
]
setup(
    ext_modules=cythonize(extensions))

"""
name="RDP_Algorithm_generator",
    version="1.0.0",
    description="xd",
    long_description=long_description,
    author="",
    author_email="",
    url="",
    packages=[
        "src",
        "src/data",
        "src/exceptions",
        "src/files_management",
        ],
"""