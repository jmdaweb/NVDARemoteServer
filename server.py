import sys
import os
import select
import socket
import ssl
import json
import time
import random
import platform

class Server(object):
	PING_TIME = 300

	def __init__(self, port, bind_host=''):
		self.port = port
		#Maps client sockets to clients
		self.clients = {}
		self.client_sockets = []
		self.running = False
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if hasattr(sys, 'frozen'):
			certfile=os.path.join(sys.prefix, 'server.pem')
		else:
			certfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server.pem')
		self.server_socket = ssl.wrap_socket(self.server_socket, certfile=certfile)
		# This reuses the port and avoid "Address already in use" errors.
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server_socket.bind((bind_host, self.port))
		self.server_socket.listen(5)

	def run(self):
		if platform.system()=='Linux':
			try:
				import signal
				signal.signal(signal.SIGINT, self.sighandler)
				signal.signal(signal.SIGTERM, self.sighandler)
				signal.signal(signal.SIGSTOP, self.sighandler)
			except:
				pass
		self.running = True
		self.last_ping_time = time.time()
		while self.running:
			r, w, e = select.select(self.client_sockets+[self.server_socket], [], self.client_sockets, 60)
			if not self.running:
				break
			for sock in r:
				if sock is self.server_socket:
					self.accept_new_connection()
					continue
				self.clients[sock].handle_data()
			if time.time() - self.last_ping_time >= self.PING_TIME:
				for client in self.clients.itervalues():
					if client.password!="":
						client.send(type='ping')
				self.last_ping_time = time.time()

	def accept_new_connection(self):
		try:
			client_sock, addr = self.server_socket.accept()
		except ssl.SSLError:
			return
		client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		client = Client(server=self, socket=client_sock)
		self.add_client(client)

	def add_client(self, client):
		self.clients[client.socket] = client
		self.client_sockets.append(client.socket)

	def remove_client(self, client):
		del self.clients[client.socket]
		self.client_sockets.remove(client.socket)

	def client_disconnected(self, client):
		self.remove_client(client)
		if client.password!="":
			client.send_to_others(type='client_left', user_id=client.id)

	def close(self):
		self.running = False
		self.server_socket.close()

	def sighandler(self, signum, frame):
		self.close()

class Client(object):
	id = 0

	def __init__(self, server, socket):
		self.server = server
		self.socket = socket
		self.buffer = ""
		self.password=""
		self.id = Client.id + 1
		Client.id += 1

	def handle_data(self):
		try:
			data = self.buffer + self.socket.recv(8192)
		except:
			self.close()
			return
		if data == '': #Disconnect
			self.close()
			return
		if '\n' not in data:
			self.buffer += data
			return
		self.buffer = ""
		while '\n' in data:
			line, sep, data = data.partition('\n')
			self.parse(line)
		self.buffer += data

	def parse(self, line):
		try:
			parsed = json.loads(line)
		except ValueError:
			self.close()
			return
		if 'type' not in parsed:
			return
		if self.password!="":
			self.send_to_others(**parsed)
			return
		fn = 'do_'+parsed['type']
		if hasattr(self, fn):
			getattr(self, fn)(parsed)

	def do_join(self, obj):
		self.password = obj.get('channel', None)
		clients = [c.id for c in self.server.clients.values() if c is not self]
		self.send(type='channel_joined', channel=self.password, user_ids=clients)
		self.send_to_others(type='client_joined', user_id=self.id)

	def do_generate_key(self, obj):
		res = str(random.randrange(1, 9))
		for n in xrange(6):
			res += str(random.randrange(0, 9))
		self.send(type='generate_key', key=res)

	def close(self):
		self.socket.close()
		self.server.client_disconnected(self)

	def send(self, type, **kwargs):
		msg = dict(type=type, **kwargs)
		msgstr = json.dumps(msg)+"\n"
		try:
			self.socket.sendall(msgstr)
		except:
			self.close()
			return

	def send_to_others(self, **obj):
		for c in self.server.clients.itervalues():
			if (c.password==self.password)&(c!=self):
				c.send(**obj)

if (platform.system()=="Linux")|(platform.system()=="Darwin"):
	import daemon
	class serverDaemon(daemon.Daemon):
		def run(self):
			srv=Server(6837)
			srv.run()

if __name__ == "__main__":
	if (platform.system()=='Linux')|(platform.system()=='Darwin'):
		dm=serverDaemon('/var/run/NVDARemoteServer.pid')
		if len(sys.argv) == 2:
			if 'start' == sys.argv[1]:
				dm.start()
			elif 'stop' == sys.argv[1]:
				dm.stop()
			elif "restart" == sys.argv[1]:
				dm.restart()
			else:
				print "Unknown command"
				sys.exit(2)
			sys.exit(0)
		else:
			print "usage: %s start|stop|restart" % sys.argv[0]
			sys.exit(2)
	else:
		srv=Server(6837)
		srv.run()
