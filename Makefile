SRC=rk4.c
DEST=rk4
CC=clang
CFLAGS=-Wall -Wextra -Wpedantic

all: 
	${CC} ${SRC} ${CC_FLAGS} -o ${DEST}.elf

run: all
	./${DEST}.elf
grind:
	${CC} ${SRC} ${CC_FLAGS} -g -o ${DEST}.elf
	valgrind ./${DEST}.elf

so:
	${CC} ${SRC} -fPIC -shared -o ${DEST}.so
