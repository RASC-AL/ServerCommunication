/*
 * server.h
 *
 *  Created on: Apr 22, 2014
 *      Author: guru
 */

#ifndef SERVER_H_
#define SERVER_H_

int send_message(int socket, char *s, off_t len);
int read_message(int socket, char *buf, int len);
int start_server(int port);

#endif /* SERVER_H_ */
