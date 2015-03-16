#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import serial

Command = ""
now = 0
command_pub = rospy.Publisher('Command', String, queue_size=1)
ser = serial.Serial('/dev/ttyACM0', baudrate = 115200)

def callbackArm(data):
  global Command
  global now
  if Command == "":
    now = rospy.get_time()
    Command = str(data.data)

def callbackDrv(data):
  global Command
  global now
  if Command != "":
    Command += str(data.data)
    #Write to serial
    Command = Command.replace("data: ", "")
    rospy.sleep(.0625-(rospy.get_time()-now))
    command_pub.publish(Command) #TODO: Test using publisher
    ser.write(Command)
    ser.flush()
    Command = ""  
  
def controller():
  rospy.init_node("ControlSerial")
  rospy.Subscriber('ARM', String, callbackArm)
  rospy.Subscriber('DRV', String, callbackDrv)
  rospy.spin();

if __name__ == '__main__':
  rospy.sleep(5)
  controller()
