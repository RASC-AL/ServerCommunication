#!/usr/bin/env python
import rospy
import math
import time
from sensor_msgs.msg import Joy
from std_msgs.msg import String

armPub = rospy.Publisher('ARM', String, queue_size = 1)
drvPub = rospy.Publisher('DRV', String, queue_size = 1)

base = 1500.0
elbow = 1100.0
shoulder = 1100.0
wrist = 1500.0

base_mod = 4
elbow_mod = 17
shoulder_mod = 30
wrist_mod = 4

base_min = 1100.0
base_max = 1900.0

elbow_min = 1000.0
elbow_max = 2000.0

shoulder_min = 1000.0
shoulder_max = 2000.0

wrist_min = 600.0
wrist_max = 2100.0

scoop = 0

flag = 0

dropNow = 0
homeNow = 0

def callback(data):
        global base, base_min, base_max, elbow, elbow_min, elbow_max, shoulder, shoulder_min, shoulder_max, wrist, wrist_min, wrist_max, scoop, flag, dropNow, homeNow
        now=rospy.get_time()
	ind = -1
        try:
                ind = data.buttons.index(1)
        except ValueError: pass
	#arm control
    	#Base Servo left
        if data.axes[2] < 0:
               	base -= data.axes[2]/base_mod * 80;
                base = base_max if base > base_max else base
        #Base Servo right
        elif data.axes[5] < 0:
                base += data.axes[5]/base_mod * 80;
                base = base_min if base < base_min else base
                #Shoulder forward and back
        if math.fabs(data.axes[1]) > .2:
                shoulder += data.axes[1]/shoulder_mod * 100;
                if shoulder > shoulder_max:
                        shoulder = shoulder_max
                elif shoulder < shoulder_min:
                        shoulder = shoulder_min
	
        #Wrist up and down
	if ind==5 and math.fabs(data.axes[4]) > .2:
        	wrist += data.axes[4]/wrist_mod * 180;
        	if wrist > wrist_max:
                	wrist = wrist_max
        	elif wrist < wrist_min:
                	wrist = wrist_min		
	 
        #Elbow forward and back 
        elif math.fabs(data.axes[4]) > .2:
                elbow += data.axes[4]/elbow_mod * 100;
                if elbow > elbow_max:
                        elbow = elbow_max
                elif elbow < elbow_min:
                        elbow = elbow_min

        #Scoop open
	if ind==0:
		scoop = 1
	#Scoop close
	elif ind==1:
		scoop = 0
        #Drop position (X)
        elif ind==2 and flag==0:
            elbow = 1194.0
            shoulder = 1000.0
            flag = 2
            dropNow = time.time()
        #Home position (Y)
        elif ind==3 and flag == 0:
            flag = 3
            pass
        elif ind==4:  
            drvPub.publish('STOP')
        elif ind==13:
            drvPub.publish('GO')

	rospy.sleep(.0625-(rospy.get_time()-now))
        armPub.publish('l'+str(int(elbow))+','+str(int(shoulder))+','+str(int(base))+','+str(int(wrist))+','+str(int(scoop))+',')

        if flag==2 and time.time() - dropNow > 10:
            base = 1724.0
            flag = 0
        elif ind==3:
            pass
   
def controller():
        rospy.init_node('xboxArm', anonymous = True)
        rospy.Subscriber('joy1', Joy, callback, queue_size=1)
        rospy.spin()

if __name__ == '__main__':
        controller()

