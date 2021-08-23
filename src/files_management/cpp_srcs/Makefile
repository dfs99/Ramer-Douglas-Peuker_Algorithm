CPP=g++
CPPFLAGS= -g -Wall
CPPVERSION = -std=c++17 -O3

# directories.
SRC_DIR = srcs
OBJ_DIR =objs
HEADERS_DIR = headers
BIN_DIR = bin

# extracting files.
SRCS = $(wildcard $(SRC_DIR)/*.cpp)
HEADERS = $(wildcard $(HEADERS_DIR)/*.h)
OBJS = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRCS))
BIN = $(BIN_DIR)/main

all: $(BIN)

$(BIN) : $(OBJS)
	$(CPP)	$(CPPFLAGS) $(CPPVERSION) -o $@ $(OBJS)

$(OBJ_DIR)/%.o : $(SRC_DIR)/%.cpp $(HEADERS)
	$(CPP) $(CPPVERSION) -c $< -o $@

clean:
	rm -r $(OBJS)
	rm -r $(BIN)
	rm -rf $(BIN_DIR)/res_* $(BIN_DIR)/generated_from_* $(BIN_DIR)/rdp_data_*