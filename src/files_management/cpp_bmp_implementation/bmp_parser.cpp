#include <iostream>
#include <fstream>
#include <vector>
// BMP HEADER = bitmap header + dib header
// bpp bits per pixel

#define BMP_HEADER_SIZE 54
#define BITMAP_HEADER_SIZE 14
#define DIB_HEADER_SIZE 40  // bitmap information header



// se estan usando

#define BYTES_PER_PIXEL 3
#define MOD_ALIGN_MEMORY 4

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


struct pixel_24bpp{
    // unsigned ints 8 bits => 1 byte
    // (B, G, R) Format
    uint8_t blue;
    uint8_t green;
    uint8_t red;
};

// 14 bytes.
struct bitmap_header{
    unsigned char b;
    unsigned char m;
    uint32_t total_size_in_bytes;
    uint32_t reserved_fields;   // si se genera manualmente puede ponerse como 0, varia el valor
    // dependiendo de la aplicación que lo ha creado.
    uint32_t image_data_offset;
};

// 40 bytes.
struct dib_header{
// detailed info about the BMP file.
    uint32_t dib_header_size;   // 40
    uint32_t width_in_pixels;
    uint32_t height_in_pixels;
    uint16_t color_planes;    // must be 1
    uint16_t dot_size;        // num bits per pixel. 1, 4, 8, 16, 24 and 32.
    uint32_t compression_method;
    uint32_t image_size_bytes;
    uint32_t horizontal_resolution; // pixel per metre.
    uint32_t vertical_resolution; // pixel per metre.
    uint32_t color_pallete_size;
    uint32_t color_count;
};

class BMPfile{
    public:
        // no default constructor
        BMPfile() = delete;

        BMPfile(const std::string given_filename){
            filename = BMPfile::is_exists(given_filename) == true ? (std::string)given_filename : "";
            // eliminar mmry
            std::vector<unsigned char> temp_buffer;
            BMPfile::get_data_buffer(temp_buffer);
            // eliminar la memoria reservada.
            BMPfile::header = (struct bitmap_header*) malloc(sizeof(struct bitmap_header));
            BMPfile::detailed_header = (struct dib_header*) malloc(sizeof(struct dib_header));
            BMPfile::init_header(temp_buffer);
            BMPfile::init_dib_header(temp_buffer);

            BMPfile::padding = BMPfile::set_padding();

            BMPfile::image_data = new pixel_24bpp* [BMPfile::detailed_header->height_in_pixels];
            for(size_t i = 0; i < BMPfile::detailed_header->height_in_pixels; ++i){
                BMPfile::image_data[i] = new pixel_24bpp [BMPfile::detailed_header->width_in_pixels];
            }
            BMPfile::fetch_image(temp_buffer);
        }

        void print_values(){
            std::cout << "HEADER VALUES" << std::endl;
            std::cout << BMPfile::header->b << " ";
            std::cout << BMPfile::header->m << " ";
            std::cout << BMPfile::header->total_size_in_bytes << " ";
            std::cout << BMPfile::header->reserved_fields << " ";
            std::cout << BMPfile::header->image_data_offset << " ";
            std::cout << std::endl << "DIB HEADER VALUES" << std::endl;
            std::cout << BMPfile::detailed_header->dib_header_size << " ";
            std::cout << BMPfile::detailed_header->width_in_pixels << " ";
            std::cout << BMPfile::detailed_header->height_in_pixels << " ";
            std::cout << BMPfile::detailed_header->color_planes << " ";
            std::cout << BMPfile::detailed_header->dot_size << " ";
            std::cout << BMPfile::detailed_header->compression_method << " ";
            std::cout << BMPfile::detailed_header->image_size_bytes << " ";
            std::cout << BMPfile::detailed_header->horizontal_resolution << " ";
            std::cout << BMPfile::detailed_header->vertical_resolution << " ";
            std::cout << BMPfile::detailed_header->color_pallete_size << " ";
            std::cout << BMPfile::detailed_header->color_count << " ";
            std::cout << std::endl << "IMAGE DATA" << std::endl;
            for(size_t i = 0; i < BMPfile::detailed_header->height_in_pixels; ++i){
                for(size_t j = 0; j < BMPfile::detailed_header->width_in_pixels; ++j){
                    std::cout << "Pixel: b" << BMPfile::image_data[i][j].blue << " g" << BMPfile::image_data[i][j].green
                    << " r" << BMPfile::image_data[i][j].red << " ";
                }
                std::cout << std::endl;
            }
        }

