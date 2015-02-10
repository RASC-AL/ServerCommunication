#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import Joy
from std_msgs.msg import String

drvPub = rospy.Publisher('DRV',String, queue_size=10)

left_speed = 0
right_speed = 0

speed_mod = 1.0

def callback(data):
	global move, left_speed, right_speed, speed_mod
        now = rospy.get_time()
	ind = -1
	try:
		ind = data.buttons.index(1)
	except ValueError: pass
	#Drive control
	if data.axes[5] < -.5:
		speed_mod = 1.5
	else:
		speed_mod = 1.0
	if math.fabs(data.axes[4]) > .1:
		right_speed = speed_mod*data.axes[4]
	else:
		right_speed = 0.0
	if math.fabs(data.axes[1]) > .1:
		left_speed = speed_mod*data.axes[1]
	else:
		left_speed = 0.0
	rospy.sleep(.125-(rospy.get_time()-now))
	drvPub.publish(str(left_speed)+','+str(right_speed))

def controller():
	rospy.init_node('xbox', anonymous = True)
	rospy.Subscriber('joy', Joy, callback, queue_size=1)
        rospy.spin()

if __name__ == '__main__':
	controller()
