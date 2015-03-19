import socket
import sys
import sockmessage
import cPickle as pickle

class client:

    MSGLEN = 4096

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        serialized_msg = pickle.dumps(msg, -1)
        sent = self.sock.send(serialized_msg)

    def receive(self):
        recieved_msg = self.sock.recv(2048)
        msg = pickle.loads(recieved_msg)
        return msg
