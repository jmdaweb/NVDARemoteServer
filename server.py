# -*- coding: utf-8 -*-
import sys
import os
import select
import socket
import ssl
import json
import time
import random
import platform
import codecs
import struct
from threading import Thread, Lock
from Queue import Queue
from functools import wraps
from time import sleep
protocol="SSL v 23"
import locale
encoding=locale.getpreferredencoding()
reload(sys)
sys.setdefaultencoding(encoding)
import options

#use the higuest available ssl protocol version
def sslwrap(func):
	@wraps(func)
	def bar(*args, **kw):
		global protocol
		if hasattr(ssl, 'PROTOCOL_TLSv1_2'):
			kw['ssl_version'] = ssl.PROTOCOL_TLSv1_2
			protocol="TLS v 1.2"
		elif hasattr(ssl, 'PROTOCOL_TLSv1_1'):
			kw['ssl_version'] = ssl.PROTOCOL_TLSv1_1
			protocol="TLS v 1.1"
		elif hasattr(ssl, 'PROTOCOL_TLSv1'):
			kw['ssl_version'] = ssl.PROTOCOL_TLSv1
			protocol="TLS v 1"
		elif hasattr(ssl, 'PROTOCOL_SSLv3'):
			kw['ssl_version'] = ssl.PROTOCOL_SSLv3
			protocol="SSL v 3"
		return func(*args, **kw)
	return bar

ssl.wrap_socket = sslwrap(ssl.wrap_socket)
debug=False
logfile=None
loggerThread=None
import traceback
def printError():
	global loggerThread
	if loggerThread is None:
		return
	loggerThread.queue.put(sys.exc_info())

def printDebugMessage(msg, level):
	if level>options.loglevel:
		return
	global loggerThread
	if loggerThread is None:
		loggerThread=LoggerThread()
		loggerThread.start()
	loggerThread.queue.put(msg)

class LoggerThread(Thread):
	def __init__(self):
		super(LoggerThread, self).__init__()
		self.daemon=True
		self.log=None
		try:
			if debug==False:
				self.log=codecs.open(logfile, "w", "utf-8")
				sys.stdout=self.log
				sys.stderr=self.log
			print "Loggin system initialized."
		except:
			print "Error opening NVDARemoteServer.log. Incorrect permissions or read only environment."
			self.printError(sys.exc_info())
		self.running=True
		self.queue=Queue(0)

	def run(self):
		while self.running or not self.queue.empty():
			try:
				item=self.queue.get(True, None)
				self.queue.task_done()
				print time.asctime()
				if isinstance(item, str) or isinstance(item, unicode):
					print item
				elif isinstance(item, tuple):
					self.printError(item)
				sys.stdout.flush()
			except:
				self.printError(sys.exc_info())
		print "Closing logger thread..."
		try:
			if self.log is not None:
				self.log.close()
		except:
			self.printError(sys.exc_info())

	def printError(self, item):
		try:
			exc, type, trace=item
			traceback.print_exception(exc, type, trace)
		except:
			print "Can't print all stack trace, text encoding error"
		finally:
			sys.stdout.flush()
			sys.stderr.flush()

class baseServer(Thread):
	def __init__(self):
		super(baseServer, self).__init__()
		self.daemon=True
		self.clients={}
		self.client_sockets=[]
		self.running=False

	def add_client(self, client):
		self.clients[client.id] = client
		self.client_sockets.append(client.socket)

	def remove_client(self, client):
		self.client_sockets.remove(client.socket)
		del self.clients[client.id]

	def client_disconnected(self, client):
		printDebugMessage("Client "+str(client.id)+" has disconnected.", 2)
		if client.password!="":
			printDebugMessage("Sending notification to other clients about client "+str(client.id), 2)
			client.send_to_others(type='client_left', user_id=client.id, client=client.as_dict())
		self.remove_client(client)
		printDebugMessage("Client "+str(client.id)+" removed.", 2)

	def searchId(self, socket):
		id=0
		for c in self.clients.values():
			if socket==c.socket:
				id=c.id
				break
		return id

