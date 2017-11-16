import zmq

ctx = zmq.Context.instance()
back = ctx.socket(zmq.ROUTER)
back.bind('tcp://*:8000')
front = ctx.socket(zmq.ROUTER)
front.bind('tcp://*:8001')
ready = []
busy = {}

def handle_front():
    if ready:
        client, _, request = front.recv_multipart()
        worker = ready.pop(0)
        busy[worker] = client
        back.send_multipart([worker, _, request])

def handle_back():
    worker, _, response = back.recv_multipart()
    if response != b'READY':
        client = busy.pop(worker)
        front.send_multipart([client, _, response])
    ready.append(worker)

poller = zmq.Poller()
poller.register(back, zmq.POLLIN)
poller.register(front, zmq.POLLIN)
while True:
    for sock, flags in poller.poll(1000):
        if sock == front:
            handle_front()
        elif sock == back:
            handle_back()
