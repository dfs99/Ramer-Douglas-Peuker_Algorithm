#include <iostream>
#include <fstream>
#include <vector>
#include "../headers/BMPfile.h"

// get current os to manage path accesses.
#if defined(_WIN32)
    #define PLATFORM_NAME 1 // windows.
#elif defined(_WIN64)
    #define PLATFORM_NAME 1 // "windows"
#elif defined(__linux__)
    #define PLATFORM_NAME 2 // "linux"
#endif

// padding
#define BYTES_PER_PIXEL 3
#define MOD_ALIGN_MEMORY 4

// parsing file.
#define BLACK_COLOR 0
#define WHITE_COLOR 255
#define BMP_FILE_HEADER_SIZE 54

// bmp header offsets.
#define BMP_HEADER_OFFSET_B 0
#define BMP_HEADER_OFFSET_M 1
#define BMP_HEADER_OFFSET_TOTAL_SIZE 2
#define BMP_HEADER_OFFSET_RESERVED_FIELDS 6
#define BMP_HEADER_OFFSET_IMAGE_DATA_OFFSET 10
#define BMP_HEADER_OFFSET_DIB_HEADER_SIZE 14
#define BMP_HEADER_OFFSET_WIDTH_PIXELS 18
#define BMP_HEADER_OFFSET_HEIGHT_PIXELS 22
#define BMP_HEADER_OFFSET_COLOR_PLANES 26
#define BMP_HEADER_OFFSET_DOT_SIZE 28
#define BMP_HEADER_OFFSET_COMPREHENSION_METHOD 30
#define BMP_HEADER_OFFSET_IMAGE_SIZE 34
#define BMP_HEADER_OFFSET_HORIZONTAL_RESOLUTION 38
#define BMP_HEADER_OFFSET_VERTICAL_RESOLUTION 42
#define BMP_HEADER_OFFSET_COLOR_PALLETE 46
#define BMP_HEADER_OFFSET_COLOR_COUNT 50

// BMPfileException messages.
const char* BMP_EXCEPT_OPENING_ERROR = "Error while opening the bmp file. The file either not exists nor has been placed in another directory";
const char* BMP_EXCEPT_WRONG_TYPE = "Error, the file is not a BMP file.";
const char* BMP_EXCEPT_WRONG_BBP = "Error, the BMP file is not 24bbp. Cannot be loaded.";
const char* BMP_EXCEPT_COMPRESSION = "Error, the BMP has a compression method. It cannot have any compression methods.";
const char* BMP_EXCEPT_FAIL_TO_EXTRACT_NAME = "Error, a failure has been occur while the name was being extracting from path.";


BMPfile::BMPfile(const std::string path){
    path_ = BMPfile::is_exists(path) == true ? (std::string)path : throw BMPfileException(BMP_EXCEPT_OPENING_ERROR);
    filename_ = BMPfile::extract_filename_from_path();
    std::vector<unsigned char> temp_buffer;
    BMPfile::get_data_buffer(temp_buffer);
    BMPfile::header_ = (struct bitmap_header*) malloc(sizeof(struct bitmap_header));
    BMPfile::detailed_header_ = (struct dib_header*) malloc(sizeof(struct dib_header));
    BMPfile::init_header(temp_buffer);
    BMPfile::init_dib_header(temp_buffer);
    BMPfile::padding_ = BMPfile::set_padding();
    BMPfile::image_data_ = new pixel_24bpp* [BMPfile::detailed_header_->height_in_pixels];
    for(size_t i = 0; i < BMPfile::detailed_header_->height_in_pixels; ++i){
        BMPfile::image_data_[i] = new pixel_24bpp [BMPfile::detailed_header_->width_in_pixels];
    }
    BMPfile::fetch_image(temp_buffer);
}

BMPfile::~BMPfile(){
    for(size_t i = 0; i < BMPfile::get_detailed_header()->height_in_pixels; ++i){
        delete [] BMPfile::image_data_[i];
    }
    delete [] BMPfile::image_data_;
    free(BMPfile::header_);
    free(BMPfile::detailed_header_);
}

std::string BMPfile::get_path() const noexcept{ return BMPfile::path_; }
std::string BMPfile::get_filename() const noexcept{ return BMPfile::filename_; }
int BMPfile::get_padding() const noexcept { return BMPfile::padding_; }
struct bitmap_header* BMPfile::get_header() const noexcept {return BMPfile::header_; }
struct dib_header* BMPfile::get_detailed_header() const noexcept {return BMPfile::detailed_header_; }
struct pixel_24bpp** BMPfile::get_image_data() const noexcept { return BMPfile::image_data_; }

