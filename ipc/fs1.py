import io
import os

pid = os.fork()
try:
    f = io.open('my_data', 'x')
except IOError:
    print("Failed to create file; I'm the slave")
    f = io.open('my_data', 'r')
    while True:
        s = f.read()
        if s:
            print("Received", s)
            break
else:
    print("Created file; I'm the master!")
    f.write('hello')
