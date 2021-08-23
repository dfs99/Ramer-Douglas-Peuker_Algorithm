#include "../headers/RDPfile.h"


RDPfileException::RDPfileException(const char *message): message_{message} {}
char const* RDPfileException::what() const throw(){ return RDPfileException::message_; }