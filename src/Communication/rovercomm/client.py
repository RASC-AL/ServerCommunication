#!/usr/bin/env python
import socket
import sys
import rospy

#communication: holder class for socket, contains the socket and the receive function
class client:

    MSGLEN = 128

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def receive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < self.MSGLEN:
            chunk = self.sock.recv(min(self.MSGLEN - bytes_recd, self.MSGLEN))
            if chunk == '':
                raise RuntimeError("socket connection broken")
	    rospy.logerr('chunk : ' + chunk)
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
            if '\n' in chunk:
                #assert chunk[-1] == '\n'
                break
	retval = ''.join(chunks)
	#ret = retval.split('\n')
	#assert retval.count('\n') == 1
	#rospy.logerr(ret[0])
	#return ret[0]
	return retval
