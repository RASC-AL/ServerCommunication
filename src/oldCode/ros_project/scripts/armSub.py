#!/usr/bin/env python
import roslib
roslib.load_manifest('ros_project')
import sys
import rospy
import serial
def callback(data):
    rospy.loginfo(rospy.get_caller_id()+"I heard %s",data.data)
    arduino.write(data.data)
    
def listener():

    # in ROS, nodes are unique named. If two nodes with the same
    # node are launched, the previous one is kicked off. The 
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaenously.
    rospy.init_node('armSub', anonymous=True)
    arduino=serial.Serial('/dev/ttyACM0', 9600)
    rospy.Subscriber("ARM", String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
        
if __name__ == '__main__':
    listener()
