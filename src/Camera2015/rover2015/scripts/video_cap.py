#!/usr/bin/env python
import roslib
roslib.load_manifest('rover2015')
import os
import rospy
import numpy as np
import cv2
from cv2 import cv
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import warnings

def checkcamList(camList):
    stream=os.popen("ls /dev/video*")
    devices = stream.read().split()
    for i in camList:
        if '/dev/video' + str(i) not in devices:
            warnings.warn('/dev/video' + str(i) + ' does not exits!')
            
# see my-webcam.rules for cameras mapping
# 0->video7, 1->video6, ...
# camList = [7,6,5,4]
from conf import camList

checkcamList(camList)

prev_cam = 0
cam = 0
fps = 30
cap = cv.CaptureFromCAM(camList[cam])
r = None

def callback_config(msg):
    global prev_cam
    global cam
    global cap, cap1
    global fps
    global r
    s = str(msg.data).split(',')
    cam = int(s[0])
    fps = int(s[1])
    if cam != prev_cam and cam in range(len(camList)):
        cap = cv.CaptureFromCAM(camList[cam])
        prev_cam = cam
    r = rospy.Rate(fps)
 
def talker():
    global r

    bridge=CvBridge()
    pub = rospy.Publisher('chatter', Image, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    
    rospy.Subscriber("config", String, callback_config)
    r = rospy.Rate(fps)
    
    while not rospy.is_shutdown():
        try:
            if cam in range(len(camList)):
                frame = cv.QueryFrame(cap)
                if frame is not None:
                    frame = np.asarray(frame[:,:])
                    pub.publish(bridge.cv2_to_imgmsg(frame, "bgr8"))
        except Exception:
            pass
        r.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
