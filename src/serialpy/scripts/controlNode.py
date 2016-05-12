#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import subprocess
import os

control_pub = rospy.Publisher('HomeControl', String, queue_size = 1)
cam_pub = rospy.Publisher('config', String, queue_size = 1)
ptz_pub = rospy.Publisher('PTZ', String, queue_size = 1)

def callback(data):
        command = str(data.data).rstrip()
        if(command[0] == 'l' or command[0] == 's' or command[0] == 'P'):
        	control_pub.publish(command)
        	if(command[0] == 'P'):
        	    ptz_pub.publish(command[-1])
        elif(command[0] == 'C'):
                command = command.replace('C', '')
                cam_pub.publish(command)
        elif(command[0] == 'R'):
		os.spawnl(os.P_NOWAIT, 'bash /home/sbrover/start_rover.sh')
		# subprocess.Popen('/home/sbrover/start_rover.sh') 
def controlNode():
        rospy.init_node('ControlNode')
        rospy.Subscriber('HomeCommand', String, callback)
        rospy.spin()

if __name__ == '__main__':
        controlNode()


