#include "gprot.h"
int main (int argc, char *argv[]) 
{
	ros::init(argc,argv,"UDPServer");
	ros::NodeHandle n;
	int sid;
	int status;
	struct sockaddr_in addr;
	struct sockaddr_in host_addr;
	memset(&addr,0,sizeof(addr));
	memset(&host_addr,0,sizeof(host_addr));
	socklen_t len = sizeof(host_addr);
	sid = socket(AF_INET,SOCK_STREAM,0);	
	if(sid < 0)
	{
		ROS_INFO("My IP Command Fail\n");
		exit(1);
	}
	addr.sin_family = AF_INET;
	addr.sin_port = htons(53);
	addr.sin_addr.s_addr =inet_addr("8.8.8.8");

	status = connect(sid,(struct sockaddr *)&addr,sizeof(addr));
	if(status < 0)
	{
		ROS_INFO("My IP Command Fail:Connect\n");
		exit(1);
	}
	getsockname(sid,(struct sockaddr *)&host_addr,&len);
	strcpy(myip,inet_ntoa(host_addr.sin_addr));
	ROS_INFO("Address:%s\n",inet_ntoa(host_addr.sin_addr));
	ROS_INFO("Port:%d\n",port);
	close(sid);
}