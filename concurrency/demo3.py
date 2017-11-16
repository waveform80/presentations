import zmq

ctx = zmq.Context.instance()
server = ctx.socket(zmq.PUSH)
server.bind('inproc://foo')
clients = [ctx.socket(zmq.PULL) for i in range(10)]
poller = zmq.Poller()
for client in clients:
    client.connect('inproc://foo')
    poller.register(client, zmq.POLLIN)

for client in clients:
    server.send(b'DATA')
for sock, flags in poller.poll(0):
    print(sock, repr(sock.recv()))
