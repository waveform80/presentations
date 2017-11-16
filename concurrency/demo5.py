import zmq

ctx = zmq.Context.instance()
server = ctx.socket(zmq.ROUTER)
server.bind('inproc://foo')
clients = [ctx.socket(zmq.REQ) for i in range(10)]
for i, client in enumerate(clients):
    client.connect('inproc://foo')
    client.send_string('FOO%d' % i)

messages = []
while server.poll(0):
    messages.append(server.recv_multipart())
for msg in messages:
    print(repr(msg))
