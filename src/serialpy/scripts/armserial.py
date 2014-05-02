#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import serial

com = serial.Serial('/dev/ttyACM1',baudrate=115200)
com.write('a,40,90,70,105,40')
def callback(data):
	
	rospy.loginfo(data)
	data = 'a,'+str(data) + '\n'
	rospy.loginfo(data)
	print data
	com.write(data)
	com.flush()

def controller():
	rospy.init_node('arm')
	rospy.Subscriber('/ARM', String, callback)
	rospy.spin()

if __name__ == '__main__':
	controller()