    private:
        std::string filename;
        int padding;
        struct bitmap_header *header;
        struct dib_header *detailed_header;
        struct pixel_24bpp **image_data;

        int set_padding(){
        // the size of each row in a bitmap must be % 4 = 0, a word
            int padd = 0;
            if (/*(BMPfile::detailed_header->width_in_pixels*BYTES_PER_PIXEL)%MOD_ALIGN_MEMORY)*/ 0 != 0){
                padd = MOD_ALIGN_MEMORY - ((BMPfile::detailed_header->width_in_pixels*BYTES_PER_PIXEL)%MOD_ALIGN_MEMORY);
            }
            return padd;
        }

        bool is_exists(const std::string& name){
            std::ifstream f(name.c_str());
            return f.good();
        }

        void get_data_buffer(std::vector<unsigned char>& buff){
            if (BMPfile::filename != ""){
                std::ifstream current_file(BMPfile::filename, std::ios_base::binary);

                if (BMPfile::check_bmp_file()){
                    while(current_file){ buff.push_back(current_file.get());}
                }/*else{
                    // lanzar excepcion: existe fichero pero no es bmp
                }
                */
            }/*else{
                // lanzar una excepcion. no existe fichero.
            }*/
        }

        bool check_bmp_file(){
            // problema a la hora de leer la info.
            std::ifstream current_file(BMPfile::filename, std::ios_base::binary);
            // check only the first 2 bytes that contains the magic letters BM.
            std::vector<unsigned char> magic_letters {2};
            magic_letters[0] = current_file.get();
            magic_letters[1] = current_file.get();
            //cout << "Magic letters: " << magic_letters[0] << " " << magic_letters[1] << endl;
            return (magic_letters[0] == 'B' && magic_letters[1] == 'M') ? true : false;
        }

        void init_header(std::vector<unsigned char>& buffer){
            BMPfile::header->b = buffer[BMP_HEADER_OFFSET_B];
            BMPfile::header->m = buffer[BMP_HEADER_OFFSET_M];
            BMPfile::header->total_size_in_bytes = (uint32_t)(buffer[BMP_HEADER_OFFSET_TOTAL_SIZE] |
                                                     buffer[BMP_HEADER_OFFSET_TOTAL_SIZE+1] << 8 |
                                                     buffer[BMP_HEADER_OFFSET_TOTAL_SIZE+2] << 16 |
                                                     buffer[BMP_HEADER_OFFSET_TOTAL_SIZE+3] << 24);
            BMPfile::header->reserved_fields = (uint32_t)(buffer[BMP_HEADER_OFFSET_RESERVED_FIELDS] |
                                                     buffer[BMP_HEADER_OFFSET_RESERVED_FIELDS+1] << 8 |
                                                     buffer[BMP_HEADER_OFFSET_RESERVED_FIELDS+2] << 16 |
                                                     buffer[BMP_HEADER_OFFSET_RESERVED_FIELDS+3] << 24);
            BMPfile::header->image_data_offset =(uint32_t)(buffer[BMP_HEADER_OFFSET_IMAGE_DATA_OFFSET] |
                                                     buffer[BMP_HEADER_OFFSET_IMAGE_DATA_OFFSET+1] << 8 |
                                                     buffer[BMP_HEADER_OFFSET_IMAGE_DATA_OFFSET+2] << 16 |
                                                     buffer[BMP_HEADER_OFFSET_IMAGE_DATA_OFFSET+3] << 24);
        }

