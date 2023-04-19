CC = gcc
CXX = g++
CFLAG = -Wall -Wextra -pedantic -std=c99
SOURCES = ../src/meow.c \
					../src/utils.c
HEADERS = ../src/utils.h
TARGETS = ./bin/meow

mewo: $(SOURCE) $(HEADERS)
	$(CC) $(CFLAG) -o $(TARGETS) $(SOURCES)

clean:
	rm -f mewo