import zmq

ctx = zmq.Context.instance()
server = ctx.socket(zmq.PUB)
server.bind('inproc://foo')
clients = [ctx.socket(zmq.SUB) for i in range(10)]
for client in clients:
    client.connect('inproc://foo')
    client.setsockopt_string(zmq.SUBSCRIBE, '')

server.send_string('FOO')
for client in clients:
    print(client.recv_string())
