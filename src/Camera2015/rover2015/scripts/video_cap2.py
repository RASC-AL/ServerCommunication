#!/usr/bin/env python
# Software License Agreement (BSD License)

import rospy
import os
import signal
import roslib
roslib.load_manifest('rover2015')
import numpy as np
import cv2
from cv2 import cv
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import warnings
import subprocess as sub
from conf import HOME_IP
import gst


# see my-webcam.rules for cameras mapping
# 0->video7, 1->video6, ...
# camList = [7,6,5,4]
from conf import camList, audioList

class VideoCapture:

    def __init__(self): 
        self.prev_fps = 15
        self.fps = 15
        self.prev_cam = 0
        self.cam = 0
        self.setCommand()
        self.checkcamList(camList)
        self.player = gst.parse_launch(self.streamCommand)
        self.player.set_state(gst.STATE_PLAYING)

    def setCommand(self):
        rospy.logerr('fps : ' + str(self.fps))
        rospy.logerr("Current cam:"+str(self.cam))
    
        self.streamCommand = 'v4l2src device=/dev/video' + str(self.cam) + ' ! video/x-raw-yuv,width=640,height=480 ! x264enc pass=qual quantizer=20 tune=zerolatency ! rtph264pay ! udpsink host=128.205.55.104 port=1234'

    def checkcamList(self, camList):
        stream=os.popen("ls /dev/video*")
        devices = stream.read().split()
        for i in camList:
            if '/dev/video' + str(i) not in devices:
                warnings.warn('/dev/video' + str(i) + ' does not exist!')

    def callback_config(self, msg):
        rospy.logerr('camera change message ' + str(msg.data))
        s = str(msg.data).split(',')
        self.cam = int(s[0])
        self.fps = int(s[1])
        if ((self.cam != self.prev_cam and self.cam in range(len(camList))) or (self.fps != self.prev_fps)):
	    if self.cam > 1:
                rospy.sleep(2.)
            rospy.logerr('killing current camera')
            self.player.set_state(gst.STATE_NULL)
            self.setCommand()
            self.player = gst.parse_launch(self.streamCommand)
            self.player.set_state(gst.STATE_PLAYING)
            self.prev_cam = self.cam
            self.prev_fps = self.fps
    
def listener():
    rospy.init_node('talker', anonymous=True)
    videoCapture = VideoCapture()
    rospy.Subscriber("config", String, videoCapture.callback_config)
    rospy.spin()

if __name__ == '__main__':
    listener()
