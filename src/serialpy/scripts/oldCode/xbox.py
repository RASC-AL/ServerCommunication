#!/usr/bin/env python
import rospy
from sensor_msgs.msg import Joy
from std_msgs.msg import String

move = False

drvPub = rospy.Publisher('DRV',String, queue_size=10)
armPub = rospy.Publisher('ARM',String, queue_size=10)
rlyPub = rospy.Publisher('RLY',String, queue_size=10)

speed = 20
turn_speed = 20
base = 144
shoulder = 90
elbow = 30
wrist = 30
scoop = 38

base_min = 75
base_max = 149

shoulder_min = 90
shoulder_max = 150

elbow_min = 30
elbow_max = 180

yaw_min = 5
yaw_max = 175
counter = 0
relay_0 = False
relay_1 = False

def callback(data):
	global speed, move, base, shoulder, wrist, elbow, scoop, base_min, base_max, shoulder_min, shoulder_max, elbow_min, elbow_max, yaw_min, yaw_max, counter, relay_0, relay_1
	ind = -1
	axes = data.axes[0:2]+data.axes[3:5]
	try:
		ind = data.buttons.index(1)
	except ValueError: pass
	turn_speed = 60
	if speed < 60:
		turn_speed = speed
	if ind == 14:
		drvPub.publish(str(-speed)+','+str(-speed))
	elif ind == 13:
		drvPub.publish(str(speed)+','+str(speed))
	elif ind == 12:
		drvPub.publish(str(turn_speed)+',' + str(-turn_speed))
	elif ind == 11:
		drvPub.publish(str(-turn_speed) + ','+str(turn_speed))

	if ind < 15 and ind > 10:
		move = True
	elif move:
		drvPub.publish('0,0')
		move = False
	if ind == 5 and speed < 110:
		speed = speed + 10
	elif ind == 4 and speed > 10:
		speed = speed - 10
	if ind == 2:
		relay_0 = not relay_0
		rlyPub.publish(('1' if relay_0 else '0')+','+ ('1' if relay_1 else '0'))
	if ind == 3:
		relay_1 = not relay_1
		rlyPub.publish(('1' if relay_0 else '0')+','+ ('1' if relay_1 else '0'))
	axis = filter(lambda x:abs(x) > 0.5, axes)
	if len(axis) > 0  or ind == 0:
		counter = (counter + 1)%20
		change = False
		if ind == 0:
			if scoop == 70:
				scoop = 38
				change = True
			else:
				scoop = 70
				change = True

		if counter == 0:
			if axes[0] > 0.2 and base < base_max:
				base += int(axes[0]/0.2)
				base = base_max if base > base_max else base
			if axes[0] < -0.2 and base > base_min:
				base += int(axes[0]/0.2)
				base = base_min if base < base_min else base
			if axes[1] > 0.2 and shoulder < shoulder_max:
				shoulder += int(axes[1]/0.2)
				shoulder = shoulder_max if shoulder > shoulder_max else shoulder
			if axes[1] < -0.2 and shoulder > shoulder_min:
				shoulder += int(axes[1]/0.2)
				shoulder = shoulder_min if shoulder < shoulder_min else shoulder
			if axes[3] > 0.2 and elbow < elbow_max:
				elbow += int(axes[3]/0.2)*2
				elbow = elbow_max if elbow > elbow_max else elbow
			if axes[3] < -0.2 and elbow > elbow_min:
				elbow += int(axes[3]/0.2)*2
				elbow = elbow_min if elbow < elbow_min else elbow
			if axes[2] > 0.2 and wrist < yaw_max:
				wrist += int(axes[2]/0.2)*2
				wrist = yaw_max if wrist > yaw_max else wrist
			if axes[2] < -0.2 and wrist > yaw_min:
				wrist += int(axes[2]/0.2)*2
				wrist = yaw_min if wrist < yaw_min else wrist
			change = True
		if change:
			change = False
			armPub.publish(str(base)+','+str(shoulder)+','+str(elbow)+','+str(wrist)+','+str(scoop))

def controller():
	rospy.init_node('xbox', anonymous = True)
	rospy.Subscriber('joy', Joy, callback)
	rospy.spin()

if __name__ == '__main__':
	controller()
