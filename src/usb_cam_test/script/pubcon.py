#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('config', String)
    rospy.init_node('pubcon', anonymous=True)
    #a=str(0)
    #r = rospy.Rate(10) # 10hz
    cam=str(0)
    while not rospy.is_shutdown():
        CameraNo=input("Enter the camera number:")
        height= input("Enter the image height:")
        width=input("Enter the image width:")
        fps=input("Enter the frame rate:")
        if CameraNo==0:
            cam=0
        if CameraNo==1:
            cam=1
        if CameraNo==2:
            cam=2
        if CameraNo==3:
            cam=3
        if CameraNo==4:
            cam=4
        string =str(cam)+","+str(fps)+","+str(width)+","+str(height)
        print string
        #rospy.loginfo(str)
        pub.publish(string)
        #r.sleep(g

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
