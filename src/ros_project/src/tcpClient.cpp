/* fpont 12/99 */
/* pont.net    */
/* tcpClient.c */
#include "ros/ros.h"
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h> /* close */
#define SERVER_PORT 5000
#define MAX_MSG 100
typedef struct
{
	//motion control
	double r;
	double theta;
	char DIR;
	//camera control
	int cameraSelection;
	char pan;
	char tilt;
	char zoom;
}dataSet;
int main (int argc, char *argv[]) 
{
	ros::init(argc,argv,"Client");
	ros::NodeHandle n;
	int sd, rc, i;
	struct sockaddr_in localAddr, servAddr;
	struct hostent *h;
	char buffer[1024];
	if(argc < 3) {
		exit(1);
	}
	h = gethostbyname(argv[1]);
	if(h==NULL) {
		exit(1);
	}
  servAddr.sin_family = h->h_addrtype;
  memcpy((char *) &servAddr.sin_addr.s_addr, h->h_addr_list[0], h->h_length);
  servAddr.sin_port = htons(SERVER_PORT);
  /* create socket */
  sd = socket(AF_INET, SOCK_STREAM, 0);
  if(sd<0) {
    exit(1);
  }
  /* bind any port number */
  localAddr.sin_family = AF_INET;
  localAddr.sin_addr.s_addr = htonl(INADDR_ANY);
  localAddr.sin_port = htons(0);
  rc = bind(sd, (struct sockaddr *) &localAddr, sizeof(localAddr));
  if(rc<0) {
    exit(1);
  }			
  rc = connect(sd, (struct sockaddr *) &servAddr, sizeof(servAddr));
  if(rc<0) {
    exit(1);
  }
  dataSet obj;
  obj.r = 2.13;
  obj.theta = 30;
  obj.DIR = 'F';
  memset(buffer,0,sizeof(buffer));
  memcpy(&obj,buffer,sizeof(obj));
  send(sd,buffer,sizeof(obj),0);
  return 0; 
}
