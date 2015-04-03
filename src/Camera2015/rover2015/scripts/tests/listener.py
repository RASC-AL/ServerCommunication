#!/usr/bin/env python
# Software License Agreement (BSD License)

import rospy
import numpy as np
import sys
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()

def callback(data):
    try:
      cv_image = bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError, e:
      print e
    cv2.imshow('frame',cv_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        sys.exit()
    # rospy.loginfo(rospy.get_caller_id()+"I heard %s",data.data)
    
def listener():

    # in ROS, nodes are unique named. If two nodes with the same
    # node are launched, the previous one is kicked off. The 
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'talker' node so that multiple talkers can
    # run simultaenously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", Image, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
        
if __name__ == '__main__':
    listener()
