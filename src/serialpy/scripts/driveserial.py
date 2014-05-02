#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import serial


com = serial.Serial('/dev/ttyACM1',baudrate=115200)
def callback(data):
        data = str(data)
        com.write('d,'+data)
        com.flush()

def controller():
        rospy.init_node('drv')
        rospy.Subscriber('/DRV', String, callback)
        rospy.spin()

if __name__ == '__main__':
        controller()

