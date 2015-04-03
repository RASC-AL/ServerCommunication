#!/usr/bin/env python
# Software License Agreement (BSD License)

import rospy
from std_msgs.msg import String
import os

from conf import COMM_FILE

def talker():
    pub = rospy.Publisher('config', String, queue_size=1)
    rospy.init_node('talker_config', anonymous=True)
    r = rospy.Rate(1) # 10hz
    
    print os.getcwd()
    
    while not rospy.is_shutdown():
        if os.path.exists(COMM_FILE):
            with open(COMM_FILE) as f:
                conf_str = f.read()
                pub.publish(conf_str)
        r.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException: pass
