PROG_NAME=tempsense
MAKEFLAGS = --no-builtin-rules
# We don't use any suffix rules
.SUFFIXES :

LIBS     = -lpthread -lrt

MODULES=common server client
SOURCE_DIRS=$(addprefix src/, $(MODULES))
BUILD_DIR=build/
INCLUDE=src/include

vpath %.h $(INCLUDE)
vpath %.c $(SOURCE_DIRS)
VPATH=src:$(SOURCE_DIRS)

CFLAGS = -Isrc
CC_OPTS = $(CFLAGS) $($*_CC_OPTS) -g -Wall
CC =gcc

all : server.o main.o common.o
	$(addprefix $(CROSS), $(CC)) $(CFLAGS) -g -o $(PROG_NAME) $^ $(LIBS)

client : client.o
	$(addprefix $(CROSS), $(CC)) $(CFLAGS) -g -o client $^ $(LIBS)

%.o : %.c
	$(addprefix $(CROSS), $(CC)) $(CC_OPTS) -c $< -o $@

clean :
	@rm -rf *.o *.a $(PROG_NAME) client

.PHONY : clean all client
