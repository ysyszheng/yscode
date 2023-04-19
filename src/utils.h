# ifndef UTILS_H
# define UTILS_H

#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <termios.h>
#include <unistd.h>

enum state {NORMAL, INSERT, VISUAL, COMMAND};

struct termios orig_termios;

void die(const char *s);
void disableRawMode();
void enableRawMode();

# endif /* UTILS_H */