void BMPfile::print_values (int code=2) const{
    switch(code){
        case 0: break; // nothing gets printed out.
        case 1:        // prints detailed information.
            std::cout << "Current os using: " << (PLATFORM_NAME == 1 ? "windows" : "linux") << std::endl;
            std::cout << "Filename: " << BMPfile::get_filename() << std::endl;
            std::cout << std::endl;
            std::cout << "HEADER VALUES" << std::endl;
            std::cout << "\tB: " << BMPfile::get_header()->b << std::endl;
            std::cout << "\tM: " << BMPfile::get_header()->m << std::endl;
            std::cout << "\tTotal size (bytes): " << BMPfile::get_header()->total_size_in_bytes << std::endl;
            std::cout << "\tReserved fields: " << BMPfile::get_header()->reserved_fields << std::endl;
            std::cout << "\tImage offset: " << BMPfile::get_header()->image_data_offset << std::endl;
            std::cout << std::endl;
            std::cout << "DIB HEADER VALUES" << std::endl;
            std::cout << "\tDib header size: " << BMPfile::get_detailed_header()->dib_header_size << std::endl;
            std::cout << "\tWidth (pixels): " << BMPfile::get_detailed_header()->width_in_pixels << std::endl;
            std::cout << "\tHeight (pixels): " << BMPfile::get_detailed_header()->height_in_pixels << std::endl;
            std::cout << "\tColor planes: " << BMPfile::get_detailed_header()->color_planes << std::endl;
            std::cout << "\tDot size (bbp): " << BMPfile::get_detailed_header()->dot_size << std::endl;
            std::cout << "\tCompression Method: " << BMPfile::get_detailed_header()->compression_method << std::endl;
            std::cout << "\tImage size (bytes): " << BMPfile::get_detailed_header()->image_size_bytes << std::endl;
            std::cout << "\tHorizontal Resolution: " << BMPfile::get_detailed_header()->horizontal_resolution << std::endl;
            std::cout << "\tVertical Resolution: " << BMPfile::get_detailed_header()->vertical_resolution << std::endl;
            std::cout << "\tColor Pallete size: " << BMPfile::get_detailed_header()->color_pallete_size << std::endl;
            std::cout << "\tColor count: " << BMPfile::get_detailed_header()->color_count << std::endl;
            break;
        default:    // prints simple info.
            std::cout << "HEADER VALUES" << std::endl;
            std::cout << BMPfile::get_header()->b << " ";
            std::cout << BMPfile::get_header()->m << " ";
            std::cout << BMPfile::get_header()->total_size_in_bytes << " ";
            std::cout << BMPfile::get_header()->reserved_fields << " ";
            std::cout << BMPfile::get_header()->image_data_offset << " ";
            std::cout << std::endl << "DIB HEADER VALUES" << std::endl;
            std::cout << BMPfile::get_detailed_header()->dib_header_size << " ";
            std::cout << BMPfile::get_detailed_header()->width_in_pixels << " ";
            std::cout << BMPfile::get_detailed_header()->height_in_pixels << " ";
            std::cout << BMPfile::get_detailed_header()->color_planes << " ";
            std::cout << BMPfile::get_detailed_header()->dot_size << " ";
            std::cout << BMPfile::get_detailed_header()->compression_method << " ";
            std::cout << BMPfile::get_detailed_header()->image_size_bytes << " ";
            std::cout << BMPfile::get_detailed_header()->horizontal_resolution << " ";
            std::cout << BMPfile::get_detailed_header()->vertical_resolution << " ";
            std::cout << BMPfile::get_detailed_header()->color_pallete_size << " ";
            std::cout << BMPfile::get_detailed_header()->color_count << " ";
    }
}


int BMPfile::set_padding () {
// the size of each row in a bitmap must be % 4 = 0, a word
    int padd = 0;
    if ((BMPfile::get_detailed_header()->width_in_pixels*BYTES_PER_PIXEL)%MOD_ALIGN_MEMORY != 0){
        padd = MOD_ALIGN_MEMORY - ((BMPfile::get_detailed_header()->width_in_pixels*BYTES_PER_PIXEL)%MOD_ALIGN_MEMORY);
    }
    return padd;
}

bool BMPfile::is_exists (const std::string& path){
    std::ifstream f(path.c_str());
    return f.good();
}

