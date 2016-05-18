#!/usr/bin/env python
import rospy
import math
from sensor_msgs.msg import Joy
from std_msgs.msg import String

drvPub = rospy.Publisher('DRV',String, queue_size=1)

left_speed = 0
right_speed = 0

speed_mod = 1.0
actuatorTracker = [0, 0, 0, 0, 0]
count = 0

def callback(data):
    global left_speed, right_speed, speed_mod, actuatorTracker, count
    now = rospy.get_time()
    actuatorType = actuatorTracker[-1]
    count = 0
    changed = False
    try:
        if data.buttons[6] == 1:
            actuatorTracker[-1] = 1
            changed = True
        elif data.buttons[7] == 1:
            actuatorTracker[-1] = 0
            changed = True
        for i in range(11, 15):
            pressed = data.buttons[i]
            ind = i - 11
            if i == 12:
                ind = 3
            elif i == 14:
                ind = 1
            actuatorTracker[ind] = pressed
            count += pressed * actuatorTracker[-1]
            
    except ValueError: pass
   
    if(count > 0 or changed):
        movVal = data.axes[4] * 254 if math.fabs(data.axes[4]) > .2 else 0
        actStr = 'A' + ','.join(str(x) for x in actuatorTracker) + ',' + \
                 str(int(movVal))
        drvPub.publish(actStr)
    else:
	try:
	    ind = data.buttons.index(1)
	except ValueError: pass
	#Drive control
	#Set speed modification
	if data.axes[5] < -.5:
	    speed_mod = 1.0
	else:
	    speed_mod = 2.0
	#Right wheel speed
	if math.fabs(data.axes[4]) > .2:
	    right_speed = data.axes[4]/speed_mod*127+127
	else:
	    right_speed = 127
	#Left wheel speed
	if math.fabs(data.axes[1]) > .2:
	    left_speed = data.axes[1]/speed_mod*127+127
	else:
	    left_speed = 127
	rospy.sleep(.0625-(rospy.get_time()-now))
	drvPub.publish(str(int(right_speed))+','+str(int(left_speed)))

def controller():
	rospy.init_node('xboxDrv', anonymous = True)
	rospy.Subscriber('joy2', Joy, callback, queue_size=1)
        rospy.spin()

if __name__ == '__main__':
	controller()
