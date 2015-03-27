#!/usr/bin/env python
import rospy
import os
import subprocess
import signal
from std_msgs.msg import String

def gettemp():
	tempproc = subprocess.Popen(["sensors"], stdout=subprocess.PIPE, shell=True)
	(out, err) = tempproc.communicate()
	return out

def extracttemp():
	temp = gettemp()
	i = temp.index('+') - 1
	j = temp.index('C') - 2
	return temp[i:j]

def talker():
	pub = rospy.Publisher('rovertemp', String, queue_size=10)
    	rospy.init_node('tempnode', anonymous=True)
    	rate = rospy.Rate(10)
    	while not rospy.is_shutdown():
        	temp_str = extracttemp() + rospy.get_time()
        	pub.publish(temp_str)
        	rate.sleep()

if __name__ == '__main__':
    	try:
        	talker()
    	except rospy.ROSInterruptException:
        	pass	
