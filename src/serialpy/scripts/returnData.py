#!/usr/bin/env python
import socket
import rospy
import traceback
from std_msgs.msg import String

baseSocket = None

#communication: mothod for sending data across to base. This socket is only meant for sending data to the base. 
#baseSocket is None when connections isn't present and it is set to the socket when connection is established
#The socket used for receiving data is in server.py. The sockets are kept separate because this node cannot access 
#the socket in the server.
def callback(dataS):
	try:
		global baseSocket
		
		if baseSocket is None:
			rospy.loginfo("creating new socket")
			baseSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			#baseSocket.settimeout(1)
			#baseSocket.connect(("128.205.55.128", 9999))
		rospy.loginfo("socket initialized")
		data = dataS.data
		if len(data) == 0:
			return
		#totalsent = 0
		#while totalsent < len(data):
		sent = baseSocket.sendto(data, ('128.205.55.128', 9999))
		#rospy.logerr('sent data : size => ' + str(sent) + " " + data)
			#if sent == 0:
				#break
			#totalsent = totalsent + sent
		rospy.loginfo("sent data: " + data)
	except Exception, e:
		rospy.logerr(e)
		if baseSocket is None:
			return
		#baseSocket.close()
		baseSocket = None

#communication: this node subscribes to a topic and sends across whatever data it receives
def returnData():
	rospy.init_node("rover_data")
	rospy.Subscriber('ReturnData', String, callback)
	rospy.spin()

if __name__ == "__main__":
	try:
		returnData()
	except Exception, e:
		pass
