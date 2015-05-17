#!/usr/bin/env python
import socket
import rospy
import traceback
from std_msgs.msg import String

def callback(dataS):
	try:
		data = dataS.data + "\n"
		#data.replace("data: ", "")
		print "sending data" + data
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect(("128.205.55.128", 9999))
		totalsent = 0
		while totalsent < len(data):
			sent = sock.send(data[totalsent:])
			if sent == 0:
				print "connection closed"
				break
			totalsent = totalsent + sent
	except Exception, e:
		rospy.logerr(e)

def returnData():
	rospy.init_node("rover_data")
	rospy.Subscriber('ReturnData', String, callback)
	rospy.spin()

if __name__ == "__main__":
	try:
		returnData()
	except Exception, e:
		pass
