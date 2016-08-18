import io
import os

pid = os.fork()
try:
    f = io.open('my_data', 'xb', buffering=0)
except IOError:
    print("Failed to create file; I'm the slave")
    f = io.open('my_data', 'rb', buffering=0)
    os.remove('my_data')
    while True:
        s = f.read()
        if s:
            print("Received", s.decode('ascii'))
            break
else:
    print("Created file; I'm the master!")
    f.write(b'hello')
