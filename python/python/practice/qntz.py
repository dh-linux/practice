#!/usr/bin/env python
# -*- encoding:utf-8 -*-

'''
	 青年图摘图片抓取
1.给定一个初始URL
2.获取当天日期，创建/Users/MR_qiaoke/qntz/$date 目录，将当天的图片存到目录中
3.获取前一天的URL，继续抓取
4.依赖第三方库requests
'''

import requests 
import urllib,urllib2
import re
import os

qntz_picdir = r'/Users/MR_qiaoke/spider/qntz/'

def spider(url,day):
#获取URL的数字，供后面循环使用
    url_num = int(re.search('\d+',url).group())
    url_list = re.split(r'\d+', url)
    day = int(day)
    while 0 < day:
        html = requests.get(url)
        if html.status_code == 200:
#抓取图片URL
            pic_list = re.findall(r'data-lazy-src="(.*\.jpg|.*\.gif)".*<noscript>', html.text) 
#获取日期
            date_utf8 = re.findall(r'<title>.*</title>', html.text)[0].encode("UTF-8")
            date = re.search(r'\d+', date_utf8).group()
#创建目录, 并下载图片
            dir = qntz_picdir + date + "/"
            if not os.path.isdir(dir):
                os.mkdir(dir)
            for pic_url in pic_list:
                try:
                    pic_name = re.split(r'/', pic_url)[-1]
                    pic = urllib2.urlopen(pic_url).read()
                    with open(dir + pic_name, "wb+") as f:
                        f.write(pic)
                except Exception:
                    continue
            day -= 1
        url_num -= 1
        url =  url_list[0] + str(url_num) + url_list[1]

if __name__ == '__main__':
    url = raw_input("请输入初始URL: ")
    day = raw_input("请输入抓取的天数(由后往前): ")
    print "已经开始抓取，请稍等..."
    spider(url,day)
    print "抓取完成."
