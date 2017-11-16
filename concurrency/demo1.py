import zmq

ctx = zmq.Context.instance()
server = ctx.socket(zmq.PULL)
server.bind('inproc://foo')
client = ctx.socket(zmq.PUSH)
client.connect('inproc://foo')
client.send(b'DATA')
print(repr(server.recv()))
