import io
import os
import mmap

pid = os.fork()
try:
    f = io.open('my_array', 'x+b', buffering=0)
except IOError:
    f = io.open('my_array', 'r+b', buffering=0)
    os.remove('my_array')
f.write(b'\x00' * 128)
m = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_WRITE)
a = np.frombuffer(m, np.uint16, 64)
# ... do what you want with the shared arrays ... 
