import socket
import sys

from common import *

#communication: holder class for socket, contains the socket and the receive function
class client:

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        totalsent = 0
		msg = pad(msg)
        while totalsent < len(msg):
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def receive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(self.MSGLEN - bytes_recd, MSGLEN))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
		retval = ''.join(chunks)
		assert len(retval) == MSGLEN, 'Received message length did not match MSGLEN! %d != %d' % (len(retval), MSGLEN)
		return retval

