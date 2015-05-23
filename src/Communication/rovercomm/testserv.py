#!/usr/bin/env python
import sys
import server

#communication: node running the server
port = 9999
serv = server.server(port)
serv.start()