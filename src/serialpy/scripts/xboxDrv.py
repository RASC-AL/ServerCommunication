#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import Joy
from std_msgs.msg import String

drvPub = rospy.Publisher('DRV',String, queue_size=10)

left_speed = 0
right_speed = 0

speed_mod = 2.0

def callback(data):
	global move, left_speed, right_speed, speed_mod
        now = rospy.get_time()
	ind = -1
	try:
		ind = data.buttons.index(1)
	except ValueError: pass
	#Drive control
	#Set speed modification
	if data.axes[5] < -.5:
		speed_mod = 1.0
	else:
		speed_mod = 2.0
	#Right wheel speed
	if math.fabs(data.axes[4]) > .1:
		right_speed = -data.axes[4]/speed_mod*500+1500
	else:
		right_speed = 1500
	#Left wheel speed
	if math.fabs(data.axes[1]) > .1:
		left_speed = data.axes[1]/speed_mod*500+1500
	else:
		left_speed = 1500
	rospy.sleep(.0625-(rospy.get_time()-now))
	drvPub.publish(str(int(right_speed))+','+str(int(left_speed))+',')

def controller():
	rospy.init_node('xboxDrv', anonymous = True)
	rospy.Subscriber('joy2', Joy, callback, queue_size=1)
        rospy.spin()

if __name__ == '__main__':
	controller()
