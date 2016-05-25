#!/usr/bin/env python
import sys
import udpclient

#communication: node running the server
port = 9999
client = udpclient.udpclient(port)
client.start()
