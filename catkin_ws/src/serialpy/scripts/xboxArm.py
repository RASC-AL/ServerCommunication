#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import Joy
from std_msgs.msg import String

armPub = rospy.Publisher('ARM',String, queue_size=10)

base = 50.0
elbow = 50.0
shoulder = 50.0
wrist = 50.0

base_min = 0.0
base_max = 100.0

elbow_min = 0.0
elbow_max = 100.0

shoulder_min = 0.0
shoulder_max = 100.0

wrist_min = 0.0
wrist_max = 100.0

scoop = 38.0
scoop_min = 0.0
scoop_max = 100.0

def callback(data):
        global base, base_min, base_max, elbow, elbow_min, elbow_max, shoulder, shoulder_min, shoulder_max, wrist, wrist_min, wrist_max, scoop, scoop_min, scoop_max
        now=rospy.get_time()
	ind = -1
        try:
                ind = data.buttons.index(1)
        except ValueError: pass
	#arm control
    	#Base Servo left
        if data.axes[2] < 0:
               	base += data.axes[2];
                base = base_min if base < base_min else base
        #Base Servo right
        elif data.axes[5] < 0:
                base -= data.axes[5];
                base = base_max if base > base_max else base
        #Elbow forward and back 
        if math.fabs(data.axes[1]) > .2:
                elbow += data.axes[1];
                if elbow > elbow_max:
        	      	elbow = elbow_max
                elif elbow < elbow_min:
              		elbow = elbow_min
	#Wrist up and down
	if ind==5 and math.fabs(data.axes[4]) > .2:
        	wrist += data.axes[4];
        	if wrist > wrist_max:
                	wrist = wrist_max
        	elif wrist < wrist_min:
                	wrist = wrist_min		
        #Shoulder forward and back
        elif math.fabs(data.axes[4]) > .2:
                shoulder += data.axes[4];
                if shoulder > shoulder_max:
                       	shoulder = shoulder_max
                elif shoulder < shoulder_min:          
              		shoulder = shoulder_min
	#Scoop open
	if ind==0:
		scoop+= 1.0
		scoop = scoop_max if scoop > scoop_max else scoop
	#Scoop close
	elif ind==1:
		scoop -= 1.0
		scoop = scoop_min if scoop < scoop_min else scoop 
	rospy.sleep(.125-(rospy.get_time()-now))
        armPub.publish(str(base)+','+str(elbow)+','+str(shoulder)+','+str(wrist)+','+str(scoop))

def controller():
        rospy.init_node('xbox', anonymous = True)
        rospy.Subscriber('joy', Joy, callback, queue_size=1)
        rospy.spin()

if __name__ == '__main__':
        controller()

