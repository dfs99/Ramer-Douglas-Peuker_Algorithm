import bmpfile_data_structs
name = "../cpp_srcs/images/prueba1.bmp"
file = bmpfile_data_structs.PyBMPfile(bytes(name, 'utf-8'))
file.generate_bmp_file()
print("passing 0:\n")
file.show_info(0)
print("passing 1:\n")
file.show_info(1)
print("passing 2:\n")
file.show_info(2)