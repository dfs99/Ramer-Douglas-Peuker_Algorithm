#include <iostream>
#include <fstream>
#include <vector>
// BMP HEADER = bitmap header + dib header
// bpp bits per pixel

#define BMP_HEADER_SIZE 54
#define BITMAP_HEADER_SIZE 14
#define DIB_HEADER_SIZE 40  // bitmap information header

struct pixel_8bpp{
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

struct BMP_file{
    struct bitmap_header header;
    struct dib_header detailed_header;
    struct pixel_8bpp **image_data;
};


union intc32 {
    char c[4];
    int v;
};

int charsToInt(char a, char b, char c, char d) {
    intc32 r = { { a, b, c, d } };
    return r.v;
}



void check_bmp_file(const std::string given_filename){
    using namespace std;
    std::ifstream current_file(given_filename, std::ios_base::binary);
    std::vector<unsigned char> buffer;
    int i = 0;
    while(current_file)
    {
        buffer.push_back(current_file.get());
        ++i;
    }
    int a = 1;
    int b = 1;
    int c = 1;
    std::vector<unsigned char> aux;
    for (std::vector<unsigned char>::iterator it = buffer.begin() ; it != buffer.end(); ++it){
        if(c == 6){
            cout << charsToInt(aux[0], aux[1], aux[2], aux[3]) << endl;
            break;
        }
        if (a == 1) cout << *it << endl;
        if (b == 2) cout << *it << endl;

        if (c < 6 && c > 2){
            aux.push_back(*it);
        }
        //cout << (int)*it << ' ';
        ++a;
        ++b;
        ++c;
    }
    cout << endl;
    //1.105.906
    //1.105.906
    //std::vector<char> buffer (std::istreambuf_iterator<char>(current_file), std::istreambuf_iterator<char>());
    //cout << buffer << endl;
    //for (std::vector<int>::iterator it = buffer.begin() ; it != buffer.end(); ++it){
    //    cout << *it << ' ';
    //}
    /*
    string line;
    cout << "Starting..." << endl;
    while(current_file){
        getline(current_file, line);
        // cout << line << endl;
        for(size_t i = 0; i < line.length(); ++i){
            cout << (unsigned char)line[i] << " ";
            cout << (int)line[i] << " ";
            cout << (unsigned char)line[i] << " ";
        }
        cout << endl;
    }
    cout << "Ending" << endl;
    // cout << current_file[0];*/
}


using namespace std;
int main(){
    char b = 'B';
    char m = 'M';
    int b_int = b;
    int m_int = m;
    cout << "BMP PARSER" << endl;
    cout << "B value: " << b_int << " => HEX: 0x" << hex << b_int << endl;
    cout << "M value: " << m_int << " => HEX: 0x" << hex << m_int << endl;
    const string filename = "spain_map.bmp";
    struct BMP_file current_file;
    check_bmp_file(filename);
}