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
        self.x = 0.3
        self.y = 0.3
        self.z = 0.0

        self.coord_mod = 50

        self.scoop = 1
        self.flag = 0
        self.dropNow = 0
        self.homeNow = 0

        self.instructionsPerSecond = 16.0

    def callback(self, data):
        now = rospy.get_time()
	ind = -1
	tempX = self.x
	tempY = self.y
	tempZ = self.z
        
        try:
            ind = data.buttons.index(1)
        except ValueError: pass
	#Arm control
        #Change x position
        if math.fabs(data.axes[0]) > .2:
            tempX = self.x - data.axes[0] / self.coord_mod

    	#Change y position
        if math.fabs(data.axes[1]) > .2:
            tempY = self.y + data.axes[1] / self.coord_mod
               
        #Change z position (Need to verify index)
        if math.fabs(data.axes[4]) > .2:
            tempZ = self.z + data.axes[4] / self.coord_mod
        
        #TODO  
        wrist = 1500.0
  
        #Scoop open
	if ind==0:
            self.scoop = 1
	#Scoop close
	elif ind==1:
	    self.scoop = 0
        #Drop position (X)
        ''' 
        elif ind==2 and flag==0:
            x = 0
            y = 0
            z = 0
            dropNow = time.time()
        #Home position (Y)
        elif ind==3 and flag == 0:
            flag = 3
            pass
        '''
 
        jointValues = self.getJoints(tempX, tempY, tempZ)

	rospy.sleep((1 / self.instructionsPerSecond)-(rospy.get_time()-now))
        if(jointValues):
            self.armPub.publish('l'+str(int(jointValues[2]))+','+str(int(jointValues[1]))+','+str(int(jointValues[0]))+','+str(int(wrist))+','+str(int(self.scoop))+',')
            self.testPub.publish('X: ' + str(self.x) + ' Y: ' + str(self.y) + ' Z: ' + str(self.z))
        #else:
        #    self.testPub.publish("Can't Reach")
        '''
        if flag==2 and time.time() - dropNow > 10:
            base = 1724.0
            flag = 0
        elif ind==3:
            pass
        '''

    def getJoints(self, x, y, z):
        link1 = 11.5 * .0254 # First link length in meters
        link2 = 12.5 * .0254 # Second link length in meters
         
        #Try block will prevent arm taking on any unreachable values
        try:
            #To find the angle of the base
            base_angle = math.atan2(y, x)

            #To find the angle of the elbow
            #Parameters
            k = 2 * z * link2
            l = 2 * x * link2 / math.cos(base_angle)
            m = link1 * link1 - z * z - link2 * link2 - x * x / (math.cos(base_angle) * math.cos(base_angle));
            
            elbow_angle = 2 * math.atan2(-k + math.sqrt(k * k - m * m + l * l), m - l);

            #To find the angle of the shoulder
            shoulder_angle = math.atan2(z - link2 * math.sin(elbow_angle), x / math.cos(base_angle) - link2 * math.cos(elbow_angle));

            #Convert the angles from radians to degree
            base_angle = base_angle*180/math.pi;
            shoulder_angle = shoulder_angle*180/math.pi;
            elbow_angle = 360-elbow_angle*180/math.pi;

            #self.testPub.publish(str(base_angle) + ' ' + str(shoulder_angle) + ' ' + str(elbow_angle))

            #TODO Need to verify values of angles at limits
            if(base_angle < 0 or base_angle > 180 or shoulder_angle < 0 or shoulder_angle > 90 or elbow_angle < 28.5 or elbow_angle > 114.8):       
                raise ValueError

            self.x = x
            self.y = y 
            self.z = z

            #Convert angles to values of what is written to servos and actuators
            base = 1100 + 800 * (base_angle) / 180
            shoulder = 1000 + 650 * (90 - shoulder_angle) / 90
            elbow = 1000 + 1000 * (114.8 - elbow_angle) / 86.3

            return (base, shoulder, elbow) 

        except ValueError:
            self.testPub.publish(str(base_angle) + ' ' + str(shoulder_angle) + ' ' + str(elbow_angle))
            return ()
        
 
def controller():
    rospy.init_node('xboxArmNew', anonymous = True)
    armController = ArmController()
    rospy.Subscriber('joy1', Joy, armController.callback, queue_size=1)
    rospy.spin()

if __name__ == '__main__':
    controller()

