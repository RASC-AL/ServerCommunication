#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import serial

com = serial.Serial('/dev/ttyACM0',baudrate=115200)

def callback(data):
        data = 'r,'+str(data) + '\n'
        com.write(data)
        com.flush()

def controller():
        rospy.init_node('relay')
        rospy.Subscriber('/RLY', String, callback)
        rospy.spin()

if __name__ == '__main__':
        controller()

