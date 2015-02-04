#/usr/bin/env python
# -*- coding:utf-8 -*-

import time,os
import urllib2,urllib,re,thread,time


req = urllib2.Request('http://requests-docs-cn.readthedocs.org/zh_CN/latest/')
response = urllib2.urlopen(req)
the_page = response.read()
myitem = re.findall('href="user/(.*).html">',the_page,re.S)
print myitem


#print the_page
'''
myitem = re.search('user/quickstart.html',the_page,re.S)
print myitem.group()
response = urllib2.urlopen('http://requests-docs-cn.readthedocs.org/zh_CN/latest/' + myitem.group())
page = response.read()
with open('/Users/MR_qiaoke/tmp/tmp.html','w') as f:
	f.write(page)
'''