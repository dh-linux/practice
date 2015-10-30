#!/usr/bin/env python
# coding: utf-8
# author: baoliang1 , 5693
# changetime: 2014-3-21
# version: 2.1

import socket
import os
import sys
import subprocess
import signal
import time
import select


#########################################################################################

### config listen
listen_addr = '0.0.0.0'
listen_port = 12345
max_connect = 100


### config process
# white_ctrl_list : what server_ip can connect .
# daemon_tag : if tag is 'daemon' , process may run in bakup ,and return 0 immediately .
# run_dir : work dir when run
# run_pid : process id when agent run .
# run_log : record command and other info . set null can close log record .

white_ctrl_list = ['10.210.215.250','10.13.48.232','10.13.3.69']
daemon_tag = 'daemon'
run_dir = sys.path[0]
run_pid = sys.path[0] + '/run.pid'
#run_log = sys.path[0] + '/run.log'
run_log = ''

#########################################################################################


# process signal of SIGCHLD for recycle child process 
def sig_handler(signum,frame):
	while True:
		try:
			pid,sts = os.waitpid(-1, os.WNOHANG)
		except OSError:
			return

# record logs
def write_log(content=''):
	try:
		if run_log != '': 
			c_time = time.strftime("%Y-%m-%d_%H:%M:%S ", time.localtime())
			content = content + '\n'
			logfile = open(run_log,'a')
			logfile.write(c_time + content)
			logfile.close()
	except:
		pass
	return

# record run_pid
def write_pid(t_pid=0):
	f_pid = open(run_pid,'w')
	f_pid.write(str(t_pid))
	f_pid.close()

# main function
def work():
    ## socket bind
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((listen_addr,listen_port))
		sock.listen(max_connect)
		pid = os.fork()
		if pid > 0 :
			write_pid(pid)
			write_log('Start run ...')
			sys.exit(0)
	except socket.error , x:
		print 'Error :',x
		sys.exit(1)

    ## listen , wait for accept command
	while True:
		try:
			conn, addr = sock.accept()
			pid = os.fork()
			if pid > 0:
				conn.close()
				continue
			if pid == 0:
				pid = os.fork()
				if pid > 0:
					conn.close()
					sys.exit(0)
			    ## check white_list
				if str(addr[0]) not in white_ctrl_list:
					result = str(addr) + 'denied'
					write_log(result)
					conn.send(result)
				else:
					ret = conn.recv(2048)
					write_log(ret)
				    ## ret ,split with ''':<<|>>:''' ,example: uptime:<<|>>:30:<<|>>:baoliang1
					tag = ret.split(':<<|>>:')[1]
					cmdline = ret.split(':<<|>>:')[0]
					p = subprocess.Popen(cmdline, cwd = run_dir,
								shell = True,
								executable = "/bin/bash",
								stdout = subprocess.PIPE, 
								stderr = subprocess.STDOUT )
				    ## return result to ctrl server
                                        result=''
					if tag != daemon_tag:
						p.stdout.flush()
					    ## timeout process
						timeout = int(tag)
						fs = select.select([p.stdout], [], [], timeout)
						if p.stdout in fs[0]:
							for line in p.stdout.readlines():
								result += str(line)
						else:
						    ## when timeout , kill child pid
							os.kill(p.pid, signal.SIGKILL)
							result = 'Killed . TimeOut in ' + str(timeout) + 's'
					if result == '':
						result = '0'
					conn.send(result)
				conn.close()
				sys.exit(0)
		except KeyboardInterrupt:
			write_log('Be killed ..')
			sys.exit(2)
		except AttributeError:
			pass
		except IOError:
			pass
		except socket.error:
			pass
		except TypeError:
			pass
	sock.close()

if __name__ == '__main__':
	signal.signal(signal.SIGCHLD, sig_handler)
	work()

