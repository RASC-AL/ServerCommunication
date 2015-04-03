#!/usr/bin/env python
# Software License Agreement (BSD License)

import roslib
roslib.load_manifest('rover2015')
import sys
import rospy
import numpy as np
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

def talker():
    pub = rospy.Publisher('chatter', Image, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    r = rospy.Rate(10) # 10hz
    bridge = CvBridge()
    cap = cv2.VideoCapture(0)
    while not rospy.is_shutdown():
        # str = "hello world %s"%rospy.get_time()
        # rospy.loginfo(str)
        ret, frame = cap.read()
        frame = np.hstack((frame,frame))
        try:
          pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
        except CvBridgeError, e:
          print e
        r.sleep()
        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
