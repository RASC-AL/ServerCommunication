#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import serial

#ser = serial.Serial('/dev/ttyACM0', baudrate = 115200)
homeCom_pub = rospy.Publisher('homeTest', String, queue_size=1)
command = ""
now = 0

def callback(data):
        global now
	command = str(data.data)        
        homeCom_pub.publish(command)
#        ser.write(command)
#       ser.flush()
        command = ""

def serialWrite():
	rospy.init_node('SerialWrite')
        rospy.Subscriber('HomeControl', String, callback)
        rospy.spin()

if __name__ == '__main__':
	rospy.sleep(5)
        serialWrite()        


