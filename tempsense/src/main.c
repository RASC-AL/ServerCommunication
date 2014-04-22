/*
 * main.c
 *
 *  Created on: Apr 22, 2014
 *      Author: guru
 */

#include <sys/socket.h>
#include <arpa/inet.h>
#include <sys/wait.h>

#include "include/common.h"
#include "include/server.h"


static struct timespec delay = {1,0};
int port;

static void usage(char *error) {
	struct _IO_FILE *file = stdout;

	if(strcmp(error, " ") != 0)
		file = stderr;
	fprintf(file, "%s\n"
			"tempsense - Senses available temperature and transmits via network\n"
			"tempsense [OPTION]\n"
			"    -h        : Print this help message\n"
			"    -d <n>    : Specifies delay (in seconds). Accepts float\n"
			"    -p <n>    : Specifies a port # [1024 - 65535]\n"
			, error);

	if(strcmp(error, " ") != 0)
		exit(-1);
}

static int parse_opts(int argc, char **argv) {
	int opt;

	while( (opt = getopt(argc, argv, "d:p:hv")) != -1) {
		switch(opt) {
		case ':' :
			usage("missing parameter value");
			break;
		case 'd' : {
			i64 time = (i64) (atof(optarg) * 1e9);
			if(time < 0)
				usage("Delay must be positive\n");
			time_t sec 	= time / 1e9;
			time_t nsec = time - (sec * 1e9);
			delay.tv_nsec = nsec;
			delay.tv_sec  = sec;
			break;
		}
		case 'h' :
			usage(" ");
			break;
		case 'p' :
			port = atoi(optarg);
			if(port < 1024 || port > 65535)
				usage("Invalid port #\n");
			break;
		case 'v' :
			verbose = 1;
			break;
		default :
		case '?' :
			usage("invalid command line argument");
			break;
		}
	}

	if(!port)
		usage("Must specify port number\n");

	return 0;
}

int main(int argc, char **argv) {
	parse_opts(argc, argv);

	int sock_fd = start_server(port);
	if(sock_fd < 0)
		panic("Could not open socket\n");

	char *exec_arg[] = {"", NULL};
	struct sockaddr_storage client_addr;
	unsigned int address_size = sizeof(client_addr);
	while(1) {
		VERBOSE("Listening for incoming connections\n");
		int new_sock_fd = accept(sock_fd, (struct sockaddr *) &client_addr, &address_size);
		if(new_sock_fd == -1)
			panic("Unable to accept!\n");
		VERBOSE("Accepted incoming connection\n");

//		Duplicate stderr
		dup2(1, 10);
		dup2(new_sock_fd, 1);
		int pid = fork();
		if(pid == 0) {
//			Child
			execv("/usr/bin/sensors", exec_arg);
		}
		else {
//			Parent
			int status;
			waitpid(pid, &status, 0);
			dup2(10, 1);
			nanosleep(&delay, NULL);
			close(new_sock_fd);
		}
	}
}
