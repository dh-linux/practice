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
        print "�Ҳ���dpool_ip�ļ�,���Ҫ�·��ķ����б���Ϊdpool_ip�ļ����ŵ�/data1/server/Ŀ¼...\n"
        sys.exit()
    return ip_list

def check_app_name(app):
    app_list = "svn list https://svn1.intra.sina.com.cn/wapcms/newwap/app/"
    app_list = os.popen(app_list).readlines()
    rule = re.compile(r'^\w+')
    for i in range(0,len(app_list)):
        app_list[i] = rule.match(app_list[i]).group()
    if app not in app_list:
        print "ҵ�������������˶Ժ����·�..."
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
    print "����������ȡ..."
    rm = "rm -rf " + app_path
    app_svn = "svn export https://svn1.intra.sina.com.cn/wapcms/newwap/app/" + app + " " + app_path + " --force > /dev/null 2>&1"
    print app_svn
    os.system(rm)
    os.system(app_svn)
    chown = "chown -R root.root " + app_path
    os.system(chown)
    print "������ȡ���...\n"

def issue():
    print "����ҵ��: "
    ls = "ls " + path
    output = os.popen(ls).readlines()
    for name in output:
        print name.strip() 
    app = raw_input("������Ҫ�·���ҵ��(������ҵ��): ")
    checkout(app)
    print "���뿪ʼ�·�..."
    for ip in ip_list:
        print ip + "..."
        try:
            rsync = 'rsync -avz --delete --exclude "sinasrv_config" --exclude "*.svn" --port=8875 --timeout=15 --contimeout=10 ' + path + app + '/trunk/ ' + ip + '::newwap/' + app + ' > /dev/null 2>&1'
            os.system(rsync)
        except Exception,e:
            print " ���ӳ�ʱ... " + ip + " ����������ȷ����÷�����������״̬...\n"
    print "�����·����...\n"

def frame_issue():
    print "��ܴ��뿪ʼ��ȡ..."
    be_path = path + "framework"
    if not os.path.isdir(be_path):
        print "mkdir be_path: " + be_path
        os.makedirs(be_path)
    be_svn = "svn export https://svn1.intra.sina.com.cn/wapcms/newwap/framework/ " + be_path + " --force > /dev/null 2>&1"
    os.system(be_svn)
    print "��ܴ�����ȡ���...\n"
    print "��ܴ��뿪ʼ�·�..."
    for ip in ip_list:
        print ip + "..."
        rsync = 'rsync -avz --delete --exclude "sinasrv_config" --exclude "*.svn" --port=8875 --timeout=15 --contimeout=10 ' + path + 'framework/trunk/ ' + ip + '::newwap/be > /dev/null 2>&1'
        os.system(rsync)
    print "��ܴ����·����...\n"

def picsrc_issue(app):
    ip_list = ('10.13.1.112','172.16.174.81')
    checkout(app)
    print "picsrc�����������..."
    for ip in ip_list:
        print ip + "..."
        rsync = 'rsync -avz --delete --exclude "sinasrv_config" --exclude "*.svn" --port=8875 --timeout=15 --contimeout=10 ' + path + app + '/trunk/ ' + ip + '::newwap/' + app + ' > /dev/null 2>&1'
        os.system(rsync)
    print "picsrc�����·����..."    

def rollbak():
    print "�ѱ��ݵ�ҵ��: "
    bak_list = "ls " + bakpath
    bak_list = os.popen(bak_list).read()
    print bak_list
    app = raw_input("������Ҫ�ع���ҵ��(�ع�Ϊ���һ���·��Ĵ���): ")
    for ip in ip_list:
        print ip + "..."
        rsync = 'rsync -avz --delete --exclude "sinasrv_config" --exclude "*.svn" --port=8875 --timeout=15 --contimeout=10 ' + bakpath + app + '/ ' + ip + '::newwap/' + app + ' > /dev/null 2>&1'
        os.system(rsync)
    print "�ع����..."
    
if __name__ == '__main__':

    ip_list = check_ip_file()
    issueoption = {
        1:'app',
        2:'be���',
        3:'picsrc',
        4:'�·�ҵ����뵽�����(10.13.1.233)',
        5:'�·���ܴ��뵽�����(10.13.1.233)',
        6:'�����·������ԣ�',
        7:'�ع�(rollbak)',
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
            ip = raw_input("���뽫ֻ�·���һ̨������,���ֶ�����ip:  ")
            ip_list = []
            ip_list.append(ip)
            ch = raw_input('ҵ���������"1" or ��ܴ�������"2"��')
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
