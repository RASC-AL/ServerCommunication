#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import Joy
from std_msgs.msg import String

armPub = rospy.Publisher('ARM',String, queue_size=10)

base = 1500.0
elbow = 1100.0
shoulder = 1100.0
wrist = 1500.0

base_mod = 4
elbow_mod = 17
shoulder_mod = 16
wrist_mod = 4

base_min = 1100.0
base_max = 1900.0

elbow_min = 1000.0
elbow_max = 2000.0

shoulder_min = 1000.0
shoulder_max = 2000.0

wrist_min = 600.0
wrist_max = 2400.0

scoop = 0

def callback(data):
        global base, base_min, base_max, elbow, elbow_min, elbow_max, shoulder, shoulder_min, shoulder_max, wrist, wrist_min, wrist_max, scoop
        now=rospy.get_time()
	ind = -1
        try:
                ind = data.buttons.index(1)
        except ValueError: pass
	#arm control
    	#Base Servo left
        if data.axes[2] < 0:
               	base += data.axes[2]/base_mod * 80;
                base = base_min if base < base_min else base
        #Base Servo right
        elif data.axes[5] < 0:
                base -= data.axes[5]/base_mod * 80;
                base = base_max if base > base_max else base
        #Elbow forward and back 
        if math.fabs(data.axes[1]) > .2:
                elbow += data.axes[1]/elbow_mod * 100;
                if elbow > elbow_max:
        	      	elbow = elbow_max
                elif elbow < elbow_min:
              		elbow = elbow_min
	#Wrist up and down
	if ind==5 and math.fabs(data.axes[4]) > .2:
        	wrist += data.axes[4]/wrist_mod * 180;
        	if wrist > wrist_max:
                	wrist = wrist_max
        	elif wrist < wrist_min:
                	wrist = wrist_min		
        #Shoulder forward and back
        elif math.fabs(data.axes[4]) > .2:
                shoulder += data.axes[4]/shoulder_mod * 100;
                if shoulder > shoulder_max:
                       	shoulder = shoulder_max
                elif shoulder < shoulder_min:          
              		shoulder = shoulder_min
	#Scoop open
	if ind==0:
		scoop = 1
	#SCoop close
	elif ind==1:
		scoop = 0
	rospy.sleep(.0625-(rospy.get_time()-now))
        armPub.publish(str(elbow)+','+str(shoulder)+','+str(base)+','+str(wrist)+','+str(scoop)+',')

def controller():
        rospy.init_node('xbox', anonymous = True)
        rospy.Subscriber('joy1', Joy, callback, queue_size=1)
        rospy.spin()

if __name__ == '__main__':
        controller()

