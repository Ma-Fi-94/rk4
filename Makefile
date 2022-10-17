SRC=rk4
DEST=rk4
CC=clang
CFLAGS=-Wall -Wextra -Wpedantic

PYTHONLIB=rk4lib.py

elf: 
	${CC} ${SRC}.c ${CC_FLAGS} -o ${DEST}.elf

run: elf
	./${DEST}.elf

grind: elf
	valgrind ./${DEST}.elf

so:
	${CC} ${SRC}.c -fPIC -shared -o ${DEST}.so

pythonlib: so
	# Code style
	importchecker ${PYTHONLIB}
	isort ${PYTHONLIB}
	yapf -i ${PYTHONLIB}
	
	# Linting
	pylint ${PYTHONLIB}
	
	# Type checking
	mypy ${PYTHONLIB}
	
	# Testing
	py.test --cov=. --cov-report term-missing  -v