std::string BMPfile::extract_filename_from_path(){
    std::string name;
    switch(PLATFORM_NAME){
        case 1: //"windows"
            name = BMPfile::get_path().substr(BMPfile::get_path().find_last_of("\\") + 1);
            break;
        case 2: //"linux"
            name = BMPfile::get_path().substr(BMPfile::get_path().find_last_of("/") + 1);
            break;
        default:
            throw BMPfileException(BMP_EXCEPT_FAIL_TO_EXTRACT_NAME);
    }
    return name;
}

void BMPfile::get_data_buffer(std::vector<unsigned char>& buff){
    std::ifstream current_file(BMPfile::get_path(), std::ios_base::binary);
    if (BMPfile::check_bmp_file()){
        while(current_file){ buff.push_back(current_file.get());}
    }
}

bool BMPfile::check_bmp_file(){
    // checks is a bmp file, no compressed and 24bbp.

    std::vector<unsigned char> magic_letters (2);
    std::ifstream current_file(BMPfile::get_path(), std::ios_base::binary);

    // check first the first 2 bytes that contains the magic letters BM.
    magic_letters[0] = current_file.get();
    magic_letters[1] = current_file.get();
    if (magic_letters[0] != 'B' || magic_letters[1] != 'M') throw BMPfileException(BMP_EXCEPT_WRONG_TYPE);

    std::vector<unsigned char> rest_header;
    size_t header_bytes_remaining = 52;
    while (header_bytes_remaining != 0){
        rest_header.push_back(current_file.get());
        --header_bytes_remaining;
    }

    uint16_t bits_per_pixel_format = (uint16_t)(rest_header[BMP_HEADER_OFFSET_DOT_SIZE-2] |
                                                rest_header[BMP_HEADER_OFFSET_DOT_SIZE-1] << 8);

    //std::cout << bits_per_pixel_format << std::endl;
    if (bits_per_pixel_format != 24) throw BMPfileException(BMP_EXCEPT_WRONG_BBP);

    uint32_t compression_format = (uint32_t)(rest_header[BMP_HEADER_OFFSET_COMPREHENSION_METHOD-2] |
                                             rest_header[BMP_HEADER_OFFSET_COMPREHENSION_METHOD-1] << 8 |
                                             rest_header[BMP_HEADER_OFFSET_COMPREHENSION_METHOD] << 16 |
                                             rest_header[BMP_HEADER_OFFSET_COMPREHENSION_METHOD+1] << 24);
    //std::cout << compression_format << std::endl;
    if (compression_format != 0) throw BMPfileException(BMP_EXCEPT_COMPRESSION);

    return true;
}

void BMPfile::init_header(std::vector<unsigned char>& buffer){
    BMPfile::get_header()->b = buffer[BMP_HEADER_OFFSET_B];
    BMPfile::get_header()->m = buffer[BMP_HEADER_OFFSET_M];
    BMPfile::get_header()->total_size_in_bytes = (uint32_t)(buffer[BMP_HEADER_OFFSET_TOTAL_SIZE] |
                                             buffer[BMP_HEADER_OFFSET_TOTAL_SIZE+1] << 8 |
                                             buffer[BMP_HEADER_OFFSET_TOTAL_SIZE+2] << 16 |
                                             buffer[BMP_HEADER_OFFSET_TOTAL_SIZE+3] << 24);
    BMPfile::get_header()->reserved_fields = (uint32_t)(buffer[BMP_HEADER_OFFSET_RESERVED_FIELDS] |
                                             buffer[BMP_HEADER_OFFSET_RESERVED_FIELDS+1] << 8 |
                                             buffer[BMP_HEADER_OFFSET_RESERVED_FIELDS+2] << 16 |
                                             buffer[BMP_HEADER_OFFSET_RESERVED_FIELDS+3] << 24);
    BMPfile::get_header()->image_data_offset =(uint32_t)(buffer[BMP_HEADER_OFFSET_IMAGE_DATA_OFFSET] |
                                             buffer[BMP_HEADER_OFFSET_IMAGE_DATA_OFFSET+1] << 8 |
                                             buffer[BMP_HEADER_OFFSET_IMAGE_DATA_OFFSET+2] << 16 |
                                             buffer[BMP_HEADER_OFFSET_IMAGE_DATA_OFFSET+3] << 24);
}

