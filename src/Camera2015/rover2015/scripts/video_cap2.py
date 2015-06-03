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

# see my-webcam.rules for cameras mapping
# 0->video7, 1->video6, ...
# camList = [7,6,5,4]
from conf import camList, audioList

prev_fps = 15
prev_cam = 0
cam = 0
fps = 15
cmd = ""
pro = 0

def getCommand():
    rospy.logerr('fps : ' + str(fps))
    #rospy.logerr("Current cam:"+str(cam))
    return ['gst-launch-0.10', 'v4l2src', 'device=/dev/video' + str(camList[cam]), '!', 'videorate', '!', 'video/x-raw-yuv,width=320,height=240,framerate=' + str(fps) + '/1', '!', 'ffmpegcolorspace', '!', 'jpegenc', '!', 'rtpjpegpay', '!', 'udpsink', 'host=128.205.55.128', 'port=5632', 'pulsesrc','device=' + audioList[cam], '!', 'audioconvert', '!', 'audio/x-raw-int,channels=1,width=16,depth=16,rate=8000', '!', 'amrnbenc', '!', 'rtpamrpay', '!', 'udpsink', 'host=128.205.55.128', 'port=6112']
    #return ['gst-launch-0.10', '-v', 'v4l2src', 'device=/dev/video' + str(camList[cam]), '!', 'videorate', '!', 'video/x-raw-yuv,width=320,height=240,framerate='+str(fps)+'/1', '!', 'ffmpegcolorspace', '!', 'jpegenc', '!', 'rtpjpegpay', '!', 'udpsink', 'sync=false', 'async=false', 'host=128.205.55.128', 'port=5632', 'pulsesrc', 'device=' + audioList[cam], '!', 'audioconvert', '!', 'audio/x-raw-int,channels=1,depth=16,width=16,rate=8000', '!', 'rtpL16pay', '!', 'udpsink', 'host=128.205.55.128', 'port=6112', 'sync=false', 'async=false']
    #return ['gst-launch-0.10', '-v', 'v4l2src', 'device=/dev/video' + str(camList[cam]), '!', 'video/x-raw-yuv,width=320,height=240','!', 'ffmpegcolorspace', '!', 'jpegenc', '!', 'rtpjpegpay', '!', 'udpsink', 'host=128.205.55.128', 'port=5632', 'sync=false']
    #return ['gst-launch-0.10', '-v', 'v4l2src', 'device=/dev/video' + str(camList[cam]), '!', 'videorate', '!','video/x-raw-yuv,width=320,height=240,framerate='+str(fps)+'/1','!', 'ffmpegcolorspace', '!', 'jpegenc', '!', 'rtpjpegpay', '!', 'udpsink', 'host=128.205.55.128', 'port=5632', 'sync=false', 'pulsesrc', 'device=' + audioList[cam], '!', 'audioconvert', '!', 'audio/x-raw-int,channels=1,depth=16,width=16,rate=22000', '!', 'rtpL16pay', '!', 'udpsink', 'host=128.205.55.128', 'port=6112']
    #return ['gst-launch-1.0', '-v', 'v4l2src', 'device=/dev/video' + str(camList[cam]), '!', 'video/x-raw, format=YUV2, width=320, height=240','!', 'videoconvert', '!', 'jpegenc', '!', 'rtpjpegpay', '!', 'udpsink', 'host=128.205.55.128', 'port=5632', 'sync=false']

    #return ['gst-launch-0.10', '-v', 'v4l2src', 'device=/dev/video' + str(camList[cam]), '!', 'video/x-raw-yuv,width=320,height=240,framerate=15/1', '!', 'ffmpegcolorspace', '!', 'x264enc', 'tune=zerolatency', 'byte-stream=true', 'bitrate=3000', 'threads=2', '!', 'rtph264pay', '!', 'udpsink', 'host=128.205.55.128', 'port=1234', 'sync=false'] 
   #return ['gst-launch-0.10', '-v', 'v4l2src', 'device=/dev/video5', '!', 'video/x-raw-yuv,width=320,height=240,framerate=10/1', '!', 'ffenc_mpeg4', '!', 'rtpmp4vpay', 'send-config=true', '!', 'udpsink', 'host=128.205.55.128', 'port=5632']
   #return ['gst-launch-0.10', '-v', 'v4l2src', 'device=/dev/video' + str(camList[cam]), '!', 'video/x-raw-yuv,width=320,height=240', '!', 'ffmpegcolorspace', '!', 'theoraenc', '!', 'rtptheorapay', '!', 'udpsink', 'host=128.205.55.128', 'port=5632', 'sync=false']
    #return ['gst-launch-0.10', '-v', 'v4l2src', 'device=/dev/video' + str(camList[cam]), '!', 'videorate', '!', 'video/x-raw-yuv,width=320,height=240,framerate=15/1', '!', 'ffenc_mpeg4', '!', 'rtpmp4vpay', 'send-config=true', '!', 'udpsink', 'host=128.205.55.128', 'port=5632', 'pulsesrc', 'device=' + audioList[cam], '!', 'audioconvert', '!', 'audio/x-raw-int,channels=1,depth=16,width=16,rate=22000', '!', 'rtpL16pay', '!', 'udpsink', 'host=128.205.55.128', 'port=6112']
    

def checkcamList(camList):
    stream=os.popen("ls /dev/video*")
    devices = stream.read().split()
    for i in camList:
        if '/dev/video' + str(i) not in devices:
            warnings.warn('/dev/video' + str(i) + ' does not exist!')

def callback_config(msg):
    global prev_fps
    global prev_cam
    global cam
    global fps
    global pro
    rospy.logerr('camera change message' + str(msg.data))
    s = str(msg.data).split(',')
    cam = int(s[0])
    fps = int(s[1])
    if ((cam != prev_cam and cam in range(len(camList))) or (fps != prev_fps)):
	if cam > 1:
            rospy.sleep(2.)
        rospy.logerr('killing curent camera')
	pro.kill()
        pro = sub.Popen(getCommand(), stdout = sub.PIPE, stderr = sub.PIPE)
        rospy.logerr('starting camera')
        prev_cam = cam
	prev_fps = fps
    
def listener():
    rospy.init_node('talker', anonymous=True)
    rospy.Subscriber("config", String, callback_config)
    rospy.spin()

if __name__ == '__main__':
    checkcamList(camList)
    cmd = getCommand()
    pro = sub.Popen(cmd, stdout = sub.PIPE, stderr = sub.PIPE)
    listener()
