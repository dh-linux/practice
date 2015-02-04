#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
script : rsync be code to the dpool
author : denghao1
C-Date : 2014-10-31
version : 1.0
M-Date : 2014-11-06
version : 1.1
change : add rollbak
'''

import os
import re
import sys

server = r'/data1/server/server'
path = r'/data1/server/be_code/'
bakpath = r'/data1/server/rollbak/'

def check_ip_file():
    if os.path.exists(server):
        print "ok,ip list is exists...\n"
        ip_list=[]
        with open(server,'r') as f:
            for ip in f.readlines():
                ip = re.match(r'^\d+.\d+.\d+.\d+',ip)
                if ip:
                    ip_list.append(ip.group()) 
    else:
        print "找不到dpool_ip文件,请把要下发的服务列表保存为dpool_ip文件，放到/data1/server/目录...\n"
        sys.exit()
    return ip_list

def check_app_name(app):
    app_list = "svn list https://svn1.intra.sina.com.cn/wapcms/newwap/app/"
    app_list = os.popen(app_list).readlines()
    rule = re.compile(r'^\w+')
    for i in range(0,len(app_list)):
        app_list[i] = rule.match(app_list[i]).group()
    if app not in app_list:
        print "业务名输入错误，请核对后再下发..."
        sys.exit()

def code_bak(app):
    app_path = path + app
    app_bakpath = bakpath + app
    if not os.path.isdir(app_bakpath):
        print "mkdir app_bakpath: " + app_bakpath
        os.makedirs(app_bakpath)
    rm = "rm -rf " + app_bakpath
    cp = "cp -r " + app_path + "/trunk " + app_bakpath
    os.system(rm)
    os.system(cp) 

def checkout(app):
    print "app is " + app + "\n"
    check_app_name(app)
    code_bak(app)
    app_path = path + app
    app_sys_path = app_path + "/sys"
    if not os.path.isdir(app_path):
        print "mkdir app_path: " + app_path
        os.makedirs(app_path)
        os.makedirs(app_sys_path)
    print "代码正在拉取..."
    rm = "rm -rf " + app_path
    app_svn = "svn export https://svn1.intra.sina.com.cn/wapcms/newwap/app/" + app + " " + app_path + " --force > /dev/null 2>&1"
    print app_svn
    os.system(rm)
    os.system(app_svn)
    chown = "chown -R root.root " + app_path
    os.system(chown)
    print "代码拉取完成...\n"

def issue():
    print "已有业务: "
    ls = "ls " + path
    output = os.popen(ls).readlines()
    for name in output:
        print name.strip() 
    app = raw_input("请输入要下发的业务(或者新业务): ")
    checkout(app)
    print "代码开始下发..."
    for ip in ip_list:
        print ip + "..."
        try:
            rsync = 'rsync -avz --delete --exclude "sinasrv_config" --exclude "*.svn" --port=8875 --timeout=15 --contimeout=10 ' + path + app + '/trunk/ ' + ip + '::newwap/' + app + ' > /dev/null 2>&1'
            os.system(rsync)
        except Exception,e:
            print " 连接超时... " + ip + " 已跳过，请确认与该服务器的连接状态...\n"
    print "代码下发完成...\n"

def frame_issue():
    print "框架代码开始拉取..."
    be_path = path + "framework"
    if not os.path.isdir(be_path):
        print "mkdir be_path: " + be_path
        os.makedirs(be_path)
    be_svn = "svn export https://svn1.intra.sina.com.cn/wapcms/newwap/framework/ " + be_path + " --force > /dev/null 2>&1"
    os.system(be_svn)
    print "框架代码拉取完成...\n"
    print "框架代码开始下发..."
    for ip in ip_list:
        print ip + "..."
        rsync = 'rsync -avz --delete --exclude "sinasrv_config" --exclude "*.svn" --port=8875 --timeout=15 --contimeout=10 ' + path + 'framework/trunk/ ' + ip + '::newwap/be > /dev/null 2>&1'
        os.system(rsync)
    print "框架代码下发完成...\n"

def picsrc_issue(app):
    ip_list = ('10.13.1.112','172.16.174.81')
    checkout(app)
    print "picsrc代码下拉完成..."
    for ip in ip_list:
        print ip + "..."
        rsync = 'rsync -avz --delete --exclude "sinasrv_config" --exclude "*.svn" --port=8875 --timeout=15 --contimeout=10 ' + path + app + '/trunk/ ' + ip + '::newwap/' + app + ' > /dev/null 2>&1'
        os.system(rsync)
    print "picsrc代码下发完成..."    

def rollbak():
    print "已备份的业务: "
    bak_list = "ls " + bakpath
    bak_list = os.popen(bak_list).read()
    print bak_list
    app = raw_input("请输入要回滚的业务(回滚为最近一次下发的代码): ")
    for ip in ip_list:
        print ip + "..."
        rsync = 'rsync -avz --delete --exclude "sinasrv_config" --exclude "*.svn" --port=8875 --timeout=15 --contimeout=10 ' + bakpath + app + '/ ' + ip + '::newwap/' + app + ' > /dev/null 2>&1'
        os.system(rsync)
    print "回滚完成..."
    
if __name__ == '__main__':

    ip_list = check_ip_file()
    issueoption = {
        1:'app',
        2:'be框架',
        3:'picsrc',
        4:'下发业务代码到仿真机(10.13.1.233)',
        5:'下发框架代码到仿真机(10.13.1.233)',
        6:'单机下发（测试）',
        7:'回滚(rollbak)',
        8:'exit'
    }
    for k,v in issueoption.iteritems():
        print "%d: " % k, v
    flag = False
    while not flag:
        try:
            option = raw_input("please input your choice option: ")
            if option == 'q' or option == 'Q' or option == 'exit':
                sys.exit()
        except Exception,e:
            print "please input nubmer !"
        else:
            flag = True
    option = int(option)
    if option in issueoption:
        if option == 1: 
            issue()
        elif option == 2:
            frame_issue()
        elif option == 3:
            picsrc_issue(picsrc)
        elif option == 4:
            ip_list = ['10.13.1.233']
            issue()
        elif option == 5:
            ip_list = ['10.13.1.233']
            frame_issue()
        elif option == 6:
            ip = raw_input("代码将只下发到一台机器上,请手动输入ip:  ")
            ip_list = []
            ip_list.append(ip)
            ch = raw_input('业务代码输入"1" or 框架代码输入"2"：')
            if ch == "1":
                issue()
            elif ch == "2":
                frame_issue()
            else:
                print "err..."
        elif option == 7:
            rollbak()
        elif option == 8:
            sys.exit()
    else:
        print "exit... "

### END ###