        void init_dib_header(std::vector<unsigned char>& buffer){
            BMPfile::detailed_header->dib_header_size = (uint32_t)(buffer[BMP_HEADER_OFFSET_DIB_HEADER_SIZE] |
                                                     buffer[BMP_HEADER_OFFSET_DIB_HEADER_SIZE+1] << 8 |
                                                     buffer[BMP_HEADER_OFFSET_DIB_HEADER_SIZE+2] << 16 |
                                                     buffer[BMP_HEADER_OFFSET_DIB_HEADER_SIZE+3] << 24);

            BMPfile::detailed_header->width_in_pixels = (uint32_t)(buffer[BMP_HEADER_OFFSET_WIDTH_PIXELS] |
                                                     buffer[BMP_HEADER_OFFSET_WIDTH_PIXELS+1] << 8 |
                                                     buffer[BMP_HEADER_OFFSET_WIDTH_PIXELS+2] << 16 |
                                                     buffer[BMP_HEADER_OFFSET_WIDTH_PIXELS+3] << 24);

            BMPfile::detailed_header->height_in_pixels = (uint32_t)(buffer[BMP_HEADER_OFFSET_HEIGHT_PIXELS] |
                                                     buffer[BMP_HEADER_OFFSET_HEIGHT_PIXELS+1] << 8 |
                                                     buffer[BMP_HEADER_OFFSET_HEIGHT_PIXELS+2] << 16 |
                                                     buffer[BMP_HEADER_OFFSET_HEIGHT_PIXELS+3] << 24);

            BMPfile::detailed_header->color_planes = (uint16_t)(buffer[BMP_HEADER_OFFSET_COLOR_PLANES] |
                                                     buffer[BMP_HEADER_OFFSET_COLOR_PLANES+1] << 8);

            BMPfile::detailed_header->dot_size = (uint16_t)(buffer[BMP_HEADER_OFFSET_DOT_SIZE] |
                                                     buffer[BMP_HEADER_OFFSET_DOT_SIZE+1] << 8);

            BMPfile::detailed_header->compression_method = (uint32_t)(buffer[BMP_HEADER_OFFSET_COMPREHENSION_METHOD] |
                                                     buffer[BMP_HEADER_OFFSET_COMPREHENSION_METHOD+1] << 8 |
                                                     buffer[BMP_HEADER_OFFSET_COMPREHENSION_METHOD+2] << 16 |
                                                     buffer[BMP_HEADER_OFFSET_COMPREHENSION_METHOD+3] << 24);

            BMPfile::detailed_header->image_size_bytes = (uint32_t)(buffer[BMP_HEADER_OFFSET_IMAGE_SIZE] |
                                                     buffer[BMP_HEADER_OFFSET_IMAGE_SIZE+1] << 8 |
                                                     buffer[BMP_HEADER_OFFSET_IMAGE_SIZE+2] << 16 |
                                                     buffer[BMP_HEADER_OFFSET_IMAGE_SIZE+3] << 24);

            BMPfile::detailed_header->horizontal_resolution = (uint32_t)(buffer[BMP_HEADER_OFFSET_HORIZONTAL_RESOLUTION] |
                                                     buffer[BMP_HEADER_OFFSET_HORIZONTAL_RESOLUTION+1] << 8 |
                                                     buffer[BMP_HEADER_OFFSET_HORIZONTAL_RESOLUTION+2] << 16 |
                                                     buffer[BMP_HEADER_OFFSET_HORIZONTAL_RESOLUTION+3] << 24);

            BMPfile::detailed_header->vertical_resolution = (uint32_t)(buffer[BMP_HEADER_OFFSET_VERTICAL_RESOLUTION] |
                                                     buffer[BMP_HEADER_OFFSET_VERTICAL_RESOLUTION+1] << 8 |
                                                     buffer[BMP_HEADER_OFFSET_VERTICAL_RESOLUTION+2] << 16 |
                                                     buffer[BMP_HEADER_OFFSET_VERTICAL_RESOLUTION+3] << 24);

            BMPfile::detailed_header->color_pallete_size = (uint32_t)(buffer[BMP_HEADER_OFFSET_COLOR_PALLETE] |
                                                     buffer[BMP_HEADER_OFFSET_COLOR_PALLETE+1] << 8 |
                                                     buffer[BMP_HEADER_OFFSET_COLOR_PALLETE+2] << 16 |
                                                     buffer[BMP_HEADER_OFFSET_COLOR_PALLETE+3] << 24);

            BMPfile::detailed_header->color_count = (uint32_t)(buffer[BMP_HEADER_OFFSET_COLOR_COUNT] |
                                                     buffer[BMP_HEADER_OFFSET_COLOR_COUNT+1] << 8 |
                                                     buffer[BMP_HEADER_OFFSET_COLOR_COUNT+2] << 16 |
                                                     buffer[BMP_HEADER_OFFSET_COLOR_COUNT+3] << 24);
        }

