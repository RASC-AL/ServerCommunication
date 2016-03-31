#!/usr/bin/env python
import roslib
import sys
import rospy
import cv
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
import time
import os
from subprocess import call
import re

def talker():
    global cap1
    global cap2
    bridge=CvBridge()

    pub = rospy.Publisher('blob', Image)
    rospy.init_node('blob', anonymous=True)

    #rospy.Subscriber("configCam", String, cam_setup)

    i = 0

    while i<2:
        try:
            cap1=cv2.VideoCapture(i)
            print i
        except e: pass
        i=i+1



if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
