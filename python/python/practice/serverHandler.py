#!/usr/bin/env python
# -*- coding:utf-8 -*-
#

HOST, PORT = "", 9999
#import SocketServer
from SocketServer import BaseRequestHandler, StreamRequestHandler, TCPServer

class MyTCPHandler(StreamRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print "{} wrote:" . str(self.client_address[0])
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":

    # Create the server, binding to localhost on port 9999
    server = TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
