#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket,os,SocketServer,commands

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        while 1:
            self.data = self.request.recv(1024).strip()
       	    print " {} wrote: ". format(self.client_address[0])
	    if not self.data:
		print "client %s is dead!" % self.client_address
		break
	    cmd_status, result = commands.getstatusoutput(self.data)
	    if len(result.strip()) !=0:
		self.request.sendall(result)
	    else:
		self.request.sendall('Done')

if __name__ == "__main__":
	HOST, PORT = "localhost", 9999
	server = SocketServer.ThreadingTCPServer((HOST, PORT), MyTCPHandler)
	server.serve_forever()

'''
HOST=''
PORT=50007
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((HOST,PORT))
s.listen(2)
while 1:
    conn,addr=s.accept()
    print 'Connectedd by', addr
    while 1:
        data=conn.recv(1024)
        if not data:break
        print 'data from:', addr, data
	cmd_result=os.popen(data).read()
        conn.sendall(cmd_result)
conn.close()
'''
