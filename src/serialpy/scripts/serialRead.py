#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import serial

#Setup
def talker():
	ser = serial.Serial('/dev/ttyACM0', baudrate = 115200, timeout = .5)
	roverData_pub = rospy.Publisher('ReturnData', String, queue_size = 1)
	rospy.init_node("SerialRead")
	r = rospy.Rate(16)
 	rospy.sleep(5)
	#Loop
	while not rospy.is_shutdown():
        	data = ser.readline()
      		roverData_pub.publish('d' + data)
        	r.sleep()

if __name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass

