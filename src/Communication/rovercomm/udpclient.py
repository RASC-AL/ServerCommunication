#!/usr/bin/env python
import socket
import sys
import rospy
import imp
from std_msgs.msg import String
from common import *

#communication: holder class for socket, contains the socket and the receive function
class udpclient:
    def __init__(self, port):
        self.config_pub = rospy.Publisher('HomeCommand', String, queue_size = 10) 
        rospy.init_node('Server')
        self.port = port
        ipGetter = imp.load_source('ipGetter', '/home/sbrover/Rover2015/src/ipGetter.py')
        self.homeIP = ipGetter.getHomeIP()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        #Handshake
        flag = False
        while not flag:
            self.sock.sendto("Start", (self.homeIP, 9998))
            self.sock.settimeout(1)
            try:
                self.sock.recvfrom(64)
                flag = True
            except socket.timeout:
                rospy.logerr("Waiting for response from server")

    def start(self):
        while(True):
            self.receive()

    def receive(self):
        chunk, addr = self.sock.recvfrom(64)
        s = str(chunk)
        s = s.strip()
        rospy.logerr(s)
        if s is None:
            rospy.logerr('message was None')
            return
        self.config_pub.publish(s)
