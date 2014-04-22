/*
 * server.c
 *
 *  Created on: Jan 13, 2014
 *      Author: namita
 */

#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <fcntl.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>

#include "include/common.h"

static int open_socket() {
	int sock_fd = socket(PF_INET, SOCK_STREAM, 0);
	if(sock_fd == -1) {
		panic("Can't open socket!");
	}
	return sock_fd;
}

static void bind_to_port(int socket, int port) {
	struct sockaddr_in name;
	name.sin_family = PF_INET;
	name.sin_port = (in_port_t)htons(port);
	name.sin_addr.s_addr = htonl(INADDR_ANY);
	int reuse = 1;
	if(setsockopt(socket, SOL_SOCKET, SO_REUSEADDR, (char*)&reuse, sizeof(int)) == -1) {
		panic("Can't set reuse option on socket!");
	}
	int c = bind(socket, (struct sockaddr *) &name, sizeof(name));
	if(c == -1) {
		panic("Can't bind to port!");
	}
}

static void listen_for_connections(int socket, int qLenght) {
	int l = listen(socket, qLenght);
	if (l == -1) {
		panic("Can't listen!");
	}
}

int send_message(int socket, char *s, off_t len) {
	char *ptr = s;
	while(len > 0) {
		off_t ret = write(socket, ptr, len);
		ptr += ret;
		len -= ret;
	}
	return 0;
}

int read_message(int socket, char *buf, int len) {
	int bytes = read(socket, buf, len);
	return bytes;
}

int start_server(int port) {
	int sock_fd = open_socket();

	bind_to_port(sock_fd, port);
	listen_for_connections(sock_fd, 10);
	return sock_fd;
}


