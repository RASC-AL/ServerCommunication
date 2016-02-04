#!/usr/bin/env python
import rospy
import math
import time
from sensor_msgs.msg import Joy
from std_msgs.msg import String

class ArmController:

    def __init__(self):
        self.armPub = rospy.Publisher('ARM', String, queue_size = 1)
        self.testPub = rospy.Publisher('ArmTest', String, queue_size = 1)   
        
        self.base = 1500.0
        self.base_mod = 4
        self.base_min = 1100.0
        self.base_max = 1900.0

        self.wrist = 1500.0
        self.wrist_mod = 4
        self.wrist_min = 600.0
        self.wrist_max = 2100.0

        self.scoop = 1

        self.instructionsPerSecond = 16.0

    def callback(self, data):
        now = rospy.get_time()
	ind = -1
        pos = False

        try:
            ind = data.buttons.index(1)
        except ValueError: pass
	#Arm control
        #Base Servo left
        if data.axes[2] < 0:
            self.base -= data.axes[2] / self.base_mod * 80;
            self.base = self.base_max if self.base > self.base_max else self.base
        #Base Servo right
        elif data.axes[5] < 0:
            self.base += data.axes[5] / self.base_mod * 80;
            self.base = self.base_min if self.base < self.base_min else self.base
        
        #Shoulder forward and back
        if math.fabs(data.axes[1]) > .2:
            shoulder = data.axes[1] * 127 + 127;
        else:
            shoulder = 127

        #Wrist up and down
        if ind == 5 and math.fabs(data.axes[4]) > .2:
            elbow = 127
            self.wrist += data.axes[4] / self.wrist_mod * 180;
            if self.wrist > self.wrist_max:
                self.wrist = self.wrist_max
            elif self.wrist < self.wrist_min:
                self.wrist = self.wrist_min
        #Elbow forward and back 
        elif math.fabs(data.axes[4]) > .2:
            elbow = data.axes[4] * 127 + 127;
        else:
            elbow = 127

        #Scoop open
	if ind == 0:
            self.scoop = 1
	#Scoop close
	elif ind == 1:
	    self.scoop = 0
	#Drop Position (X)
	elif ind == 2:
	    elbow = 1194.0
            shoulder = 1000.0
            self.base = 1800.0
            pos = True
	#Home Position (Y)
	elif ind == 3:
	    elbow = 1100.0
	    shoulder = 1000.0
	    self.base = 1500.0
	    pos = True 
        elif ind == 4:
            drvPub.publish('STOP')
        elif ind == 13:
            drvPub.publish('GO')

        leadChar = 'l' if pos else 's'

        rospy.sleep((1 / self.instructionsPerSecond)-(rospy.get_time()-now))
        self.armPub.publish(leadChar+str(int(elbow))+','+str(int(shoulder))+','+str(int(self.base))+','+str(int(self.wrist))+','+str(int(self.scoop))+',')
       
def controller():
    rospy.init_node('xboxArmSpeed', anonymous = True)
    armController = ArmController()
    rospy.Subscriber('joy1', Joy, armController.callback, queue_size=1)
    rospy.spin()

if __name__ == '__main__':
    controller()

