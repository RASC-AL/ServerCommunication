#!/usr/bin/env python
# Software License Agreement (BSD License)

import rospy
from std_msgs.msg import String
import os

from conf import COMM_FILE

cam = 0
pub = rospy.Publisher('config', String, queue_size=1)

'''
def talker():
    global cam
    
    rospy.init_node('talker_config', anonymous=True)
    r = rospy.Rate(1) # 10hz
    
    print os.getcwd()
    
    while not rospy.is_shutdown():
        if os.path.exists(COMM_FILE):
            with open(COMM_FILE) as f:
                conf_str = f.read()
                pub.publish(conf_str)
        r.sleep()
'''

def callback(data):
        pub.publish(data)
        
def talker():
        rospy.init_node("Cam_Config")
        rospy.Subscriber('HomeCam', String, callback)
        rospy.spin()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
