CC=gcc
CFLAGS=-g -Wall

HEADERS=mp8.h Makefile imageData.h lodepng.h
OBJECTS=testing.o lodepng.o imageData.o mp8.o mp8recurse.o
FLOOD_OBJECTS=testing.o lodepng.o imageData.o mp8.o goldrecurse.c
RECURSE_OBJECTS=testing.o lodepng.o imageData.o gold.c mp8recurse.o

all: grader flood_grader recurse_grader

grader: ${OBJECTS}
	${CC} ${CFLAGS} ${OBJECTS} -o grader

flood_grader: ${OBJECTS}
	${CC} ${CFLAGS} ${FLOOD_OBJECTS} -o flood_grader

recurse_grader: ${OBJECTS}
	${CC} ${CFLAGS} ${RECURSE_OBJECTS} -o recurse_grader

%.o: %.c ${HEADERS}
	${CC} -c ${CFLAGS} $< -o $@

clean::
	rm -f *.o *~

clear: clean
	rm -f grader flood_grader recurse_grader
