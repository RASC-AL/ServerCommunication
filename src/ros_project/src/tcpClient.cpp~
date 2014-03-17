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

int main (int argc, char *argv[]) {
	ros::init(argc,argv,"Client");
	ros::NodeHandle n;
  int sd, rc, i;
  struct sockaddr_in localAddr, servAddr;
  struct hostent *h;
  
  if(argc < 3) {
    //cout<<"usage:"<< argv[0] << "<server> <data1> <data2> ... <dataN>\n";
    exit(1);
  }

  h = gethostbyname(argv[1]);
  if(h==NULL) {
    //cout<<argv[0]<< "unknown host" << argv[1] <<endl;
    exit(1);
  }

  servAddr.sin_family = h->h_addrtype;
  memcpy((char *) &servAddr.sin_addr.s_addr, h->h_addr_list[0], h->h_length);
  servAddr.sin_port = htons(SERVER_PORT);

  /* create socket */
  sd = socket(AF_INET, SOCK_STREAM, 0);
  if(sd<0) {
   //cout<<"can't open";
    exit(1);
  }

  /* bind any port number */
  localAddr.sin_family = AF_INET;
  localAddr.sin_addr.s_addr = htonl(INADDR_ANY);
  localAddr.sin_port = htons(0);
  
  rc = bind(sd, (struct sockaddr *) &localAddr, sizeof(localAddr));
  if(rc<0) {
    //printf("%s: cannot bind port TCP %u\n",argv[0],SERVER_PORT);
    //perror("error ");
    exit(1);
  }
				
  /* connect to server */
  rc = connect(sd, (struct sockaddr *) &servAddr, sizeof(servAddr));
  if(rc<0) {
    //perror("cannot connect ");

    exit(1);
  }

  for(i=2;i<argc;i++) {
    
    rc = send(sd, argv[i], strlen(argv[i]) + 1, 0);
    
    if(rc<0) {
      //perror("cannot send data ");
      close(sd);
      exit(1);
    
    }
ROS_INFO("%s : data %u sent : %s\n",argv[0],i-1,argv[i]);
    //printf("%s: data%u sent (%s)\n",argv[0],i-1,argv[i]);

   
  }

return 0;
  
}

