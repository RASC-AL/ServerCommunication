#!/usr/bin/env python
# Software License Agreement (BSD License)

import rospy
import os

from conf import HOME_IP

def talker():
    cmd = '''gst-launch-0.10 -evt souphttpsrc location='http://127.0.0.1:8080/stream?topic=/chatter' is_live=true timeout=5 ! multipartdemux ! image/jpeg, width=640, height=480, framerate=15/1 ! ffdec_mjpeg ! x264enc pass=qual quantizer=20 tune=zerolatency ! rtph264pay ! udpsink host=128.205.54.9 port=1234'''
    cmd = '''gst-launch-0.10 -evt souphttpsrc location='http://127.0.0.1:8080/stream?topic=/chatter' is_live=true timeout=5 ! multipartdemux ! image/jpeg ! ffdec_mjpeg ! x264enc pass=qual quantizer=20 tune=zerolatency ! rtph264pay ! udpsink host=%s port=1234''' % HOME_IP
    os.system(cmd)
    rospy.init_node('gstreamer', anonymous=True)
    r = rospy.Rate(10) # 10hz
    while not rospy.is_shutdown():
        r.sleep()
        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
