#!/usr/bin/env python
import subprocess
from subprocess import call
import time
import rospy
from std_msgs.msg import String

temp_pub = rospy.Publisher('ReturnData', String, queue_size = 10)

# Parses output from 'sensors' into a list of strings and returns this list
# Each list item represents all the output for a particular component
def tempsense():
	# Make a process call to 'sensors'
	# Redirect output to PIPEs
  	p = subprocess.Popen('/usr/bin/sensors -A', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

	# Now that we have the output in the pipe, we iterate over it
	# and append these lines to our output
  	output = ""
  	for line in p.stdout.readlines():
    		output += line
  	retval = p.wait()

	# Verbose/Debug printing
	#  for val in final_output:
	#    print val + '\n'
  	return output

def parseTemp(temp):
  	index1 = temp.find("CPUTIN: ")
  	index2 = temp.find("  (high = +")
  	return temp[index1:index2]

def tempnode():
  	rospy.init_node("tempnode")
	rate = rospy.Rate(4)
  	while not rospy.is_shutdown():
                temperature_str = tempsense()
    		temperature_str = parseTemp(temperature_str)
                temperature_str += time.strftime(" %H:%M:%S")
                temperature_str = 'T' + temperature_str
    		temp_pub.publish(temperature_str)
		rate.sleep()

if __name__ == "__main__":
	try:
		tempnode()
	except rospy.ROSInterruptException, e:
		pass
               
