#ifndef GPROT_H
#define GPROT_H

#include "ros/ros.h"
#include "std_msgs/String.h"
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h> /* close */

#define SUCCESS 0
#define ERROR   1
#define TRUE 1
#define FALSE  0

#define END_LINE 0x0
#define SERVER_PORT 6000
#define MAX_MSG 100
#define HOST_SIZE 128
#define SOCK_FAMILY AF_INET
#define SOCK_TYPE SOCK_DGRAM
#define SOCK_FLAG  0
#define MAX_BUF_SIZE 1024


struct sockaddr_in server_addr;
struct sockaddr_in client_addr;
int server_sock_id; 
char recv_buf[MAX_BUF_SIZE];
void server_setup();
#endif