class Server(baseServer):
	PING_TIME = 300

	def __init__(self):
		super(Server, self).__init__()
		self.port = options.port
		self.port6=options.port6
		self.bind_host=options.interface
		self.bind_host6=options.interface6
		self.channels={}
		printDebugMessage("Initialized instance variables", 2)
		self.createServerSocket(self.port, self.port6, self.bind_host, self.bind_host6)

	def createServerSocket(self, port, port6, bind_host, bind_host6):
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if socket.has_ipv6:
			self.server_socket6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
		printDebugMessage("Socket created.", 2)
		self.server_socket = ssl.wrap_socket(self.server_socket, certfile=options.pemfile, server_side=True)
		if socket.has_ipv6:
			self.server_socket6 = ssl.wrap_socket(self.server_socket6, certfile=options.pemfile, server_side=True)
		printDebugMessage("Enabled ssl in socket.", 2)
		printDebugMessage("Setting socket options...", 2)
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack('LL', 60, 0))
		self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		if socket.has_ipv6:
			self.server_socket6.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack('LL', 60, 0))
			self.server_socket6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.server_socket6.bind((bind_host6, port6, 0, 0))
			self.server_socket6.listen(5)
			printDebugMessage("IPV6 socket has started listening on port "+str(self.port6), 0)
		try:
			self.server_socket.bind((bind_host, port))
			self.server_socket.listen(5)
			printDebugMessage("IPV4 socket has started listening on port "+str(self.port), 0)
		except:
			self.server_socket.close()
			self.server_socket=None
			printDebugMessage("IPV4 socket has not been created", 0)
			if socket.has_ipv6==False:
				raise # If there is no IPV6 support and IPV4 socket can't listen, stop the server

	def run(self):
		try:
			import signal
			if (platform.system()=='Linux')|(platform.system()=='Darwin')|(platform.system()=='Windows')|(platform.system().startswith('CYGWIN'))|(platform.system().startswith('MSYS')):
				printDebugMessage("Configuring signal handlers", 2)
				signal.signal(signal.SIGINT, self.sighandler)
				signal.signal(signal.SIGTERM, self.sighandler)
			else:
				printDebugMessage("Warning: this server has not been tested on your platform. We don't have added signals handlers here to avoid errors. Probably you will have to kill the process manually to stop the server.", 0)
		except:
			printDebugMessage("Error setting handler for signals", 0)
			printError()
		self.running = True
		self.last_ping_time = time.time()
		printDebugMessage("NVDA Remote Server is ready.", 0)
		printDebugMessage("The server is using "+protocol, 0)
		printDebugMessage("The server is running with pid "+str(os.getpid()), 0)
		try:
			while self.running:
				try:
					if socket.has_ipv6:
						if self.server_socket is not None:
							r, w, e = select.select(self.client_sockets+[self.server_socket, self.server_socket6], self.client_sockets, self.client_sockets, 60)
						else:
							r, w, e = select.select(self.client_sockets+[self.server_socket6], self.client_sockets, self.client_sockets, 60)
					else:
						r, w, e = select.select(self.client_sockets+[self.server_socket], self.client_sockets, self.client_sockets, 60)
				except:
					printError()
				if not self.running:
					printDebugMessage("Shuting down server...", 2)
					break
				for sock in e:
					id=self.searchId(sock)
					if id!=0:
						printDebugMessage("The client "+str(id)+" has connection problems. Disconnecting...", 1)
						self.clients[id].close()
				for sock in w:
					id=self.searchId(sock)
					if id!=0:
						self.clients[id].confirmSend()
				for sock in r:
					if sock is self.server_socket:
						self.accept_new_connection(sock)
						continue
					if socket.has_ipv6:
						if sock is self.server_socket6:
							self.accept_new_connection(sock)
							continue
					id=self.searchId(sock)
					if id!=0:
						self.clients[id].handle_data()
				if time.time() - self.last_ping_time >= self.PING_TIME:
					for channel in self.channels.values():
						channel.ping()
					self.last_ping_time = time.time()
			self.close()
		except:
			printError()

	def accept_new_connection(self, srv_sock):
		try:
			client_sock, addr = srv_sock.accept()
			printDebugMessage("New incoming connection from address "+addr[0]+", port "+str(addr[1]), 1)
		except:
			printDebugMessage("Error while accepting a new connection.", 0)
			printError()
			if self.server_socket is not None:
				try:
					self.server_socket.shutdown(socket.SHUT_RDWR)
				except:
					printError()
			if socket.has_ipv6:
				try:
					self.server_socket6.shutdown(socket.SHUT_RDWR)
				except:
					printError()
			if self.server_socket is not None:
				self.server_socket.close()
			if socket.has_ipv6:
				self.server_socket6.close()
			printDebugMessage("The server socket has been closed and deleted. The server will create it again.", 0)
			self.createServerSocket(self.port, self.port6, self.bind_host, self.bind_host6)
			return
		printDebugMessage("Setting socket options...", 2)
		client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack('LL', 60, 0))
		client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, struct.pack('LL', 60, 0))
		client = Client(server=self, socket=client_sock, address=addr)
		self.add_client(client)
		printDebugMessage("Added a new client.", 2)

	def close(self):
		self.running = False
		printDebugMessage("Closing channels...", 2)
		for c in self.channels.values():
			c.running=False
		printDebugMessage("Disconnecting clients...", 2)
		for c in self.clients.values():
			c.close()
		printDebugMessage("Closing server socket...", 2)
		if self.server_socket is not None:
			try:
				self.server_socket.shutdown(socket.SHUT_RDWR)
			except:
				printError()
		if socket.has_ipv6:
			try:
				self.server_socket6.shutdown(socket.SHUT_RDWR)
			except:
				printError()
		if self.server_socket is not None:
			self.server_socket.close()
		if socket.has_ipv6:
			self.server_socket6.close()
		loggerThread.running=False
		loggerThread.join()

	def sighandler(self, signum, frame):
		printDebugMessage("Received system signal. Waiting for server stop.", 0)
		self.running=False