void BMPfile::init_dib_header(std::vector<unsigned char>& buffer){
    BMPfile::get_detailed_header()->dib_header_size = (uint32_t)(buffer[BMP_HEADER_OFFSET_DIB_HEADER_SIZE] |
                                             buffer[BMP_HEADER_OFFSET_DIB_HEADER_SIZE+1] << 8 |
                                             buffer[BMP_HEADER_OFFSET_DIB_HEADER_SIZE+2] << 16 |
                                             buffer[BMP_HEADER_OFFSET_DIB_HEADER_SIZE+3] << 24);

    BMPfile::get_detailed_header()->width_in_pixels = (uint32_t)(buffer[BMP_HEADER_OFFSET_WIDTH_PIXELS] |
                                             buffer[BMP_HEADER_OFFSET_WIDTH_PIXELS+1] << 8 |
                                             buffer[BMP_HEADER_OFFSET_WIDTH_PIXELS+2] << 16 |
                                             buffer[BMP_HEADER_OFFSET_WIDTH_PIXELS+3] << 24);

    BMPfile::get_detailed_header()->height_in_pixels = (uint32_t)(buffer[BMP_HEADER_OFFSET_HEIGHT_PIXELS] |
                                             buffer[BMP_HEADER_OFFSET_HEIGHT_PIXELS+1] << 8 |
                                             buffer[BMP_HEADER_OFFSET_HEIGHT_PIXELS+2] << 16 |
                                             buffer[BMP_HEADER_OFFSET_HEIGHT_PIXELS+3] << 24);

    BMPfile::get_detailed_header()->color_planes = (uint16_t)(buffer[BMP_HEADER_OFFSET_COLOR_PLANES] |
                                             buffer[BMP_HEADER_OFFSET_COLOR_PLANES+1] << 8);

    BMPfile::get_detailed_header()->dot_size = (uint16_t)(buffer[BMP_HEADER_OFFSET_DOT_SIZE] |
                                             buffer[BMP_HEADER_OFFSET_DOT_SIZE+1] << 8);

    BMPfile::get_detailed_header()->compression_method = (uint32_t)(buffer[BMP_HEADER_OFFSET_COMPREHENSION_METHOD] |
                                             buffer[BMP_HEADER_OFFSET_COMPREHENSION_METHOD+1] << 8 |
                                             buffer[BMP_HEADER_OFFSET_COMPREHENSION_METHOD+2] << 16 |
                                             buffer[BMP_HEADER_OFFSET_COMPREHENSION_METHOD+3] << 24);

    BMPfile::get_detailed_header()->image_size_bytes = (uint32_t)(buffer[BMP_HEADER_OFFSET_IMAGE_SIZE] |
                                             buffer[BMP_HEADER_OFFSET_IMAGE_SIZE+1] << 8 |
                                             buffer[BMP_HEADER_OFFSET_IMAGE_SIZE+2] << 16 |
                                             buffer[BMP_HEADER_OFFSET_IMAGE_SIZE+3] << 24);

    BMPfile::get_detailed_header()->horizontal_resolution = (uint32_t)(buffer[BMP_HEADER_OFFSET_HORIZONTAL_RESOLUTION] |
                                             buffer[BMP_HEADER_OFFSET_HORIZONTAL_RESOLUTION+1] << 8 |
                                             buffer[BMP_HEADER_OFFSET_HORIZONTAL_RESOLUTION+2] << 16 |
                                             buffer[BMP_HEADER_OFFSET_HORIZONTAL_RESOLUTION+3] << 24);

    BMPfile::get_detailed_header()->vertical_resolution = (uint32_t)(buffer[BMP_HEADER_OFFSET_VERTICAL_RESOLUTION] |
                                             buffer[BMP_HEADER_OFFSET_VERTICAL_RESOLUTION+1] << 8 |
                                             buffer[BMP_HEADER_OFFSET_VERTICAL_RESOLUTION+2] << 16 |
                                             buffer[BMP_HEADER_OFFSET_VERTICAL_RESOLUTION+3] << 24);

    BMPfile::get_detailed_header()->color_pallete_size = (uint32_t)(buffer[BMP_HEADER_OFFSET_COLOR_PALLETE] |
                                             buffer[BMP_HEADER_OFFSET_COLOR_PALLETE+1] << 8 |
                                             buffer[BMP_HEADER_OFFSET_COLOR_PALLETE+2] << 16 |
                                             buffer[BMP_HEADER_OFFSET_COLOR_PALLETE+3] << 24);

    BMPfile::get_detailed_header()->color_count = (uint32_t)(buffer[BMP_HEADER_OFFSET_COLOR_COUNT] |
                                             buffer[BMP_HEADER_OFFSET_COLOR_COUNT+1] << 8 |
                                             buffer[BMP_HEADER_OFFSET_COLOR_COUNT+2] << 16 |
                                             buffer[BMP_HEADER_OFFSET_COLOR_COUNT+3] << 24);
}

