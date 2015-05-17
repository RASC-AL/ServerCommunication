#!/usr/bin/env python
import socket
import rospy
import traceback
from std_msgs.msg import String

baseSocket = None

def callback(dataS):
	try:
		global baseSocket
		if baseSocket is None:
			print "creating new socket"
			baseSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			baseSocket.connect(("128.205.55.128", 9999))
		data = dataS.data + "\n"
		totalsent = 0
		while totalsent < len(data):
			sent = sock.send(data[totalsent:])
			if sent == 0:
				break
			totalsent = totalsent + sent
	except Exception, e:
		rospy.logerr(e)
		if baseSocket is None:
			return
		baseSocket.close()
		baseSocket = None

def returnData():
	rospy.init_node("rover_data")
	rospy.Subscriber('ReturnData', String, callback)
	rospy.spin()

if __name__ == "__main__":
	try:
		returnData()
	except Exception, e:
		pass
