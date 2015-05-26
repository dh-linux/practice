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
version : 1.2
change : issue check
M-Date : 2015-01-29
'''
# ¿¿¿¿¿ https://svn1.intra.sina.com.cn/wapcms/wap_remould_offline/api

import os
import re
import sys
import subprocess

server = r'/data1/server/server'
path = r'/data1/server/be_code/'
adminpath = r'/data1/server/admin/'
adminip = r'172.16.35.175'
bakpath = r'/data1/server/rollbak/'
langshou_ip = r'/data1/server/langshou_ip'

def check_ip_file(ip_file):
    if os.path.exists(ip_file):
        print "ok,ip list is exists...\n"
        ip_list=[]
        with open(ip_file,'r') as f:
            for ip in f.readlines():
                ip = re.match(r'^\d+.\d+.\d+.\d+',ip)
                if ip:
                    ip_list.append(ip.group())
    else:
        print "¿¿¿¿¿ip¿¿¿,¿¿¿¿¿¿¿¿¿¿¿¿¿/data1/server/¿¼¿¿...\n"
        sys.exit()
    return ip_list

def check_app_name(app):
    app_list = "svn list https://svn1.intra.sina.com.cn/wapcms/newwap/app/"
    app_list = os.popen(app_list).readlines()
    rule = re.compile(r'^\w+')
    for i in range(0,len(app_list)):
        app_list[i] = rule.match(app_list[i]).group()
    if app not in app_list:
        print "¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿¿·¿..."
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
    print "¿¿¿¿¿¿¿¿¿¿..."
    rm = "rm -rf " + app_path
    app_svn = "svn export https://svn1.intra.sina.com.cn/wapcms/newwap/app/" + app + " " + app_path + " --force > /dev/null 2>&1"
    print app_svn
    os.system(rm)
    os.system(app_svn)
    chown = "chown -R root.root " + app_path
    os.system(chown)
    print "¿¿¿¿¿¿¿¿¿...\n"

def issue():
    print "¿¿¿¿¿¿¿: "
    ls = "ls " + path
    output = os.popen(ls).readlines()
    for name in output:
        print name.strip()
    app = raw_input("¿¿¿¿¿¿¿¿·¿¿¿¿¿¿(¿¿¿¿¿¿¿¿¿): ")
    checkout(app)
    print "¿¿¿¿¿¿·¿,¿¿¿¿¿¿¿¿Crtl+c¿¿¿¿·¿..."
    for ip in ip_list:
        try:
            print ip + "..."
            rsync = 'rsync -avz --delete --exclude "sinasrv_config" --port=8875 --timeout=15 --contimeout=10 ' + path + app + '/trunk/ ' + ip + '::newwap/' + app
            mid = subprocess.Popen(rsync,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            status = mid.communicate()[1]
            if status != '':
                print " ¿¿¿¿¿... " + ip + " ¿¿¿¿¿¿¿¿¿¿¿¿÷¿¿¿¿¿rsync8875¿¿¿¿¿¿¿¿¿...\n"
        except KeyboardInterrupt:
            print "¿¿¿¿¿¿·¿¿¿¿¿¿¿¿¿...."
            sys.exit()
    print "¿¿¿¿¿·¿¿¿¿...\n"

def frame_issue():
    print "¿¿¿¿¿¿¿¿..."
    be_path = path + "framework"
    if not os.path.isdir(be_path):
        print "mkdir be_path: " + be_path
        os.makedirs(be_path)
    be_svn = "svn export https://svn1.intra.sina.com.cn/wapcms/newwap/framework/ " + be_path + " --force > /dev/null 2>&1"
    os.system(be_svn)
    print "¿¿¿¿¿¿¿¿¿¿...\n"
    print "¿¿¿¿¿¿¿·¿...¿¿¿¿¿¿¿¿Crtl+c¿¿¿¿·¿..."
    for ip in ip_list:
        try:
            print ip + "..."
            rsync = 'rsync -avz --delete --exclude "sinasrv_config" --port=8875 --timeout=15 --contimeout=10 ' + path + 'framework/trunk/ ' + ip + '::newwap/be > /dev/null 2>&1'
            mid = subprocess.Popen(rsync,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
            status = mid.communicate()[1]
            if status != '':
                print " ¿¿¿¿¿... " + ip + " ¿¿¿¿¿¿¿¿¿¿¿¿÷¿¿¿¿¿rsync8875¿¿¿¿¿¿¿¿¿...\n"
        except KeyboardInterrupt:
            print "¿¿¿¿¿¿·¿¿¿¿¿¿¿¿¿...."
            sys.exit()
    print "¿¿¿¿¿¿·¿¿¿¿...\n"

def picsrc_issue(app):
    ip_list = ('10.13.1.112','172.16.174.81','10.71.16.57')
    checkout(app)
    print "picsrc¿¿¿¿¿¿¿¿¿¿..."
    for ip in ip_list:
        print ip + "..."
        rsync = 'rsync -avz --delete --exclude "sinasrv_config" --port=8875 --timeout=15 --contimeout=10 ' + path + app + '/trunk/ ' + ip + '::newwap/' + app + ' > /dev/null 2>&1'
        mid = subprocess.Popen(rsync,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
        status = mid.communicate()[1]
        if status != '':
            print " ¿¿¿¿¿... " + ip + " ¿¿¿¿¿¿¿¿¿¿¿¿÷¿¿¿¿¿rsync8875¿¿¿¿¿¿¿¿¿...\n"
    print "picsrc¿¿¿¿¿·¿¿¿¿..."

def rollbak():
    print "¿¿¿¿¿¿¿¿¿: "
    bak_list = "ls " + bakpath
    bak_list = os.popen(bak_list).read()
    print bak_list
    app = raw_input("¿¿¿¿¿¿¿¿¿¿¿¿¿¿(¿¿¿¿¿¿¿¿¿¿¿·¿¿¿¿¿¿): ")
    for ip in ip_list:
        try:
            print ip + "..."
            rsync = 'rsync -avz --delete --exclude "sinasrv_config" --port=8875 --timeout=15 --contimeout=10 ' + bakpath + app + '/ ' + ip + '::newwap/' + app + ' > /dev/null 2>&1'
            mid = subprocess.Popen(rsync,stdout=subprocess.PIPE,std=subprocess.PIPE,shell=True)
            status = mid.communicate()[1]
            if status != '':
                print " ¿¿¿¿¿... " + ip + " ¿¿¿¿¿¿¿¿¿¿¿¿÷¿¿¿¿¿rsync8875¿¿¿¿¿¿¿¿¿...\n"
        except Keyboardinterrupt:
            print "¿¿¿¿¿¿·¿¿¿¿¿¿¿¿¿...."
            sys.exit()
    print "¿¿¿¿¿¿..."

def admin():
    print "¿¿¿¿¿¿¿¿"
    admin_list = "ls " + adminpath
    admin_list = os.popen(admin_list).read()
    print admin_list
    app = raw_input("¿¿¿¿¿¿¿¿·¿¿¿¿¿¿¿: ")
    svn = 'svn export https://svn1.intra.sina.com.cn/wapcms/newwap/admin/' + app + '/trunk ' + adminpath + app + ' --force'
    os.system(svn)
    chown = 'chown -R www.www /data1/server/admin/yueduadmin/runtime'
    os.system(chown)
    print adminip + "..."
    rsync = 'rsync -avz --delete --exclude "sinasrv_config" --port=8875 --timeout=15 --contimeout=10 ' + adminpath + app + '/ ' + adminip + '::newwap/' + app
    print rsync
    os.system(rsync)
    print "¿·¿¿¿¿..."

def langshou():
    option = {
        1:'¿¿¿¿¿¿¿¿172.16.181.78',
        2:'¿¿¿¿¿¿¿¿'
    }
    for k,v in option.iteritems():
        print "%d: " % k,v
    ch = raw_input("¿¿¿¿¿¿¿¿·¿¿¿¿¿¿: ")
    if ch == "1":
        print "¿¿¿¿¿¿¿¿¿¿¿¿¿¿..."
        svn = 'svn export https://svn1.intra.sina.com.cn/wapcms/wap_remoulds/home_page/trunk /data1/server/langshou/  --force '#> /dev/null 2>&1'
        print svn + ' ...'
        os.system(svn)
        print '¿¿¿¿¿¿¿¿¿¿¿·¿¿¿¿¿¿¿¿172.16.181.78...'
        rsync = 'rsync -avz --delete --exclude "sinasrv_config" --timeout=15 --contimeout=10 /data1/server/langshou/ 172.16.181.78::langshou_code'
        os.system(rsync)
        print '¿·¿¿¿¿...'
    elif ch == "2":
        print "¿¿¿¿¿¿¿¿¿¿¿¿¿¿..."
        svn = 'svn export https://svn1.intra.sina.com.cn/wapcms/wap_remoulds/home_page/trunk /data1/server/langshou/  --force > /dev/null 2>&1'
        #svn = 'svn export https://svn1.intra.sina.com.cn/wapcms/wap_remould_offline/home_page /data1/server/langshou/  --force > /dev/null 2>&1'
        print svn + ' ...'
        os.system(svn)
        print '¿¿¿¿¿¿¿¿¿¿¿·¿...¿¿¿¿¿¿¿¿Crtl+c¿¿¿¿·¿...'
        ip_list = check_ip_file(langshou_ip)
        for ip in ip_list:
            try:
                print ip + '...'
                rsync = 'rsync -avz --delete --exclude "sinasrv_config" --timeout=15 --contimeout=10  /data1/server/langshou/ ' + ip + '::langshou_code  > /dev/null 2>&1'
                mid = subprocess.Popen(rsync,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
                status = mid.communicate()[1]
                if status != '':
                    print " ¿¿¿¿¿... " + ip + " ¿¿¿¿¿¿¿¿¿¿¿¿÷¿¿¿¿¿rsync8875¿¿¿¿¿¿¿¿¿...\n"
            except Keyboardinterrupt:
                print "¿¿¿¿¿¿·¿¿¿¿¿¿¿¿¿...."
                sys.exit()
        print "¿·¿¿¿¿..."
    else:
        print "err..."

if __name__ == '__main__':

    ip_list = check_ip_file(server)
    issueoption = {
        1:'app',
        2:'be¿¿¿',
        3:'picsrc',
        4:'¿·¿¿¿¿¿¿¿¿¿¿¿¿(10.13.1.233)',
        5:'¿·¿¿¿¿¿¿¿¿¿¿¿(10.13.1.233)',
        6:'¿¿¿¿¿¿¿·¿',
        7:'¿¿¿¿¿·¿¿¿¿¿¿¿¿',
        8:'¿¿¿¿¿¿¿¿¿(rollbak)',
        9:'¿¿¿¿¿¿¿¿·¿',
        10:'exit'
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
            app = "picsrc"
            picsrc_issue(app)
        elif option == 4:
            ip_list = ['10.13.1.233']
            issue()
        elif option == 5:
            ip_list = ['10.13.1.233']
            frame_issue()
        elif option == 6:
            admin()
        elif option == 7:
            ip = raw_input("¿¿¿¿¿¿¿·¿¿¿¿¿¿¿¿¿¿¿,¿¿¿¿¿¿¿¿ip:  ")
            ip_list = []
            ip_list.append(ip)
            ch = raw_input('¿¿¿¿¿¿¿¿¿¿"1" or ¿¿¿¿¿¿¿¿¿"2"¿¿')
            if ch == "1":
                issue()
            elif ch == "2":
                frame_issue()
            else:
                print "err..."
        elif option == 8:
            rollbak()
        elif option == 9:
            langshou()
        elif option == 10:
            sys.exit()
    else:
        print "exit... "

### END ###
