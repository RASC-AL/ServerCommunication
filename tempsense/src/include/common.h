/*
 * common.h
 *
 *  Created on: Apr 22, 2014
 *      Author: guru
 */

#ifndef COMMON_H_
#define COMMON_H_

#include <time.h>
#include <unistd.h>
#include <signal.h>
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>
#include <inttypes.h>

#define unlikely(x)		__builtin_expect(!!(x), 0)
#define likely(x)		__builtin_expect(!!(x), 1)

typedef unsigned long long u64;
typedef long long i64;
typedef unsigned int u32;

extern int verbose;

#define panic(fmt,...)	_panic(fmt, ##__VA_ARGS__);

#define VERBOSE(...) \
{ \
	if(verbose) \
		printf(__VA_ARGS__); \
}

void _panic(const char *fmt, ...);

#endif /* COMMON_H_ */
