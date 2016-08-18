import io
import os
from time import sleep

f = io.open('my_data', 'w+')
pid = os.fork()
if pid:
    print("I'm the master: sending data")
    f.write("hello")
else:
    print("I'm the slave: waiting for data")
    sleep(1)
    f.seek(0)
    print("Received", f.read())
