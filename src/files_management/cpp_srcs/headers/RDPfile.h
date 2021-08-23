#ifndef RDPFILE_H
#define RDPFILE_H

#include "BMPfile.h"

class RDPfile{
    public:
        explicit RDPfile(BMPfile &bmp, double epsilon_error);
        ~RDPfile();
        double get_epsilon_error() const noexcept;
        BMPfile* get_bmp_file() const noexcept;
        void generate_input_rdp_data();

    private:
        BMPfile* bmp_;
        double epsilon_error_;

};

class RDPfileException : public std::exception {
    const char *message_;
public:
    explicit RDPfileException(const char* msg);
    virtual char const* what() const throw();
};

#endif