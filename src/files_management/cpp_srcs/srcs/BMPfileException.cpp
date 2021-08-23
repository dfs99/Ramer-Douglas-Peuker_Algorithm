#include "../headers/BMPfile.h"


BMPfileException::BMPfileException(const char *message): message_{message} {}
char const* BMPfileException::what() const throw(){ return BMPfileException::message_; }
