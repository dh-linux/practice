#!/usr/bin/python2.6
# -*- Mode: python -*-

# Copyright (c) 2009, Andrew McNabb
# Copyright (c) 2003-2008, Brent N. Chun

"""Parallel ssh to the set of nodes in hosts.txt.

For each node, this essentially does an "ssh host -l user prog [arg0] [arg1]
...". The -o option can be used to store stdout from each remote node in a
directory.  Each output file in that directory will be named by the
corresponding remote node's hostname or IP address.
"""

import fcntl
import os
import sys
import getpass

workdir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, "/usr/local/sinabase/lib")
sys.path.insert(0, os.path.expanduser('~') + '/lib')
sys.path.insert(0, workdir + "/../lib")

from psshlib.manager import Manager
from psshlib.task import Task
from psshlib.cli import common_parser, common_defaults, read_config
from expand import expand

cfg = read_config()

if cfg['default'].has_key('normal_timeout'):
    _DEFAULT_TIMEOUT_N = cfg['default']['normal_timeout']
else:
    _DEFAULT_TIMEOUT_N = 5

if cfg['default'].has_key('batch_timeout'):
    _DEFAULT_TIMEOUT_P = cfg['default']['batch_timeout']
else:
    _DEFAULT_TIMEOUT_P = 30

if cfg['default'].has_key('getgroup'):
    _GETHOST = cfg['default']['getgroup']
else:
    _GETHOST = "/usr/local/sinabase/bin/cmdb -e -g"

def option_parser():
    parser = common_parser()
    parser.usage = "%prog [OPTIONS] -g group_name [ 'command [...]' ]"
    parser.usage += "\n       %prog [OPTIONS] -f host_file [ 'command [...]' ]"
    parser.usage += "\n       %prog [OPTIONS] host[1-2] 'command [...]'"
    #parser.epilog = "Example: pgm -b denalihost uptime"
    parser.epilog = None

    parser.add_option('-P', '--print', dest='print_out', action='store_true',
            help='print output as we get it (OPTIONAL)')
    parser.add_option('-i', '--inline', dest='inline', action='store_false', default=True, 
            help='inline aggregated output for each server (OPTIONAL)')

    return parser

def parse_args():
    parser = option_parser()
    defaults = common_defaults()
    parser.set_defaults(**defaults)
    opts, args = parser.parse_args()

    if len(args) == 0:
#        parser.error('Command not specified.')
        if not opts.host_files and not opts.group_names:
            parser.error('Command not specified.')
        setattr(opts, "cmdline", False)

    if opts.batch:
        if not opts.timeout or opts.timeout == -1:
            opts.timeout = int(_DEFAULT_TIMEOUT_P)
    else:
        if not opts.timeout or opts.timeout == -1:
            opts.timeout = int(_DEFAULT_TIMEOUT_N)
        opts.par = 1
    return opts, args

def buffer_input():
    origfl = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
    fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, origfl | os.O_NONBLOCK)
    try:
        stdin = sys.stdin.read()
    except IOError: # Stdin contained no information
        stdin = ""
    fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, origfl)
    return stdin

def do_pssh(hosts, cmdline, opts):
    if opts.outdir and not os.path.exists(opts.outdir):
        os.makedirs(opts.outdir)
    if opts.errdir and not os.path.exists(opts.errdir):
        os.makedirs(opts.errdir)
    stdin = buffer_input()
    manager = Manager(opts)
    for host, port, user in hosts:
        cmd = ['ssh', host, '-o', 'NumberOfPasswordPrompts=1',
               '-o', 'SendEnv=PSSH_NODENUM', '-o', 'StrictHostKeyChecking=no']
        if not opts.verbose:
            cmd.append('-q')
        if opts.options:
            cmd += ['-o', opts.options]
        if user:
            cmd += ['-l', user]
        if port:
            cmd += ['-p', port]
        cmd.append(cmdline)
        t = Task(host, port, cmd, opts, stdin)
        manager.add_task(t)
    manager.run()
    if opts.report:
        manager.report()
   
if __name__ == "__main__":
    opts, args = parse_args()
    if opts.getgroup:
        _GETHOST = os.path.realpath(opts.getgroup)
    if opts.host_files:
        hosts = []
        for file in opts.host_files:
            f = open(file)
            for line in f.readlines():
                if len(line) > 0 and line[0] != '#':
                    hs = line.split()
                    if len(hs) > 0 and hs[0].strip():
                        hosts.append( (hs[0], "", opts.user) )
        if len(args) < 1:
            for host in hosts:
                print host[0]
            print "\n%s hosts" % (len(hosts))
            sys.exit(0)
        cmdline = " ".join(args)
    elif opts.group_names:
        hosts = []
        for group_name in opts.group_names:
            groups = expand(group_name)
            for group in groups:
                if cfg.has_key('group') and cfg['group'].has_key(group):
                    for host in cfg['group'][group].split(','):
                        hosts.append( (host.strip(), "", opts.user) )
                elif os.path.exists(_GETHOST.split(' ')[0]):
                    for host in os.popen("%s %s" % (_GETHOST, group)).read().split():
                        hosts.append( (host, "", opts.user) )
        if len(args) < 1:
            for host in hosts:
                print host[0]
            print "\n%s hosts" % (len(hosts))
            sys.exit(0)
        cmdline = " ".join(args)
    else:
        if len(args) < 2:
            print "Miss args."
            sys.exit(1)
        host_list = args[:-1]
        cmdline = args[-1]
        host_pre = []
        hosts = []
        for host in host_list:
            host_pre = expand(host)
            for h in host_pre:
                hosts.append( (h, "", opts.user) )

    do_pssh(hosts, cmdline, opts)
