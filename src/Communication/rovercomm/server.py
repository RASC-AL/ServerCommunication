#!/usr/bin/env python
import socket
import select
import os
import sys
import client
import rospy
from std_msgs.msg import String

from common import *

#communication: server code. This class holds a client object which is set to None, when we have a connection established to the base  
#the client holds the socket. This socket is only used for recieving data from the base. The socket meant for sending data is present 
#in returnData.py in serial package. This is because the server and the returnData are running as separate nodes.
class server:
	def __init__(self, port):
		# TODO publisher, change message type
		self.config_pub = rospy.Publisher('HomeCommand', String, queue_size = 10)
		rospy.init_node('Server')
		#rate = rospy.Rate(10)

		self.client = client.client()
		self.connections = []
		self.port = port
		#TODO check ip
		hostname = "0.0.0.0" #"128.205.54.5"
		self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.serv.bind((hostname, int(port)))
		self.serv.listen(10)
		self.connections.append(self.serv)

	def start(self):
		while True:
			try:
				readsock, writesock, errsock = select.select(self.connections, [], [])
				for sock in readsock:
					if sock == self.serv:
						(clientsocket, address) = self.serv.accept()
						self.client = client.client(clientsocket)
						self.connections.append(self.client.sock)
						self.addr = address
						self.receive()
					else:
						self.receive()
			except Exception, e:
				rospy.logerr(e)
				#TODO check this
				self.connections.remove(self.client.sock)
				self.client = None

	def send(self, data, host, port):
		self.client = client.client()
		self.client.connect(host, port)
		self.client.send(data)

	#communication: this method receives data from the base and then publishes it over a topic where 
	#the data is parsed and operated on
	def receive(self):
		if self.client is None:
			rospy.logerr('client connection not established')
			return
 		s = self.client.receive()
		if s is None:
			rospy.logerr('message was None')
			return
		rospy.loginfo('message recieved : ' + s)
		self.config_pub.publish(s)
		#print self.client.receive()
		#sys.stdout.flush()

	def ping(self, hostname):
		if self.client is None or self.addr is None:
			print "No client registered"
			return
		response = os.system("ping -c 1 " + addr)
		if response == 0:
		    return True
		else:
		    return False
