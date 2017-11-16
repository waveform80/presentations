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
for addr, empty, msg in messages:
    msg = msg.decode('utf-8')
    msg = msg.replace('FOO', 'BAR')
    msg = msg.encode('utf-8')
    server.send_multipart([addr, empty, msg])
for client in clients:
    print(client.recv_string())
