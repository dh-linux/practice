#!/usr/bin/python
#comment
#write for count log by denghao@20140331


import time

def timeo(fun,n=1):
    start = time.clock()
    for i in range(n): fun()
    stend = time.clock()
    thetime = stend-start
    return fun.__name__, thetime

import  os
import  datetime
import  re
#import  threading
#import thread

today = datetime.date.today()
time_yesterday = today + datetime.timedelta(days = -1)
time_yesterday = time_yesterday.strftime("%Y-%m-%d")
time_hour = range(len(('1'*24)))

def count_ls_wapcms():
    for i in time_hour:
        if i < 10 :
            log_hour = "/data1/sinawap/scribe_data/wap/sinawap_dpool_access_http/sinawap_dpool_access_http-" + time_yesterday + "_0000" + `i`
        else :
            log_hour = "/data1/sinawap/scribe_data/wap/sinawap_dpool_access_http/sinawap_dpool_access_http-" + time_yesterday + "_000" + `i`
        langshou = 0
        wap = 0
#        fd_cms = open("ceshi.txt")
        fd_cms = open(log_hour)
        fd_langshou_ip = open("/data1/tmp/count_log_ip/langshou_ip.txt",'w')
        fd_cms_ip = open("/data1/tmp/count_log_ip/cms_ip.txt",'w')
        fd_cms_file = fd_cms.readlines(512000000)
        while fd_cms_file:
            for line in fd_cms_file:
                try:
                    wap += 1     
                    array = line.strip().split('`')
                    rule_1 = re.search(r'\/3g\/',array[2])
                    rule_2 = re.search(r'^3g.sina.com.cn|^sina.cn',array[12])
                    if  rule_1==None and rule_2!=None:
                        langshou += 1
                        fd_langshou_ip.write(ip.group(3) + "\n" )
                    ip = re.search(r'((\[)(\d+.\d+.\d+.\d+)(\]))',line)
                    fd_cms_ip.write(ip.group(3) + "\n" )
                except:
                    pass
            fd_cms_file = fd_cms.readlines(512000000)
        print `i` + "log's lines: " + `wap`
        print `i` + "langshou lines : " + `langshou`
        wapcms = wap - langshou
        print `i` + "wapcms 's lines: " + `wapcms`
        fd_cms.close()
        fd_langshou_ip.close()
        fd_cms_ip.close()


def count_dpool():
     for i in time_hour:
        if i < 10 :
            log_hour = "/data1/sinawap/scribe_data/wap/sinawap_dpool_access_http/sinawap_dpool_access_http-" + time_yesterday + "_0000" + `i`
        else :
            log_hour = "/data1/sinawap/scribe_data/wap/sinawap_dpool_access_http/sinawap_dpool_access_http-" + time_yesterday + "_000" + `i`
        dpool = 0
        fd_dpool = open(log_hour)
        fd_dpool_ip = open("/data1/tmp/count_log_ip/dpool_ip.txt",'w')
        fd_dpool_file = fd_dpool.readlines(512000000)
        while fd_dpool_file:
            for line in fd_dpool_file:
                try:
                    dpool += 1
                    ip = re.search(r'((\[)(\d+.\d+.\d+.\d+)(\]))',line)
                    fd_dpool_ip.write(ip.group(3) + "\n" )
                except:
                    pass
            fd_dpool_file = fd_dpool.readlines(512000000)
        print "dpool 's lines: " + `dpool`
        fd_dpool.close()
        fd_dpool_ip.close() 



if __name__=="__main__":
    count_ls_wapcms()