        void fetch_image(std::vector<unsigned char>& buffer){
            for(size_t i = 0; i < BMPfile::detailed_header->height_in_pixels; ++i){
                for(size_t j = 0; j < BMPfile::detailed_header->width_in_pixels; ++j){
                    int pixel_index = i*(BMPfile::detailed_header->width_in_pixels * BYTES_PER_PIXEL +
                                            BMPfile::padding) + j*BYTES_PER_PIXEL;
                    BMPfile::image_data[i][j].blue = (uint8_t)buffer[pixel_index];
                    BMPfile::image_data[i][j].green = (uint8_t)buffer[pixel_index+1];
                    BMPfile::image_data[i][j].red = (uint8_t)buffer[pixel_index+2];
                }
            }
        }

};


/*
bool check_bmp_file(const std::string given_filename){
    std::ifstream current_file(given_filename, std::ios_base::binary);
    // check only the first 2 bytes that contains the magic letters BM.
    std::vector<unsigned char> magic_letters {2};
    magic_letters[0] = current_file.get();
    magic_letters[1] = current_file.get();
    //cout << "Magic letters: " << magic_letters[0] << " " << magic_letters[1] << endl;
    return (magic_letters[0] == 'B' && magic_letters[1] == 'M') ? true : false;


    std::vector<unsigned char> buffer;
    while(current_file){ buffer.push_back(current_file.get());}
    cout << endl;
    cout << "ANother aproximation:" << endl;
    int n;
    for(size_t i = 0; i < buffer.size(); ++i){
        if (i == 0) cout << buffer[i] << endl;
        if (i == 1) cout << buffer[i] << endl;
        if (i == 6) n = (int)(buffer[2] | buffer[3] << 8 | buffer [4] << 16 | buffer[5] << 24);
    }

    cout << "Total bytes: " << n << endl;
    if (n >= 1105906) cout << "si funcional!!" << endl;
    for (int j = 0; j < n; ++j){
        cout << j << " ";
    }
    //1.105.906
    //1.105.906
}*/


using namespace std;
int main(){
    /*char b = 'B';
    char m = 'M';
    int b_int = b;
    int m_int = m;
    cout << "BMP PARSER" << endl;
    cout << "B value: " << b_int << " => HEX: 0x" << hex << b_int << endl;
    cout << "M value: " << m_int << " => HEX: 0x" << hex << m_int << endl;
    //const string filename = "spain_map.bmp";
    struct BMP_file current_file;
    bool res = check_bmp_file(filename);
    cout << res;*/
    const string filename = "spain_map.bmp";
    BMPfile my_file {filename};
    my_file.print_values();
}