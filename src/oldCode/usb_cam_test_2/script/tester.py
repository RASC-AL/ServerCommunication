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

stream=os.popen("ls /dev/video*")
a= stream.read()
#print a[1]

b= a.split('\n')
#arlen=len(b)
i=0
List=[]
for device in b:
	x=re.findall(r'\d+',device)
	List=List+x

print "Available Video Devices:\n"

print List



cam_no=[]
cam_no.append(int(List[0]))
cam_no.append(int(List[1]))
cam_no.append(int(List[2]))
cam_no.append(int(List[3]))
test=0

def cam_setup(setup_data):
    global cam_no, test
    string=str(setup_data.data)
    print "Config cam string: " + string
    b=string.split(',')
    '''cam_no[0]=int(b[int(List[0])])
    cam_no[1]=int(b[int(List[1])])
    cam_no[2]=int(b[int(List[2])])
    cam_no[3]=int(b[int(List[3])])'''
    cam_no[0]=int(List[int(b[0])])
    cam_no[1]=int(List[int(b[1])])
    cam_no[2]=int(List[int(b[2])])
    cam_no[3]=int(List[int(b[3])])
    test=1




def talker():
    global capture, test
    global capture1 
    bridge=CvBridge()
    pub = rospy.Publisher('blobs', Image)
    rospy.init_node('talker', anonymous=True)
    rospy.Subscriber("configCam", String, cam_setup)
    while test==0:
        pass
    capture=cv.CaptureFromCAM(cam_no[2])
    capture1=cv.CaptureFromCAM(cam_no[3])
    #capture=cv.CaptureFromCAM(1)
    #capture1=cv.CaptureFromCAM(2)
    while not rospy.is_shutdown():
        
        
        frame=cv.QueryFrame(capture)
        #print '1'
        #image=cv2.imread('/home/niranjan/Desktop/Rock-Colors.JPG')
        #capture=cv.CaptureFromCAM(2)
        #print '2'
        frame1=cv.QueryFrame(capture1)
        #print frame
        #print '3'

        image=frame;
        image=np.asarray(image[:,:])
        image1=frame1;
        image1=np.asarray(image1[:,:])
        #print '4'
        #print image
      
        #print image1
        
        #both=np.hstack((image,image1))
        #print '5'
        #bitmap = cv.CreateImageHeader((both.shape[1], both.shape[0]), cv.IPL_DEPTH_8U, 3)
        #cv.SetData(bitmap, both.tostring(), both.dtype.itemsize * 3 * both.shape[1])
        #print '6'
        #frame=both
        #print type(frame)
        #print '2'
        #image=both
        '''medianB=np.median(image[:,:,0]);
        medianG=np.median(image[:,:,1]);
        medianR=np.median(image[:,:,2]);
        #print median
        diffB=128-medianB
        diffG=128-medianG
        diffR=128-medianR
        image[:,:,0]=image[:,:,0]+diffB
        image[:,:,1]=image[:,:,1]+diffG
        image[:,:,2]=image[:,:,2]+diffR
        image[image>=255]=254
        image[image<=0]=1'''
        #print maxi
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hsv1 = cv2.cvtColor(image1, cv2.COLOR_BGR2HSV)
        '''
        lower_blue = np.array([80,80,0])
        upper_blue = np.array([130,255,255])
        lower_green = np.array([50,80,0])
        upper_green = np.array([79,255,255])
        lower_red=np.array([0,160,0])
        upper_red=np.array([40,255,255])
        '''

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

        '''

        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask2 = cv2.inRange(hsv, lower_blue, upper_blue)
        mask3 = cv2.inRange(hsv, lower_red, upper_red)

        '''
        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask2 = cv2.inRange(hsv, lower_blue, upper_blue)
        mask3 = cv2.inRange(hsv, lower_red, upper_red)
        mask4 = cv2.inRange(hsv, lower_yellow, upper_yellow)
        mask5 = cv2.inRange(hsv, lower_orange, upper_orange)
        mask6 = cv2.inRange(hsv, lower_violet, upper_violet)
        '''
        mask4 = cv2.inRange(hsv1, lower_green, upper_green)
        mask5 = cv2.inRange(hsv1, lower_blue, upper_blue)
        mask6 = cv2.inRange(hsv1, lower_red, upper_red)
        '''

        mask7 = cv2.inRange(hsv1, lower_green, upper_green)
        mask8 = cv2.inRange(hsv1, lower_blue, upper_blue)
        mask9 = cv2.inRange(hsv1, lower_red, upper_red)
        mask10 = cv2.inRange(hsv1, lower_yellow, upper_yellow)
        mask11 = cv2.inRange(hsv1, lower_orange, upper_orange)
        mask12 = cv2.inRange(hsv1, lower_violet, upper_violet)
        #a=image.shape
        #print a
        '''for i in range(1,a[1]):
            for j in range(1,a[2]):
                temp=image[i,j]
                temp=temp+diff
                print type(temp)
                if(temp<=255 and temp>=0):
                    image[i,j]=temp
        '''

    
        
        #maxi=np.min(image)
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


