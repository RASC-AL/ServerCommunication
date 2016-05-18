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
#import gi
#gi.require_version('Gst', '1.0')
#from gi.repository import Gst
import gst
import imp

# see my-webcam.rules for cameras mapping
# 0->video7, 1->video6, ...
# camList = [7,6,5,4]
from conf import camList, audioList

class VideoCapture:

    def __init__(self): 
        self.prev_fps = 15
        self.fps = 15
        self.prev_cam = 4
        self.cam = 4
        self.det_cam = 6
        ipGetter = imp.load_source('ipGetter', '/home/sbrover/Rover2015/src/ipGetter.py')
        self.homeIP = ipGetter.getHomeIP()
        self.setCommand()
        self.setDetCommand()
        self.checkcamList(camList)
        self.player = gst.parse_launch(self.streamCommand)
        self.player.set_state(gst.STATE_PLAYING)
        self.detPlayer = gst.parse_launch(self.detCommand)
        self.detPlayer.set_state(gst.STATE_PLAYING)

    def setCommand(self):
        rospy.logerr('fps : ' + str(self.fps))
        rospy.logerr("Current cam:"+str(self.cam))
        rospy.logerr(self.homeIP)

        '''
        #H264
        self.streamCommand = 'v4l2src device=/dev/video' + str(self.cam) + ' ! video/x-raw-yuv, framerate=' + str(self.fps) + '/1, width=640, height=480 ! x264enc pass=qual quantizer=20 tune=zerolatency ! rtph264pay ! udpsink host=' + self.homeIP + ' port=1234 v4l2src device=/dev/video' + str(self.cam + 1) + ' ! video/x-raw-yuv, framerate=' + str(self.fps) + '/1, width=640, height=480 ! x264enc pass=qual quantizer=20 tune=zerolatency ! rtph264pay ! udpsink host=' + self.homeIP + ' port=1235'

        self.streamCommand = 'mpegtsmux name="muxer" ! udpsink host=' + self.homeIP + ' port=1234 v4l2src device=/dev/video' + str(self.cam) + ' ! video/x-raw-yuv, framerate=' + str(self.fps) + '/1, width=640, height=480 ! x264enc pass=qual quantizer=20 tune=zerolatency ! muxer. v4l2src device=/dev/video' + str(self.cam + 1) + ' ! video/x-raw-yuv, framerate=' + str(self.fps) + '/1, width=640, height=480 ! x264enc pass=qual quantizer=20 tune=zerolatency ! muxer.'

        self.testPlayer = gst.parse_launch('udpsrc port=1234 caps="application/x-rtp, payload=127" ! rtph264depay ! ffdec_h264 ! xvimagesink sync=false udpsrc port=1235 caps="application/x-rtp, payload=127" ! rtph264depay ! ffdec_h264 ! xvimagesink sync=false')

        self.testPlayer = gst.parse_launch('udpsrc port=1234 caps="video/mpegts, systemstream=(boolean)true, packetsize=(int)188" ! tsdemux ! ffdec_h264 ! xvimagesink sync=false udpsrc port=1234 caps="video/mpegts, systemstream=(boolean)true, packetsize=(int)188" ! tsdemux ! ffdec_h264 ! xvimagesink sync=false')
        '''

        #JPEG
        
        self.streamCommand = 'v4l2src device=/dev/video' + str(self.cam) + ' ! video/x-raw-yuv, framerate=' + str(self.fps) + '/1, width=640, height=480 ! ffmpegcolorspace ! jpegenc ! rtpjpegpay ! udpsink host=' + self.homeIP + ' port=1234'

        #self.testPlayer1 = gst.parse_launch('udpsrc port=1234 caps="application/x-rtp, payload=127" ! rtpjpegdepay ! jpegdec ! xvimagesink sync=false')

        #self.testPlayer1.set_state(gst.STATE_PLAYING)

    def setDetCommand(self):

        self.detCommand = 'v4l2src device=/dev/video' + str(self.det_cam) + ' ! video/x-raw-yuv, framerate=' + str(self.fps) + '/1, width=640, height=480 ! ffmpegcolorspace ! jpegenc ! rtpjpegpay ! udpsink host=' + self.homeIP + ' port=1235'
        #self.testPlayer2 = gst.parse_launch('udpsrc port=1235 caps="application/x-rtp, payload=127" ! rtpjpegdepay ! jpegdec ! xvimagesink sync=false')

        #self.testPlayer2.set_state(gst.STATE_PLAYING)

    def checkcamList(self, camList):
        stream=os.popen("ls /dev/video*")
        devices = stream.read().split()
        for i in camList:
            if '/dev/video' + str(i) not in devices:
                warnings.warn('/dev/video' + str(i) + ' does not exist!')

    def callback_config(self, msg):
        rospy.logerr('Drive camera change message ' + str(msg.data))
        s = str(msg.data).split(',')
        self.cam = int(s[0])
        self.fps = int(s[1])
        if ((self.cam != self.prev_cam) or (self.fps != self.prev_fps)):
            rospy.logerr('killing current camera')
            self.player.set_state(gst.STATE_NULL)
            self.setCommand()
            self.player = gst.parse_launch(self.streamCommand)
            self.player.set_state(gst.STATE_PLAYING)
            self.prev_cam = self.cam
            self.prev_fps = self.fps
 
    def callback_ptz(self, msg):
        rospy.logerr('PTZ camera change message ' + str(msg.data))
        newCam = 6 + int(msg.data)
        if newCam != self.det_cam:
            self.det_cam = newCam
            self.detPlayer.set_state(gst.STATE_NULL)
            self.setDetCommand()
            self.detPlayer = gst.parse_launch(self.detCommand)
            self.detPlayer.set_state(gst.STATE_PLAYING)

def listener():
    rospy.init_node('talker', anonymous=True)
    videoCapture = VideoCapture()
    rospy.Subscriber("config", String, videoCapture.callback_config)
    rospy.Subscriber("PTZ", String, videoCapture.callback_ptz)
    rospy.spin()

if __name__ == '__main__':
    listener()
