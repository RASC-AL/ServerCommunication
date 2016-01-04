#include "gprot.h"
#include <stdlib.h>
#include <string.h>     // string function definitions
#include <unistd.h>     // UNIX standard function definitions
#include <fcntl.h>      // File control definitions
#include <errno.h>      // Error number definitions
#include <termios.h>    // POSIX terminal control definitions
#include <string>
using namespace std;
using namespace ros;
ros::Publisher ptz_pub;
int startSerial();
void setParameters(struct termios tty,int fd);
void setParameters(struct termios tty);
void handleRecievedData(char recv_buf[],Publisher config_pub,Publisher arm_pub);
int main (int argc, char *argv[]) 
{
	int fd_max;
	struct timeval tv;
	tv.tv_sec = 2;
	tv.tv_usec = 0;
	fd_set read_fds;
	FD_ZERO(&read_fds);
	ros::init(argc,argv,"Server");
	ros::NodeHandle n;
	ros::Rate loop_rate(10);
	ros::Publisher config_pub = n.advertise<std_msgs::String>("config",1000);
	ros::Publisher arm_pub = n.advertise<std_msgs::String>("ARM",1000);
	ptz_pub = n.advertise<std_msgs::String>("chatter",1000);
	server_sock_id = socket(SOCK_FAMILY,SOCK_TYPE,SOCK_FLAG);
	if(server_sock_id < 0)
	{
		ROS_INFO("Error! - Socket Creation Error\n");
		exit(0);
	}
	FD_SET(server_sock_id,&read_fds);
	while (ros::ok())
	{
		select(server_sock_id+1,&read_fds,NULL,NULL,&tv);
		if(FD_ISSET(server_sock_id,&read_fds))
		{
			int conn_id = accept(server_sock_id,(struct sockaddr *)NULL,NULL);
			if(conn_id == -1) // WOULDBLOCK
			{
				continue;
			}
			ROS_INFO("Connection accepted\n");
			int status;
			memset(recv_buf,0x0,MAX_BUF_SIZE);
			status = recv(conn_id,recv_buf,MAX_BUF_SIZE,0);
			if(status <= 0)
			{
				ROS_INFO("Error! - Read Error");
			}
			ROS_INFO("Received Data : %s",recv_buf);
			handleRecievedData(recv_buf,config_pub,arm_pub);
		}
		ros::spinOnce();
		loop_rate.sleep();
		close(server_sock_id);
	}
	return 0;
}
void server_setup()
{
	memset(&server_addr,0,sizeof(server_addr));
	server_addr.sin_family = SOCK_FAMILY;
	server_addr.sin_addr.s_addr = htonl(INADDR_ANY);
	server_addr.sin_port = htons(SERVER_PORT);
	if(bind(server_sock_id,(struct sockaddr *)&server_addr,sizeof(server_addr)))
	{
		ROS_INFO("Error! - Bind failed\n");
		close(server_sock_id);
		exit(1);
	}
	listen(server_sock_id,MAX_CONN);
}
int startSerial()
{
	unsigned char cmd[] = "Hello World\r";
	int n_written = 0;
	struct termios tty;
	/* Open File Descriptor */
	int USB = open( "/dev/ttyACM0", O_RDWR| O_NOCTTY|O_NONBLOCK );
	/* *** Configure Port *** */
	memset (&tty, 0, sizeof tty);
	/* Error Handling */
	if ( tcgetattr ( USB, &tty ) != 0 )
	{
		ROS_INFO("Error :%d , from tcgetattr:%s \n",errno,strerror(errno));
	}
	setParameters(tty,USB);
	return USB;
}
void handleRecievedData(char recv_buf[],Publisher config_pub,Publisher arm_pub)
{
	std_msgs::String msg;
	char type[4]={'\0'};
	strncpy(type,recv_buf,3);
	if(!strcmp(type,"CAM"))
	{
		int written;
		char temp[20]={'\0'};
		strncpy(temp,recv_buf+4,strlen(recv_buf));
		ROS_INFO("sent data : %s",temp);
		msg.data = temp;
		config_pub.publish(msg);
	}
	else if(!strcmp(type,"ARM"))
	{
		int written = strlen(recv_buf);
		char temp[20]={'\0'};
		strncpy(temp,recv_buf+4,written);
		ROS_INFO("sent data : %s",temp);
		msg.data = temp;
		arm_pub.publish(msg);
	}
	else if(!strcmp(type,"PTZ"))
	{
		int written = strlen(recv_buf);
		char temp[20]={'\0'};
		strncpy(temp,recv_buf+4,written);
		ROS_INFO("sent data : %s",temp);
		msg.data = temp;
		ptz_pub.publish(msg);
	}
}

