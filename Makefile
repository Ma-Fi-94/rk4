SRC=rk4
DEST=rk4
CC=clang
CFLAGS=-Wall -Wextra -Wpedantic

PYTHONLIB=rk4.py

elf: 
	${CC} ${SRC}.c ${CC_FLAGS} -o ${DEST}.elf

run: elf
	./${DEST}.elf

grind: elf
	valgrind ./${DEST}.elf

so:
	${CC} ${SRC}.c -fPIC -shared -o ${DEST}.so

pythonlib:
	importchecker ${PYTHONLIB}
	isort ${PYTHONLIB}
	yapf -i ${PYTHONLIB}
	pylint ${PYTHONLIB}


