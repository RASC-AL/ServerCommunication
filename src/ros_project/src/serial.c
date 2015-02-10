#include <stdio.h>      // standard input / output functions
#include <stdlib.h>
#include <string.h>     // string function definitions
#include <unistd.h>     // UNIX standard function definitions
#include <fcntl.h>      // File control definitions
#include <errno.h>      // Error number definitions
#include <termios.h>    // POSIX terminal control definitions
void setParameters(struct termios tty);
void test(int USB);
int startSerial()
{
	unsigned char cmd[] = "Hello World\r";
	int n_written = 0;
	struct termios tty;
	/* Open File Descriptor */
	int USB = open( "/dev/ttyUSB0", O_RDWR| O_NOCTTY|O_NONBLOCK );
	/* *** Configure Port *** */
	memset (&tty, 0, sizeof tty);
	/* Error Handling */
	if ( tcgetattr ( USB, &tty ) != 0 )
	{
		ROS_INFO("Error : %d from tcgetattr: %d\n",errno,strerror(errno));
	}
	/* Error Handling */
	if ( tcgetattr ( USB, &tty ) != 0 )
	{
		ROS_INFO("Error :%d , from tcgetattr:%d \n",errno,strerror(errno);
	}
	setParamters(tty);

	/* Flush Port, then applies attributes */
	tcflush( USB, TCIFLUSH );
	if ( tcsetattr ( USB, TCSANOW, &tty ) != 0)
	{
		ROS_INFO("Error :%d from ctsetattr\n",errno);
	}
	startArdeno(int USB,int n_written);
	//test(USB);
}
void startArdeno(int USB)
{
	write( USB,0x01, 1 );
}
void senddataOverSerial(int USB,char cmd[],int n_written)
{
	do 
	{
		n_written += write( USB, &cmd[n_written], 1 );
		ROS_INFO("Written data : %s",cmd[n_written]);
	}while (cmd[n_written-1] != '\r' && n_written > 0);
}
void test(int USB)
{
	/* Allocate memory for read buffer */
	char buf[256];
	memset (buf, '\0', sizeof(buf));
	int n = 0;
	do
	{
		n = read( USB, buf, 1 );
	}while( *buf != '\r' && n > 0);
	if (n < 0)
		ROS_INFO("Error Reding : %d\n",strerror(errno));
	else if (n == 0)
		ROS_INFO("Read Nothing !!\n");
	else
		ROS_INFO("Response : %s",buf);
}
void setParameters(struct termios tty)
{
	/* Set Baud Rate */
	cfsetospeed (&tty, (speed_t)B9600);
	cfsetispeed (&tty, (speed_t)B9600);

	/* Setting other Port Stuff */
	tty.c_cflag     &=  ~PARENB;        // Make 8n1
	tty.c_cflag     &=  ~CSTOPB;
	tty.c_cflag     &=  ~CSIZE;
	tty.c_cflag     |=  CS8;

	tty.c_cflag     &=  ~CRTSCTS;       // no flow control
	tty.c_cc[VMIN]      =   1;                  // read doesn't block
	tty.c_cc[VTIME]     =   5;                  // 0.5 seconds read timeout
	tty.c_cflag     |=  CREAD | CLOCAL;     // turn on READ & ignore ctrl lines

	/* Make raw */
	cfmakeraw(&tty);
}
