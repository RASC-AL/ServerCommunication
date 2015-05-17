import socket

LOCAL_IP = '127.0.0.1'
ROVER_IP = '127.0.0.1'
HOME_IP =  socket.gethostbyname('sblinux.eng.buffalo.edu')
# HOME_IP = '127.0.0.1'
#HOME_IP = '128.205.55.128'

COMM_FILE = '/tmp/ros_comm'

camList = [7,6,5,4]
