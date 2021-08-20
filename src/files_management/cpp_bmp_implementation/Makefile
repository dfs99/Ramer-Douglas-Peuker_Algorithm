# g++ -c bmp_parser.cpp  // compiles the source code but not links it. '-c' Returns an
# object file.

#CC=g++
#CPPFLAGS= -c
#SRCS = $(wildcard *.c)
#OBJS = $(patsubst %.c obj/%.o, $(SRCS))

#obj/*.o: $(SRCS)
#	$(CC) $(CPPFLAGS) $@

run:
	g++ -g bmp_parser.cpp
	./a.out

clean:
	rm -r a.out aux.txt