###############################################################################
        res7 = cv2.bitwise_and(image1,image1, mask= mask7)
        im7=cv2.cvtColor(res7,cv2.COLOR_BGR2GRAY)
        contours7, hierarchy7 = cv2.findContours(im7,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in contours7:
            x7,y7,w7,h7 = cv2.boundingRect(i)
            cv2.rectangle(image1,(x7,y7),(x7+w7,y7+h7),(0,255,0),2)
        res8 = cv2.bitwise_and(image1,image1, mask= mask8)
        im8=cv2.cvtColor(res8,cv2.COLOR_BGR2GRAY)
        contours8, hierarchy8 = cv2.findContours(im8,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in contours8:
            x8,y8,w8,h8 = cv2.boundingRect(i)
            cv2.rectangle(image1,(x8,y8),(x8+w8,y8+h8),(255,0,0),2)
        res9 = cv2.bitwise_and(image1,image1, mask= mask9)
        im9=cv2.cvtColor(res9,cv2.COLOR_BGR2GRAY)
        contours9, hierarchy9 = cv2.findContours(im9,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in contours9:
            x9,y9,w9,h9 = cv2.boundingRect(i)
            cv2.rectangle(image1,(x9,y9),(x9+w9,y9+h9),(0,0,255),2)
        res10 = cv2.bitwise_and(image1,image1, mask= mask10)
        im10=cv2.cvtColor(res4,cv2.COLOR_BGR2GRAY)
        contours10, hierarchy10 = cv2.findContours(im10,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in contours10:
            x10,y10,w10,h10 = cv2.boundingRect(i)
            cv2.rectangle(image1,(x10,y10),(x10+w10,y10+h10),(0,255,255),2)
        res11 = cv2.bitwise_and(image1,image1, mask= mask11)
        im11=cv2.cvtColor(res11,cv2.COLOR_BGR2GRAY)
        contours11, hierarchy11 = cv2.findContours(im11,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in contours11:
            x11,y11,w11,h11 = cv2.boundingRect(i)
            cv2.rectangle(image1,(x11,y11),(x11+w11,y11+h11),(0,165,255),2)
        res12 = cv2.bitwise_and(image1,image1, mask= mask12)
        im12=cv2.cvtColor(res12,cv2.COLOR_BGR2GRAY)
        contours12, hierarchy12 = cv2.findContours(im12,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for i in contours12:
            x12,y12,w12,h12 = cv2.boundingRect(i)
            cv2.rectangle(image1,(x12,y12),(x12+w12,y12+h12),(238,130,238),2)


        


	#mask8 = cv2.cvtColor(mask, cv2.COLOR_HSV2BGR)
	#image[mask==0]=0
        #final=res+res3+res2
        #final=res+res2
        both=np.hstack((image,image1))
	#final=both
        #frame1=cv.fromarray(final)
        #frame1=final
        #im2=cv2.cvtColor(frame1,cv2.COLOR_BGR2GRAY)
        #im3=cv2.cvtColor(im2,cv2.COLOR_GRAY2BGR)
        #ret,thresh=cv2.threshold(im2,127,255,0)
        
        #contours, hierarchy = cv2.findContours(im2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        #for i in contours:
            #x,y,w,h = cv2.boundingRect(i)
            #cv2.rectangle(frame1,(x,y),(x+w,y+h),(0,255,0),2)
        #frame1=im3
        bitmap = cv.CreateImageHeader((both.shape[1], both.shape[0]), cv.IPL_DEPTH_8U, 3)
        cv.SetData(bitmap, both.tostring(), both.dtype.itemsize * 3 * both.shape[1])
        #frame1=cv.fromarray(frame1)
        #cv2.imshow('Features', im)       
        #frame=fin
	#res = cv2.bitwise_and(image,image, mask= mask3)
	#mask3=cv2.cvtColor(mask3,cv2.COLOR_GRAY2RGB)
	#frame=cv.fromarray(mask3)
        print bitmap
	
        
        pub.publish(bridge.cv_to_imgmsg(bitmap, "bgr8"))


if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
