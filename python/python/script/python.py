#/usr/bin/env python
# -*- coding: utf-8 -*-
import time
'''print 'hello'
sum = 0
for x in range(101):
    sum = sum + x

d={'a': 1, 'b': 2, 'c': 3}
for key in d:
	print key
for k,v in d.iteritems():
	print k,v    

class Test(object):
	def ec(self):
		print 'it is ok'

def ech(test):
	test.ec()

ech(Test())

import os 
print os.uname()

a=[x for x in os.listdir('.') if os.path.isdir(x)]
print a'''

status = False
while True:
	try:
		print 1
		time.sleep(1)
	except KeybordInterrupt:
		print ye
