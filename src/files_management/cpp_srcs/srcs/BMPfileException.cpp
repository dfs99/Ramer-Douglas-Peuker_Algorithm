#include "../headers/BMPfile.h"


BMPfileException::BMPfileException(const char *msg): message(msg) {}
char const* BMPfileException::what() const throw(){return BMPfileException::message;}
