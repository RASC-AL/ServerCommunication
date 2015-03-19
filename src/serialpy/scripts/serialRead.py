#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import serial

#Setup
ser = serial.Serial('/dev/ttyACM0', baudrate = 115200, timeout = .5)
roverData_pub = rospy.Publisher('RoverData', String, queue_size = 1)
rospy.init_node("SerialRead")
data = ""
rospy.sleep(5)
r = rospy.Rate(16)

#Loop
while not rospy.is_shutdown():
        data = ser.readline()
      	roverData_pub.publish(data)
        r.sleep()
