#!/usr/bin/env python
#-*- coding:utf-8 -*-

#from time import sleep, ctime
import os

a = 1

try:
    pid = os.fork()
    if pid == 0:
        print "erz "
        source = source - 1
        sleep(10)
    else:
        print "bab"
    print source
except :
    pass

