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

cam = 0

def callback(data):
    command = str(data.data)
    global cam 
    cam = int(command[0])
    test = rospy.Publisher('blob_test', String, queue_size = 1)
    test.publish(str(cam))
    #print command

def talker():
    global cap1
    global cap2

    global cam
    cam = 0

    bridge=CvBridge()

    pub = rospy.Publisher('blob', Image)
    pub_flag = rospy.Publisher('ReturnData', String, queue_size = 1)
    rospy.init_node('blob', anonymous=True)

    rospy.Subscriber('HomeCam', String, callback)
    #rospy.spin()

    #rospy.Subscriber("configCam", String, cam_setup)

    #cap1=cv2.VideoCapture(0)
    #cap1.set(3,320)
    #cap1.set(4,240)
    #cap1.set(cv.CV_CAP_PROP_FPS,5)
    #cap2=cv2.VideoCapture(2)
    #cap2.set(3,320)
    #cap2.set(4,240)
    #cap2.set(cv.CV_CAP_PROP_FPS,5)

    lower_blue = np.array([80,100,60])
    upper_blue = np.array([120,255,255])
    lower_green = np.array([50,90,0])
    upper_green = np.array([75,255,255])
    lower_red=np.array([170,160,60])
    upper_red=np.array([180,255,255])
    lower_orange=np.array([0,160,40])
    upper_orange=np.array([17,255,255])
    lower_yellow=np.array([23,160,60])
    upper_yellow=np.array([35,255,255])
    lower_violet=np.array([135,160,60])
    upper_violet=np.array([155,255,255])

    

    while ((not rospy.is_shutdown())):
        if cam<2:
		flag = 0

		cap1=cv2.VideoCapture(4)
		#cap1.set(18,3000)
		#cap1.set(18,320)
		#cap1.set(19,320)
		_,frame1=cap1.read()
		cap1.release()

		cap2=cv2.VideoCapture(5)
		_,frame2=cap2.read()
		cap2.release()

		image1=frame1
		image2=frame2

		

		image1=np.asarray(image1[:,:])        
		image2=np.asarray(image2[:,:])

		hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
		hsv2 = cv2.cvtColor(image2, cv2.COLOR_BGR2HSV)

		mask1 = cv2.inRange(hsv1, lower_green, upper_green)
		mask2 = cv2.inRange(hsv1, lower_blue, upper_blue)
		mask3 = cv2.inRange(hsv1, lower_red, upper_red)
		mask4 = cv2.inRange(hsv1, lower_yellow, upper_yellow)
		mask5 = cv2.inRange(hsv1, lower_orange, upper_orange)
		mask6 = cv2.inRange(hsv1, lower_violet, upper_violet)
		mask7 = cv2.inRange(hsv2, lower_green, upper_green)
		mask8 = cv2.inRange(hsv2, lower_blue, upper_blue)
		mask9 = cv2.inRange(hsv2, lower_red, upper_red)
		mask10 = cv2.inRange(hsv2, lower_yellow, upper_yellow)
		mask11 = cv2.inRange(hsv2, lower_orange, upper_orange)
		mask12 = cv2.inRange(hsv2, lower_violet, upper_violet)

		contours1, hierarchy1 = cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if len(contours1) > 0:
		    flag=1
		for i in contours1:
		    x1,y1,w1,h1 = cv2.boundingRect(i)
		    cv2.rectangle(image1,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
		       
		contours2, hierarchy2 = cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if len(contours2) > 0:
		    flag=1
		for i in contours2:
		    x2,y2,w2,h2 = cv2.boundingRect(i)
		    cv2.rectangle(image1,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
		       
		contours3, hierarchy3 = cv2.findContours(mask3,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if len(contours3) > 0:
		    flag=1
		for i in contours3:
		    x3,y3,w3,h3 = cv2.boundingRect(i)
		    cv2.rectangle(image1,(x3,y3),(x3+w3,y3+h3),(0,0,255),2)
		       
		contours4, hierarchy4 = cv2.findContours(mask4,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if len(contours4) > 0:
		    flag=1
		for i in contours4:
		    x4,y4,w4,h4 = cv2.boundingRect(i)
		    cv2.rectangle(image1,(x4,y4),(x4+w4,y4+h4),(0,255,255),2)
		       
		contours5, hierarchy5 = cv2.findContours(mask5,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if len(contours5) > 0:
		    flag=1
		for i in contours5:
		    x5,y5,w5,h5 = cv2.boundingRect(i)
		    cv2.rectangle(image1,(x5,y5),(x5+w5,y5+h5),(0,165,255),2)
		       
		contours6, hierarchy6 = cv2.findContours(mask6,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if len(contours6) > 0:
		    flag=1
		for i in contours6:
		    x6,y6,w6,h6 = cv2.boundingRect(i)
		    cv2.rectangle(image1,(x6,y6),(x6+w6,y6+h6),(238,130,238),2)


	###############################################################################
		
		contours7, hierarchy7 = cv2.findContours(mask7,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if len(contours7) > 0:
		    flag=1
		for i in contours7:
		    x7,y7,w7,h7 = cv2.boundingRect(i)
		    cv2.rectangle(image2,(x7,y7),(x7+w7,y7+h7),(0,255,0),2)
	       
		contours8, hierarchy8 = cv2.findContours(mask8,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if len(contours8) > 0:
		    flag=1
		for i in contours8:
		    x8,y8,w8,h8 = cv2.boundingRect(i)
		    cv2.rectangle(image2,(x8,y8),(x8+w8,y8+h8),(255,0,0),2)

		contours9, hierarchy9 = cv2.findContours(mask9,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if len(contours9) > 0:
		    flag=1
		for i in contours9:
		    x9,y9,w9,h9 = cv2.boundingRect(i)
		    cv2.rectangle(image2,(x9,y9),(x9+w9,y9+h9),(0,0,255),2)

		contours10, hierarchy10 = cv2.findContours(mask10,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if len(contours10) > 0:
		    flag=1
		for i in contours10:
		    x10,y10,w10,h10 = cv2.boundingRect(i)
		    cv2.rectangle(image2,(x10,y10),(x10+w10,y10+h10),(0,255,255),2)

		contours11, hierarchy11 = cv2.findContours(mask11,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if len(contours11) > 0:
		    flag=1
		for i in contours11:
		    x11,y11,w11,h11 = cv2.boundingRect(i)
		    cv2.rectangle(image2,(x11,y11),(x11+w11,y11+h11),(0,165,255),2)

		contours12, hierarchy12 = cv2.findContours(mask12,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
		if len(contours12) > 0:
		    flag=1
		for i in contours12:
		    x12,y12,w12,h12 = cv2.boundingRect(i)
		    cv2.rectangle(image2,(x12,y12),(x12+w12,y12+h12),(238,130,238),2)

		both=np.hstack((image1,image2))

		bitmap = cv.CreateImageHeader((both.shape[1], both.shape[0]), cv.IPL_DEPTH_8U, 3)
		cv.SetData(bitmap, both.tostring(), both.dtype.itemsize * 3 * both.shape[1])

		bit = np.asarray(bitmap[:,:])

		#cv2.imshow('Video', bit)         
		
		pub.publish(bridge.cv_to_imgmsg(bitmap, "bgr8"))
		data = "b"+str(flag)
		pub_flag.publish(data)
		#print flag

		cv2.waitKey(2000)


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