class Channel(baseServer):
	def __init__(self, server, password):
		super(Channel, self).__init__()
		self.server=server
		self.password=password
		printDebugMessage("Created new channel with password "+password, 3)
		self.queue=Queue(0)
		self.queue.put(None)
		self.checkThread=CheckThread(self)

	def run(self):
		self.running=True
		self.checkThread.start()
		while self.running and len(self.clients.values())>0:
			try:
				sleep(0.01) # Prevent 100% cpu usage when there's at least one writeable socket
				r, w, e = select.select(self.client_sockets, self.client_sockets, self.client_sockets, 60)
			except:
				printError()
			for sock in e:
				id=self.searchId(sock)
				if id!=0:
					printDebugMessage("The client "+str(id)+" has connection problems. Disconnecting...", 0)
					self.clients[id].close()
			for sock in w:
				id=self.searchId(sock)
				if id!=0:
					self.clients[id].confirmSend()
			for sock in r:
				id=self.searchId(sock)
				if id!=0:
					self.clients[id].handle_data()
			self.queue.put(None)
		printDebugMessage("Terminating channel with password "+self.password, 3)
		self.terminate()
		self.checkThread.running=False
		del self.server.channels[self.password]

	def ping(self):
		for client in self.clients.values():
			client.send(type='ping')

	def terminate(self):
		for client in self.clients.values():
			client.close()

class CheckThread(Thread):
	def __init__(self, channel):
		super(CheckThread, self).__init__()
		self.daemon=True
		self.channel=channel
		self.server=channel.server
		self.timeout=30
		self.running=False

	def run(self):
		self.running=True
		while True:
			try:
				#we have to consume all items in the queue, even if our channel has been closed
				self.channel.queue.get(True, self.timeout)
				self.channel.queue.task_done()
			except:
				if self.running:
					#the channel is blocked, we need to close it
					printDebugMessage("Channel with password "+self.channel.password+" is blocked. Stopping thread...", 3)
					self.channel.terminate()
					del self.server.channels[self.channel.password]
					self.channel._Thread__stop()
				printDebugMessage("Checker thread for channel "+self.channel.password+" has finished", 3)
				break

