import zmq

ctx = zmq.Context.instance()
sock = ctx.socket(zmq.REQ)
sock.connect('tcp://ip-address-here:8001')

def get_random(lo=0, hi=1):
    sock.send_json([lo, hi])
    return sock.recv_json()

for i in range(10):
    print(get_random())
