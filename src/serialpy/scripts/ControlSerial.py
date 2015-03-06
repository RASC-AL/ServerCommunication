#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import serial

Command = ""

def callbackArm(data):
  global Command
  if Command == "":
    Command = 'l'+str(data)

def callbackDrv(data):
  global Command
  if Command != "":
    Command += str(data)
    #Write to serial
    print Command #TODO: Test using publisher
    Command = ""  
  
def controller():
  rospy.init_node("ControlSerial")
  rospy.Subscriber('ARM', String, callbackArm)
  rospy.Subscriber('DRV', String, callbackDrv)
  rospy.spin();

if __name__ == '__main__':
  controller()
