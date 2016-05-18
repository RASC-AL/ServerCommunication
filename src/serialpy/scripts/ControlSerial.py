#!/usr/bin/env python
import rospy
from std_msgs.msg import String
import serial

Command = ""
now = 0
driveAllowed = True
mode = '0'
switch = False
command_pub = rospy.Publisher('Command', String, queue_size=1)
ser = serial.Serial('/dev/ttyACM0', baudrate = 115200)

def callbackArm(data):
  global Command
  global now
  if Command == "":
      now = rospy.get_time()
      Command = str(data.data)

#This is not good code clean up
def callbackDrv(data):
  global Command, now, driveAllowed, switch, mode

  drvCommand = data.data

  if Command != "":
      if drvCommand[0] == 'A':
          rospy.logerr(drvCommand)
          strArr = drvCommand.split(',')
          mode = strArr[4]
          ser.write(drvCommand + "\n")
          Command = ""
          switch = True
          rospy.sleep(.0625-(rospy.get_time()-now))
      elif switch == True and mode == '1':
          switch = False
          Command = "A1,1,1,1,1,0"
          rospy.logerr(Command)
          ser.write(Command+ "\n") 
          Command = ""
      elif drvCommand == 'STOP' or (drvCommand != 'GO' and not driveAllowed):
          driveAllowed = False 
          Command += '127,127'
          Command = Command.replace("data: ", "")
          rospy.logerr(Command)
          ser.write(Command + "\n")
          Command = ""  
      elif driveAllowed == False and drvCommand == 'GO':
          driveAllowed = True
          Command = ""
      elif driveAllowed == True and drvCommand != 'GO':
          Command += str(drvCommand)
          #Write to serial
          Command = Command.replace("data: ", "")
          rospy.sleep(.0625-(rospy.get_time()-now))
          rospy.logerr(Command) 
          ser.write(Command + "\n")
          Command = ""  

def controller():
    rospy.init_node("ControlSerial")
    rospy.Subscriber('ARM', String, callbackArm)
    rospy.Subscriber('DRV', String, callbackDrv)
    rospy.spin();

if __name__ == '__main__':
    rospy.sleep(5)
    controller()
