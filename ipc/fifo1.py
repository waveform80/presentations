import io
import os

pid = os.fork()
try:
    os.mkfifo('my_fifo')
except IOError:
    f = io.open('my_fifo', 'rb', buffering=0)
    os.remove('my_fifo')
    print(f.read(5).decode('ascii'))
else:
    f = io.open('my_fifo', 'wb', buffering=0)
    f.write(b'hello')
# Talk over your FIFO one way (use two for duplex comms)
# What happens with unbounded read?
