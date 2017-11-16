import zmq

ctx = zmq.Context.instance()
server = ctx.socket(zmq.PULL)
server.bind('inproc://foo')
clients = [ctx.socket(zmq.PUSH) for i in range(10)]
for client in clients:
    client.connect('inproc://foo')
    client.send(b'DATA')

for i in range(10):
    print(repr(server.recv()))
