#!/usr/bin/env python
import socket
import select
import os
import sys
import client
import sockmessage
import rospy
from std_msgs.msg import String

class server:

	def __init__(self, port):
		# TODO publisher, change message type
		self.config_pub = rospy.Publisher('config', String, queue_size = 10)
		self.arm_pub = rospy.Publisher('ARM', String, queue_size = 10)
		rospy.init_node('Server')
		#rate = rospy.Rate(10)

		self.client = client.client()
		self.connections = []
		self.port = port
		#TODO check ip
		hostname = "128.205.54.5"
		self.serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		#self.serv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR)
		self.serv.bind((hostname, int(port)))
		self.serv.listen(10)
		self.connections.append(self.serv)
		self.connections.append(sys.stdin)

	def start(self):
		while True:
			readsock, writesock, errsock = select.select(self.connections, [], [])
			for sock in readsock:
				if sock == self.serv:
					(clientsocket, address) = self.serv.accept()
					self.client = client.client(clientsocket)
					self.addr = address
					self.receive()
				elif sock == sys.stdin:
					# TODO check this
					port = 9999
					sstr = sys.stdin.readline()
					msg = sstr
					self.send(msg, "128.205.54.9", port)
				else:
					self.receive()

	def send(self, data, host, port):
		self.client = client.client()
		self.client.connect(host, port)
		self.client.send(data)

	def receive(self):
		print self.client.receive()
		sys.stdout.flush()

	def ping(self, hostname):
		if self.client is None or self.addr is None:
			print "No client registered"
			return
		response = os.system("ping -c 1 " + addr)
		if response == 0:
		    return True
		else:
		    return False
