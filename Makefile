SRC=rk4.c
DEST=rk4.elf
CC=clang
CFLAGS=-Wall -Wextra -Wpedantic

all: 
	${CC} ${SRC} ${CC_FLAGS} -o ${DEST}
	./${DEST}

grind:
	${CC} ${SRC} ${CC_FLAGS} -g -o ${DEST}
	valgrind ./${DEST}
