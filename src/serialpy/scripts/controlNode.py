#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import serial

control_pub = rospy.Publisher('HomeControl', String, queue_size=1)
command = ""

def callback(data):
        command = str(data.data)
	if(command[0] == 'l'):
        	control_pub.publish(command)

def controlNode():
        rospy.init_node('ControlNode')
        rospy.Subscriber('HomeCommand', String, callback)
        rospy.spin()

if __name__ == '__main__':
        controlNode()


