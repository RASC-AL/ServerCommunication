#!/usr/bin/python
import subprocess
from subprocess import call

import socket
import sys
import argparse

TCP_PORT=5006
BUFFER_SIZE=1024

def setup_parser(parser) :
  parser.add_argument("-p", "--port", type=int, help="Server port number")

def parse_args(parser) :
  args = parser.parse_args()
  if args.port is not None:
    global TCP_PORT
    print 'Using port ' + str(args.port)
    TCP_PORT=args.port


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

if __name__ == "__main__":
  parser = argparse.ArgumentParser()
  setup_parser(parser)
  parse_args(parser)

  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  s.bind(("127.0.0.1", TCP_PORT))

  print 'Listening for incoming connections. . .'
  s.listen(1)

  conn, addr = s.accept()
  print 'Connection received'

  while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data:
      break
    temperature_str = tempsense()
    conn.send(temperature_str)
