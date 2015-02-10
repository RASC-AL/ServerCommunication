/* udpClient.c DUMMY FILE*/
#include "ros/ros.h"
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <netdb.h>
#include <stdio.h>
#include <unistd.h> /* close */
#define SERVER_PORT 6000

int main (int argc, char *argv[]) {
	ros::init(argc,argv,"UDPClient");
	ros::NodeHandle n;
  int sd, rc, i;
  struct sockaddr_in localAddr, servAddr;
  struct hostent *h;
  
  if(argc < 3) {
ROS_INFO("error argc");
    exit(1);
  }

  h = gethostbyname(argv[1]);
  if(h==NULL) {
ROS_INFO("ip addr problem");
    exit(1);
  }
  servAddr.sin_family = h->h_addrtype;
  memcpy((char *) &servAddr.sin_addr.s_addr, h->h_addr_list[0], h->h_length);
  servAddr.sin_port = htons(SERVER_PORT);
  /* create socket */
  sd = socket(AF_INET, SOCK_DGRAM, 0);
  if(sd<0) {
   ROS_INFO("can't open");
    exit(1);
  }
  /* bind any port number */
  localAddr.sin_family = AF_INET;
  localAddr.sin_addr.s_addr = htonl(INADDR_ANY);
  localAddr.sin_port = htons(0);
  if(bind(sd,(struct sockaddr *)&localAddr,sizeof(localAddr)) < 0)
   {
        ROS_INFO("bind problem");
	exit(1);
  }
  ROS_INFO("Enter data to send to client : \n");
  while(ros::ok())
  {
    char *buffer = (char *)malloc(1000); //
    scanf("%s",buffer);
    rc = sendto(sd,buffer,strlen(buffer) + 1, 0,
		(struct sockaddr *)&servAddr , 
		sizeof(servAddr));
    if(rc<0) 
    {
      ROS_INFO("cannot send data ");
      close(sd);
      exit(1);
    }
    ROS_INFO("data send to client :%s",buffer);
    free(buffer);
  }
  return 0;  
}

