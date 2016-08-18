import os

pid = os.fork()
if pid:
    print("I'm the parent, my child process is PID %d" % pid)
else:
    print("I'm the child process")
