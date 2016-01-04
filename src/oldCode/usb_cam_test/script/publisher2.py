#!/usr/bin/env python
import roslib
roslib.load_manifest('usb_cam_test')
import sys
import rospy
import cv
import cv2
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import time


height=str(640)
width=str(480)
fps=str(30)
cam0=str(1)
cam1=str(0)
cam2=str(0)
cam3=str(0)
cam4=str(0)
capture=cv.CaptureFromCAM(0)
check_fps_set=0


def callback(data):
    print "Call Back Reached"
    global height
    global width
    global capture
    global fps
    global cam0
    global cam1
    global cam2
    global cam3
    global cam4
    global check_fps_set
    string=str(data.data)
    b=string.split(',')
    height=str(b[6])
    width=str(b[7])
    cam0=str(b[0])
    cam1=str(b[1])
    cam2=str(b[2])
    cam3=str(b[3])
    cam4=str(b[4])
    fps=str(b[5])
    if cam0==str(1):
        capture=cv.CaptureFromCAM(0)
    if cam1==str(1):
        capture=cv.CaptureFromCAM(1)
    if cam2==str(1):
        capture=cv.CaptureFromCAM(2)
    if cam3==str(1):
        capture=cv.CaptureFromCAM(3)
    if cam4==str(1):
        capture=cv.CaptureFromCAM(4)
    check_fps_set=1
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,int(width))
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,int(height))
        
def talker():
    #cv.NamedWindow("")
    global height
    global width
    global fps
    global check_fps_set
    #capture =cv.CaptureFromCAM(0)
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_WIDTH,int(width))
    cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FRAME_HEIGHT,int(height))
    #cv.SetCaptureProperty(capture,cv.CV_CAP_PROP_FPS,2)
    #rate=cv.GetCaptureProperty(capture,cv.CV_CAP_PROP_FPS)
    #print rate
    bridge=CvBridge()
    pub = rospy.Publisher('chatter', Image)
    rospy.init_node('talker', anonymous=True)
    
    rospy.Subscriber("config", String, callback)
    r = rospy.Rate(int(fps)) # 10hz
    frames=0
    start_time=0
    check=0
    while not rospy.is_shutdown():
        #str = "hello world %s"%rospy.get_time()
        frame=cv.QueryFrame(capture)
	if check==0:
		check=1
		start_time=time.time()
        if check_fps_set==1:
        	r = rospy.Rate(int(fps))
        	print "fps: " + fps
        	check_fps_set=0
	frames=frames+1
	if frames%10==0:
		curtime=time.time()
		diff=curtime-start_time
		fps=frames/diff
		print fps
        #ret,frame=capture.read()
        image=np.asarray(frame[:,:])
	#a=image.shape
	#print a
        #rospy.loginfo(st)
	r.sleep()
        pub.publish(bridge.cv_to_imgmsg(image, "bgr8"))

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
