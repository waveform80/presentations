import zmq
from random import random
from time import time, sleep

def get_random(lo=0, hi=1):
    start = time()
    sleep(lo + random() * (hi - lo))
    return time() - start

ctx = zmq.Context.instance()
sock = ctx.socket(zmq.REQ)
sock.connect('tcp://ip-address-here:8000')
sock.send(b'READY')
while True:
    lo, hi = sock.recv_json()
    print('Processing request')
    sock.send_json(get_random(lo, hi))
