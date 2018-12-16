CC := gcc
CFLAGS := -g -Wall
LDFLAGS := -g
HEADERS := 
EXE := prev
SOURCES := pr_buggy.o prmain.o

ALL: ${EXE}

pr_buggy.o: pr_buggy.c ${HEADERS} Makefile
	${CC} ${LDFLAGS} -c -Wall -o $@ $< >& /dev/null

%.o: %.c ${HEADERS} Makefile
	${CC} ${LDFLAGS} -c ${CFLAGS} -o $@ $<

${EXE}: ${SOURCES}
	$(CC) ${SOURCES} -o ${EXE} ${LDFLAGS}

clean::
	rm -f ${SOURCES} ${EXE}

