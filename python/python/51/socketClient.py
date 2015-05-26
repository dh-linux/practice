#!/usr/bin/env python
# -*- coding:utf-8 -*-
import socket,time

HOST='localhost'
PORT=9999
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect((HOST,PORT))
while 1:
    cmd = raw_input("Your command: ")#.strip()
    if len(cmd)==0:continue
    s.sendall(cmd)
    data=s.recv(1024)    
    print data
 #   time.sleep(0.5)
s.close
