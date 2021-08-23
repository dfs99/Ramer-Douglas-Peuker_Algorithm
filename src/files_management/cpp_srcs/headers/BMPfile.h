//#pragma once // has the same purpose as header guards.

// header guards.
#ifndef BMPFILE_H
#define BMPFILE_H

#include <cstdint>
#include <exception>
#include <string>
#include <vector>
// check for speed up.
// #include <array>

struct pixel_24bpp{
    /*
    *   Struct representing a pixel of 24 bits per pixel.
    *   Thus, due to pixels have 3 values, each one will
    *   have 8 bits = 1 byte.
    *
    *   Format used: (Blue, Green, Red)
    */
    uint8_t blue;
    uint8_t green;
    uint8_t red;
};

struct bitmap_header{
    /*
    *   BMP header is shaped by 2 kind of headers. The first
    *   one, bitmap_header:
    *
    *   => Magic bytes: b and m contain each one its char b
    *      and m respectively.
    *   => Image total size in bytes.
    *   => Reserved fields, it varies depending on the app
    *      that has generated the file. If manually, it will
    *      be set to 0.
    *   => image data offset, where the raw image starts in the
    *      bmp file.
    *
    *   Memory needed: 14 bytes.
    *
    */
    unsigned char b;
    unsigned char m;
    uint32_t total_size_in_bytes;
    uint32_t reserved_fields;
    uint32_t image_data_offset;
};

// 40 bytes.
struct dib_header{
    /*
    *   Second header that contains detailed information.
    *
    *   => dib header size, its size 40 bytes.
    *   => image width in pixels.
    *   => image height in pixels.
    *   => color planes must be 1.
    *   => dot size, number bits per pixel. Here 24bbp only.
    *   => Compression method, 0. No compression method allowed.
    *   => Image size in bytes.
    *   => Horizontal resolution, pixel per metre.
    *   => Vertical resolution, pixel per metre.
    *   => Color pallete size.
    *   => color count.
    *
    */
    uint32_t dib_header_size;
    uint32_t width_in_pixels;
    uint32_t height_in_pixels;
    uint16_t color_planes;
    uint16_t dot_size;
    uint32_t compression_method;
    uint32_t image_size_bytes;
    uint32_t horizontal_resolution;
    uint32_t vertical_resolution;
    uint32_t color_pallete_size;
    uint32_t color_count;
};

class BMPfile{
public:
    explicit BMPfile(const std::string given_path);
    ~BMPfile();

    // const keyword, no attr are modified.
    std::string get_path() const noexcept;
    std::string get_filename() const noexcept;
    int get_padding() const noexcept;
    struct bitmap_header* get_header() const noexcept;
    struct pixel_24bpp** get_image_data() const noexcept;
    struct dib_header* get_detailed_header() const noexcept;

    void print_values (int code) const;
    void generate_point_file() const;
    void generate_bmp_file() const;

private:
    // Attrs.
    std::string path_;
    std::string filename_;
    int padding_;
    struct bitmap_header* header_;
    struct dib_header* detailed_header_;
    struct pixel_24bpp** image_data_;

    // funcs used to set up instances @ constructor
    int set_padding();
    bool is_exists(const std::string& path);
    std::string extract_filename_from_path();
    void get_data_buffer(std::vector<unsigned char>& buff);
    bool check_bmp_file();
    void init_header(std::vector<unsigned char>& buffer);
    void init_dib_header(std::vector<unsigned char>& buffer);
    void fetch_image(std::vector<unsigned char>& buffer);
};

//using bitmap_point2 = std::array<size_t, 2>;
// check for speed up.

struct bitmap_point{
    size_t x_coord;
    size_t y_coord;
};

class BMPfileException : public std::exception {
    const char *message_;
public:
    BMPfileException(const char* msg);
    virtual char const* what() const throw();
};

#endif