class Client(object):
	id = 0

	def __init__(self, server, socket, address):
		self.server = server
		self.socket = socket
		self.address=address
		self.buffer = ""
		self.buffer2=""
		self.password=""
		self.id = Client.id + 1
		self.connection_type = None
		self.protocol_version = 1
		Client.id += 1
		self.sendLock=Lock()

	def handle_data(self):
		try:
			data = self.buffer + self.socket.recv(16384)
		except:
			printDebugMessage("Socket error in client "+str(self.id)+" while receiving data", 0)
			printError()
			self.close()
			return
		if data == '': #Disconnect
			printDebugMessage("Received empty buffer from client "+str(self.id)+", disconnecting", 1)
			self.close()
			return
		if '\n' not in data:
			self.buffer = data
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
			#we don't understand the parsed data, but we can send it to all clients in this channel
			printError()
			printDebugMessage("parse error, sending raw message", 0)
			self.send_data_to_others(line+"\n")
			return
		if 'type' not in parsed:
			return
		if self.password!="":
			self.send_to_others(**parsed)
			return
		fn = 'do_'+parsed['type']
		if hasattr(self, fn):
			getattr(self, fn)(parsed)

	def as_dict(self):
		return dict(id=self.id, connection_type=self.connection_type)

	def do_join(self, obj):
		self.password = obj.get('channel', None)
		if not self.password in self.server.channels.keys():
			self.server.channels[self.password]=Channel(self.server, self.password)
		self.server.remove_client(self)
		self.server=self.server.channels[self.password]
		self.server.add_client(self)
		self.connection_type = obj.get('connection_type')
		clients = []
		client_ids = []
		for c in self.server.clients.values():
			if c is not self and self.password==c.password:
				clients.append(c.as_dict())
				client_ids.append(c.id)
		self.send(type='channel_joined', channel=self.password, user_ids=client_ids, clients=clients)
		self.send_to_others(type='client_joined', user_id=self.id, client=self.as_dict())
		if not self.server.isAlive():
			self.server.start()
		printDebugMessage("Client "+str(self.id)+" joined channel "+self.password, 3)

	def do_protocol_version(self, obj):
		version = obj.get('version')
		if not version:
			return
		self.protocol_version = version

	def do_generate_key(self, obj):
		res=self.generate_key()
		while self.check_key(res):
			res=self.generate_key()
		self.send(type='generate_key', key=res)
		printDebugMessage("Client "+str(self.id)+" generated a key", 2)

	def generate_key(self):
		res = str(random.randrange(1, 9))
		for n in xrange(6):
			res += str(random.randrange(0, 9))
		return res

	def check_key(self, key):
		check=False
		for v in self.server.channels.values():
			if v.password==key:
				check=True
				break
		return check

	def close(self):
		try:
			self.socket.shutdown(socket.SHUT_RDWR)
		except:
			printError()
		self.socket.close()
		printDebugMessage("Connection from "+self.address[0]+", port "+str(self.address[1])+" closed.", 1)
		self.server.client_disconnected(self)

	def send(self, type, origin=None, clients=None, client=None, **kwargs):
		msg = dict(type=type, **kwargs)
		if self.protocol_version > 1:
			if origin:
				msg['origin'] = origin
			if clients:
				msg['clients'] = clients
			if client:
				msg['client'] = client
		msgstr = json.dumps(msg)+"\n"
		self.socket_send(msgstr)

	def socket_send(self, msgstr):
		self.sendLock.acquire()
		self.buffer2=self.buffer2+msgstr
		self.sendLock.release()

	def confirmSend(self):
		if self.buffer2!="":
			try:
				self.socket.sendall(self.buffer2)
				self.buffer2=""
			except:
				printDebugMessage("Socket error in client "+str(self.id)+" while sending data", 0)
				printError()
				self.close()

	def send_data_to_others(self, data):
		try:
			for c in self.server.clients.values():
				if (c.password==self.password)&(c!=self):
					c.socket_send(data)
		except:
			printDebugMessage("Error sending to others.", 0)
			printError()
			return

	def send_to_others(self, origin=None, **obj):
		if origin is None:
			origin = self.id
		try:
			for c in self.server.clients.values():
				if (c.password==self.password)&(c!=self):
					c.send(origin=origin, **obj)
		except:
			printDebugMessage("Error sending to others.", 0)
			printError()
			return

def startAndWait():
	srv=Server()
	srv.run()

if (platform.system()=="Linux")|(platform.system()=="Darwin")|(platform.system().startswith('CYGWIN'))|(platform.system().startswith('MSYS')):
	import daemon
	class serverDaemon(daemon.Daemon):
		def run(self):
			startAndWait()

if __name__ == "__main__":
	options.setup()
	logfile=options.logfile
	#If debug is enabled, all platform checks are skipped
	if 'debug' in sys.argv:
		debug=True
		sys.stdout=codecs.getwriter("utf-8")(sys.stdout)
		sys.stderr=codecs.getwriter("utf-8")(sys.stderr)
		startAndWait()
	elif (platform.system()=='Linux')|(platform.system()=='Darwin')|(platform.system().startswith('MSYS')):
		dm=serverDaemon(options.pidfile)
		if len(sys.argv) >= 2:
			if 'start' == sys.argv[1]:
				dm.start()
			elif 'stop' == sys.argv[1]:
				dm.stop()
			elif "restart" == sys.argv[1]:
				dm.restart()
			elif "kill" == sys.argv[1]:
				dm.kill()
			else:
				print "Unknown command"
				sys.exit(2)
			sys.exit(0)
		else:
			print "usage: %s start|stop|restart" % sys.argv[0]
			sys.exit(2)
	else:
		startAndWait()