void setParameters(struct termios tty,int fd)
{
	/* Set Baud Rate */
	cfsetospeed (&tty, (speed_t)B9600);
	cfsetispeed (&tty, (speed_t)B9600);
	/* Setting other Port Stuff */
	tty.c_cflag     &=  ~PARENB;        // Make 8n1
	tty.c_cflag     &=  ~CSTOPB;
	tty.c_cflag     &=  ~CSIZE;
	tty.c_iflag=0;
        tty.c_oflag=0;
	tty.c_lflag=0;
	tty.c_cflag     |=  CS8;

	tty.c_cflag     &=  ~CRTSCTS;       // no flow control
	tty.c_cc[VMIN]      =   1;                  // read doesn't block
	tty.c_cc[VTIME]     =   20;                  // 0.5 seconds read timeout
	tty.c_cflag     |=  CREAD | CLOCAL;     // turn on READ & ignore ctrl lines
	tty.c_iflag &= ~(IXON | IXOFF | IXANY);
        tty.c_lflag &= ~(ICANON | ECHO | ECHOE | ISIG); // make raw
        tty.c_oflag &= ~OPOST; // make raw	
	if( tcsetattr(fd, TCSANOW, &tty) < 0) {
        	ROS_INFO("init_serialport: Couldn't set term attributes");
        return;
    	}
}

/*********************Test Code******************************/
/*
void testWrite(int USB)
{
	unsigned char test[10] = "hello\r";
	int n_written = 0;
	do 
	{
		n_written += write( USB, &test[n_written], 1 );
		//ROS_INFO("Written data : %c",test[n_written]);
	}while (test[n_written-1] != '\r' && n_written > 0);
}
void test(int USB)
{
	char buf[256];
	memset (buf, '\0', sizeof(buf));
	int n = 0;
	do
	{
		n = read( USB, buf, 1 );
	}while( *buf != '\n' && n > 0);
	if (n < 0)
	ROS_INFO("Error Reding : %d\n",strerror(errno));
	else if (n == 0)
		ROS_INFO("Read Nothing !!\n");
	else
		ROS_INFO("Response : %s",buf);
}
void senddataOverSerial(int USB,char cmd[],int n_written)
{
	do 
	{
		n_written += write( USB, &cmd[n_written], 1 );
		//ROS_INFO("Written data : %s",cmd[n_written]);
	}while (cmd[n_written-1] != '\r' && n_written > 0);
}
void startArdeno(int USB)
{
	unsigned char start = 0x01;
	write( USB,&start, 1 );
	ROS_INFO("startArdeno : %c",start);
}
void moveArm(int USB)
{
	unsigned char start = 0x01;
	int n_written = 0;
	int len = strlen(cmd);
	do 
	{
		n_written += write( USB, &cmd[n_written],1);
	}while (cmd[n_written-1] != '\r' && n_written > 0);
	write(USB,"90,-20,10,10,10",15);
}
void sigHandler(int sig)
{
	g_shutdown = 0;
}
dataSet sendMotionData(char recv_buf[],dataSet prevObj,int USB,int written)
{
	dataSet obj;
	memset(&obj,0,sizeof(obj));
	memcpy(&obj,recv_buf,sizeof(recv_buf));
	if(prevObj.r != obj.r)
	{
		sprintf(recv_buf,"%f",obj.r);
		senddataOverSerial(USB,recv_buf,written);
		prevObj.r = obj.r;
	}
	if(prevObj.theta != obj.theta)
	{
		sprintf(recv_buf,"%f",obj.theta);
		senddataOverSerial(USB,recv_buf,written);
		prevObj.theta = obj.r;
	}
	if(prevObj.DIR != obj.DIR)
	{
		sprintf(recv_buf,"%c",obj.DIR);
		senddataOverSerial(USB,recv_buf,written);
		prevObj.theta = obj.r;
	}
	
}
*/
/*********************Test Code******************************/