void BMPfile::fetch_image(std::vector<unsigned char>& buffer){
//BMP_FILE_HEADER_SIZE
    for(size_t i = 0; i < BMPfile::get_detailed_header()->height_in_pixels; ++i){
        for(size_t j = 0; j < BMPfile::get_detailed_header()->width_in_pixels; ++j){
            int pixel_index = i*(BMPfile::get_detailed_header()->width_in_pixels * BYTES_PER_PIXEL +
                                    BMPfile::get_padding()) + j*BYTES_PER_PIXEL + BMPfile::get_header()->image_data_offset;
            BMPfile::get_image_data()[i][j].blue = (uint8_t)buffer[pixel_index];
            BMPfile::get_image_data()[i][j].green = (uint8_t)buffer[pixel_index+1];
            BMPfile::get_image_data()[i][j].red = (uint8_t)buffer[pixel_index+2];
        }
    }
}

void BMPfile::generate_point_file() const{
    // check performance struct vs std::array    std::vector<bitmap_point2> total_num_points;
    std::vector<bitmap_point> total_num_points;
    for (size_t i = 0; i < BMPfile::get_detailed_header()->height_in_pixels; ++i){
        for (size_t j = 0; j < BMPfile::get_detailed_header()->width_in_pixels; ++j){
            if (BMPfile::get_image_data()[i][j].blue == BLACK_COLOR &&
                BMPfile::get_image_data()[i][j].green == BLACK_COLOR &&
                BMPfile::get_image_data()[i][j].red == BLACK_COLOR){
                //bitmap_point2 current_point = {j, i};
                bitmap_point current_point = {j, i};
                total_num_points.push_back(current_point);
            }
        }
    }
    size_t lastindex = BMPfile::get_filename().find_last_of(".");
    std::string rawname = BMPfile::get_filename().substr(0, lastindex);
    std::string new_name = "res_" + rawname + ".txt";

    std::ofstream outfile(new_name);
    outfile << total_num_points.size() << std::endl;
    for(size_t i = 0; i < total_num_points.size(); ++i){
        outfile << total_num_points[i].x_coord << " " << total_num_points[i].y_coord << std::endl;
        //outfile << total_num_points[i][0] << " " << total_num_points[i][1] << std::endl;

    }
    outfile.close();
}

void BMPfile::generate_bmp_file() const{
    uint8_t value_added = 0;
    std::string new_name = "generated_from_" + BMPfile::get_filename();
    // write in binary.
    std::ofstream outfile(new_name, std::ios_base::binary);

    outfile.write(reinterpret_cast<char*>(&BMPfile::get_header()->b), sizeof(unsigned char));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_header()->m), sizeof(unsigned char));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_header()->total_size_in_bytes), sizeof(uint32_t));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_header()->reserved_fields), sizeof(uint32_t));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_header()->image_data_offset), sizeof(uint32_t));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_detailed_header()->dib_header_size), sizeof(uint32_t));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_detailed_header()->width_in_pixels), sizeof(uint32_t));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_detailed_header()->height_in_pixels), sizeof(uint32_t));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_detailed_header()->color_planes), sizeof(uint16_t));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_detailed_header()->dot_size), sizeof(uint16_t));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_detailed_header()->compression_method), sizeof(uint32_t));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_detailed_header()->image_size_bytes), sizeof(uint32_t));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_detailed_header()->horizontal_resolution), sizeof(uint32_t));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_detailed_header()->vertical_resolution), sizeof(uint32_t));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_detailed_header()->color_pallete_size), sizeof(uint32_t));
    outfile.write(reinterpret_cast<char*>(&BMPfile::get_detailed_header()->color_count), sizeof(uint32_t));

    // padding must be added.
    for(size_t i = 0; i < BMPfile::get_detailed_header()->height_in_pixels; ++i){
        for(size_t j = 0; j < BMPfile::get_detailed_header()->width_in_pixels; ++j){

            outfile.write(reinterpret_cast<char*>(&BMPfile::get_image_data()[i][j].blue), sizeof(uint8_t));
            outfile.write(reinterpret_cast<char*>(&BMPfile::get_image_data()[i][j].green), sizeof(uint8_t));
            outfile.write(reinterpret_cast<char*>(&BMPfile::get_image_data()[i][j].red), sizeof(uint8_t));
        }
        // add padding.
        for(uint8_t k = 0; k < (uint8_t)BMPfile::get_padding(); ++k){
            //outfile << (unsigned char)value_added;
            outfile.write(reinterpret_cast<char*>(&value_added), sizeof(uint8_t));
        }
    }
    outfile.close();
}