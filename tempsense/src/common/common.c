/*
 * common.c
 *
 *  Created on: Apr 22, 2014
 *      Author: guru
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>

#include "include/common.h"

int verbose = 0;

inline void _panic(const char *fmt, ...) {
	va_list arg;
    va_start(arg, fmt);
    vfprintf(stderr, fmt, arg);
    va_end(arg);
	exit(-1);
}

