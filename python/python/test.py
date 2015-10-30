import os

def child():
    print 'A new child:', os.getpid()
    print 'Parent id is:', os.getppid()

def parent():
    while True:
        newpid=os.fork()
        print newpid
        if newpid==0:
            child()
        else:
            pids=(os.getpid(),newpid)
            print "parent:%d,child:%d"%pids
            print "parent parent:",os.getppid()
        if raw_input()=='q':
            break

parent()
