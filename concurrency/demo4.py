import zmq

ctx = zmq.Context.instance()
server = ctx.socket(zmq.REP)
server.bind('inproc://foo')
clients = [ctx.socket(zmq.REQ) for i in range(10)]
for i, client in enumerate(clients):
    client.connect('inproc://foo')
    client.send_string('FOO%d' % i)

while server.poll(100):
    msg = server.recv_string()
    server.send_string(msg.replace('FOO', 'BAR'))
for client in clients:
    print(client.recv_string())
