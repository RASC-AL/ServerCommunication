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



global capture, test
bridge=CvBridge()
capture=cv.CaptureFromCAM(0)
while True:

    frame=cv.QueryFrame(capture)

    image=frame;
    image=np.asarray(image[:,:])

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)


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

    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask2 = cv2.inRange(hsv, lower_blue, upper_blue)
    mask3 = cv2.inRange(hsv, lower_red, upper_red)
    mask4 = cv2.inRange(hsv, lower_yellow, upper_yellow)
    mask5 = cv2.inRange(hsv, lower_orange, upper_orange)
    mask6 = cv2.inRange(hsv, lower_violet, upper_violet)    

    res = cv2.bitwise_and(image,image, mask= mask)
    im1=cv2.cvtColor(res,cv2.COLOR_BGR2GRAY)
    contours1, hierarchy1 = cv2.findContours(im1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for i in contours1:
        x1,y1,w1,h1 = cv2.boundingRect(i)
        cv2.rectangle(image,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
    res2 = cv2.bitwise_and(image,image, mask= mask2)
    im2=cv2.cvtColor(res2,cv2.COLOR_BGR2GRAY)
    contours2, hierarchy2 = cv2.findContours(im2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for i in contours2:
        x2,y2,w2,h2 = cv2.boundingRect(i)
        cv2.rectangle(image,(x2,y2),(x2+w2,y2+h2),(255,0,0),2)
    res3 = cv2.bitwise_and(image,image, mask= mask3)
    im3=cv2.cvtColor(res3,cv2.COLOR_BGR2GRAY)
    contours3, hierarchy3 = cv2.findContours(im3,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for i in contours3:
        x3,y3,w3,h3 = cv2.boundingRect(i)
        cv2.rectangle(image,(x3,y3),(x3+w3,y3+h3),(0,0,255),2)
    res4 = cv2.bitwise_and(image,image, mask= mask4)
    im4=cv2.cvtColor(res4,cv2.COLOR_BGR2GRAY)
    contours4, hierarchy4 = cv2.findContours(im4,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for i in contours4:
        x4,y4,w4,h4 = cv2.boundingRect(i)
        cv2.rectangle(image,(x4,y4),(x4+w4,y4+h4),(0,255,255),2)
    res5 = cv2.bitwise_and(image,image, mask= mask5)
    im5=cv2.cvtColor(res5,cv2.COLOR_BGR2GRAY)
    contours5, hierarchy5 = cv2.findContours(im5,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for i in contours5:
        x5,y5,w5,h5 = cv2.boundingRect(i)
        cv2.rectangle(image,(x5,y5),(x5+w5,y5+h5),(0,165,255),2)
    res6 = cv2.bitwise_and(image,image, mask= mask6)
    im6=cv2.cvtColor(res6,cv2.COLOR_BGR2GRAY)
    contours6, hierarchy6 = cv2.findContours(im6,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for i in contours6:
        x6,y6,w6,h6 = cv2.boundingRect(i)
        cv2.rectangle(image,(x6,y6),(x6+w6,y6+h6),(238,130,238),2)

    cv2.imshow('Video', image)   

    if cv2.waitKey(30)==27:
	break


	

