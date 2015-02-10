#!/usr/bin/env python

import socket
import argparse

TCP_IP = '127.0.0.1'
TCP_PORT=5006
BUFFER_SIZE=1024

def setup_parser(parser) :
  parser.add_argument("-p", "--port", type=int, help="Server port number")

def parse_args(parser) :
  args = parser.parse_args()
  if args.port is not None:
    print 'Using port ' + str(args.port)
    global TCP_PORT
    TCP_PORT=args.port




if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  setup_parser(parser)
  parse_args(parser)

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.connect((TCP_IP, TCP_PORT))
  while 1:
    message = raw_input()
    s.send(message)
    data = s.recv(BUFFER_SIZE)
    print data
