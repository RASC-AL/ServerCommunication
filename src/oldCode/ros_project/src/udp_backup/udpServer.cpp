#include "gprot.h"
int main (int argc, char *argv[]) 
{
	ros::init(argc,argv,"UDPServer");
	ros::NodeHandle n;
	ros::Rate loop_rate(10);
	std_msgs::String msg;
	ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter",1000);
	server_sock_id = socket(SOCK_FAMILY,SOCK_TYPE,SOCK_FLAG);
	if(server_sock_id < 0)
	{
		ROS_INFO("Error! - Socket Creation Error\n");
		exit(0);
	}
	server_setup();
	ROS_INFO("Waiting for data to come \n");
	while (ros::ok())
	{
		int status = -1;
		socklen_t cli_len = sizeof(client_addr);
		memset(recv_buf,0x0,MAX_BUF_SIZE);
		status = recvfrom(server_sock_id,recv_buf,MAX_BUF_SIZE,0,
				(struct sockaddr *)&client_addr,&cli_len);
		if(status < 0)
		{
			ROS_INFO("Error! - Read Error");
		}
		ROS_INFO("Received Data : %s",recv_buf);
		//msg.data = recv_buf;
		//chatter_pub.publish(msg);
		ros::spinOnce();
		loop_rate.sleep();
	}
	close(server_sock_id);
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
}
