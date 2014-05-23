#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import String


drvPub = rospy.Publisher('DRV',String, queue_size=10)
armPub = rospy.Publisher('ARM',String, queue_size=10)
speed = 50

def callback(data):
	global speed
	ind = -1
	try:
		ind = data.buttons.index(1)
	except ValueError: pass
	if ind == 14:
		drvPub.publish(str(-speed)+','+str(-speed))
	elif ind == 13:
		drvPub.publish(str(speed)+','+str(speed))
	elif ind == 12:
		drvPub.publish(str(speed)+','+str(-speed))
	elif ind == 11:
		drvPub.publish(str(-speed)+','+str(speed))
	else:
		drvPub.publish('0,0')


def controller():
	rospy.init_node('xbox', anonymous=True)
	rospy.Subscriber('joy', Joy, callback)
	rospy.spin()

if __name__ == '__main__':
	controller()
