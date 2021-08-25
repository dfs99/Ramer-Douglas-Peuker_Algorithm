# from distutils.core import setup
from setuptools import setup
from Cython.Build import cythonize

with open("README.md") as f:
    long_description = f.read()

setup(
    name="RDP_Algorithm_generator",
    version="1.0.0",
    description="",
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
    language="",




    ext_modules=cythonize(""))
