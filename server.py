# -*- coding: utf-8 -*-
import sys
import os
import selectors
import socket
import ssl
import json
import time
import random
import platform
import codecs
import struct
from threading import Thread, Lock, Event
import gc
from time import sleep
import options
import errno
import traceback
import string
from queue import Queue
if sys.version_info.minor >= 11:
	context = None
	def wrap_socket(sock, keyfile=None, certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_TLS_SERVER, ca_certs=None, do_handshake_on_connect=True, suppress_ragged_eofs=True, ciphers=None):
		global context
		if not context:
			context = ssl.SSLContext(ssl_version)
			context.verify_mode = cert_reqs
			context.load_cert_chain(certfile, keyfile)
		return context.wrap_socket(sock=sock, server_side=server_side, do_handshake_on_connect=do_handshake_on_connect, suppress_ragged_eofs=suppress_ragged_eofs)
else:
	wrap_socket = ssl.wrap_socket
debug = False
logfile = None
loggerThread = None
serverThread = None
if hasattr(time, 'monotonic'):
	time.time = time.monotonic
system = platform.system()

class IDGenerator(object):
	"""Generator of client and channel ids.
	"""
	def __init__(self):
		self.value = 0
		self._lock = Lock()


	def next(self):
		"""Increment the counter and return its next value, for use as an id.
		"""
		with self._lock:
			self.value += 1
			# self.value becomes volatile when this block is done, so keep the value we just made.
			val = self.value
		return val


def printError():
	if not options.includeTracebacks:
		return
	global loggerThread
	if loggerThread is None:
		return
	loggerThread.queue.put(sys.exc_info())


def printDebugMessage(msg, level):
	if level > options.loglevel:
		return
	global loggerThread
	if loggerThread is None:
		loggerThread = LoggerThread()
		loggerThread.start()
	loggerThread.queue.put(msg)


close_notifier, close_listener = socket.socketpair()


def sighandler(signum, frame):
	printDebugMessage("Received system signal. Waiting for server stop.", 0)
	serverThread.running = False
	raise


class LoggerThread(Thread):
	def __init__(self):
		super(LoggerThread, self).__init__()
		self.daemon = True
		self.log = None
		try:
			if not debug:
				self.log = codecs.open(logfile, "w", "utf-8")
				sys.stdout = self.log
				sys.stderr = self.log
			print("Logging system initialized.")
		except:
			print("Error opening NVDARemoteServer.log. Incorrect permissions or read only environment.")
			self.printError(sys.exc_info())
		self.running = True
		self.queue = Queue(0)

	def run(self):
		while self.running or not self.queue.empty():
			try:
				item = self.queue.get(True, 10)
				self.queue.task_done()
			except:
				continue
			try:
				print(time.asctime())
				if isinstance(item, str):
					print(item)
				elif isinstance(item, tuple):
					self.printError(item)
				sys.stdout.flush()
			except:
				self.printError(sys.exc_info())
		print("Closing logger thread...")
		try:
			if self.log is not None:
				self.log.close()
		except:
			self.printError(sys.exc_info())

	def printError(self, item):
		try:
			exc, type, trace = item
			traceback.print_exception(exc, type, trace)
		except:
			print("Can't print all stack trace, text encoding error")
		finally:
			sys.stdout.flush()
			sys.stderr.flush()


class baseServer(Thread):
	def __init__(self):
		super(baseServer, self).__init__()
		self.daemon = True
		self.clients = {}
		self.client_sockets = []
		self.clients_lock = Lock()
		self.running = False
		self.evt = Event()
		self.sel = selectors.DefaultSelector()

	def add_client(self, client):
		self.clients_lock.acquire()
		self.clients[client.id] = client
		self.client_sockets.append(client.socket)
		self.sel.register(client.socket, selectors.EVENT_READ | selectors.EVENT_WRITE)
		self.clients_lock.release()

	def remove_client(self, client):
		self.clients_lock.acquire()
		self.client_sockets.remove(client.socket)
		self.sel.unregister(client.socket)
		del self.clients[client.id]
		self.clients_lock.release()

	def client_disconnected(self, client):
		printDebugMessage("Client " + str(client.id) + " has disconnected.", 2)
		if client.password != "":
			printDebugMessage("Sending notification to other clients about client " + str(client.id), 2)
			client.send_to_others(type='client_left', user_id=client.id, client=client.as_dict())
		self.remove_client(client)
		printDebugMessage("Client " + str(client.id) + " removed.", 2)

	def searchId(self, socket):
		id = 0
		self.clients_lock.acquire()
		for c in self.clients.values():
			if socket == c.socket:
				id = c.id
				break
		self.clients_lock.release()
		return id


class Server(baseServer):

	def __init__(self):
		super(Server, self).__init__()
		self.port = options.port
		self.port6 = options.port6
		self.bind_host = options.interface
		self.bind_host6 = options.interface6
		self.channels = {}
		self.ping_time = options.ping_time
		self.sel.register(close_listener, selectors.EVENT_READ)
		printDebugMessage("Initialized instance variables", 2)

	def createServerSocket(self, port, port6, bind_host, bind_host6):
		self.server_sockets = []
		if socket.has_ipv6:
			try:
				server_socket6 = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
				printDebugMessage("IPV6 socket created.", 2)
				printDebugMessage("Setting socket options...", 2)
				if system != 'Windows':
					server_socket6.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack('LL', 60, 0))
				server_socket6.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
				server_socket6.bind((bind_host6, port6, 0, 0))
				server_socket6.listen(5)
				self.server_sockets.append(server_socket6)
				self.sel.register(server_socket6, selectors.EVENT_READ)
				printDebugMessage("IPV6 socket has started listening on port " + str(self.port6), 0)
			except:
				server_socket6.close()
				server_socket6 = None
				printDebugMessage("IPV6 socket cannot process incoming connections with the specified configuration. That means the configured interface and port are used by another application, or your system does not support IPV6. The server may still process incoming IPV4 connections", 0)
		try:
			server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			printDebugMessage("IPV4 socket created.", 2)
			printDebugMessage("Setting socket options...", 2)
			if system != 'Windows':
				server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack('LL', 60, 0))
			server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			server_socket.bind((bind_host, port))
			server_socket.listen(5)
			self.server_sockets.append(server_socket)
			self.sel.register(server_socket, selectors.EVENT_READ)
			printDebugMessage("IPV4 socket has started listening on port " + str(self.port), 0)
		except:
			server_socket.close()
			server_socket = None
			printDebugMessage("IPV4 socket cannot process incoming connections with the specified configuration. In most situations, this means IPV6 socket will process incoming IPV4 connections, so you can ignore this message.", 0)
		if self.server_sockets == []:
			raise  # If there are no sockets in the list, stop the server

	def run(self):
		self.createServerSocket(self.port, self.port6, self.bind_host, self.bind_host6)
		self.running = True
		self.last_ping_time = time.time()
		printDebugMessage("NVDA Remote Server is ready.", 0)
		printDebugMessage("The server is running with pid " + str(os.getpid()), 0)
		printDebugMessage("Server configuration: ", 0)
		printDebugMessage("Configuration file: "+str(options.configfile), 0)
		printDebugMessage("Listening interface: "+str(options.interface), 0)
		printDebugMessage("Listening interface for IPV6: "+str(options.interface6), 0)
		printDebugMessage("Port: "+str(options.port), 0)
		printDebugMessage("Port for IPV6: "+str(options.port6), 0)
		printDebugMessage("Log file: "+str(options.logfile), 0)
		printDebugMessage("Log level: "+str(options.loglevel), 0)
		printDebugMessage("Pid file: "+str(options.pidfile), 0)
		printDebugMessage("Certificate file: "+str(options.certfile), 0)
		printDebugMessage("Private key file: "+str(options.keyfile), 0)
		printDebugMessage("Message of the day: "+str(options.motd), 0)
		printDebugMessage("Always display message of the day: "+str(options.motd_force_display), 0)
		printDebugMessage("Include tracebacks when logging errors: "+str(options.includeTracebacks), 0)
		printDebugMessage("Maximum allowed length for messages: "+str(options.allowedMessageLength), 0)
		printDebugMessage("Connection timeout (in seconds): "+str(options.timeout), 0)
		printDebugMessage("Ping interval for clients (in seconds): "+str(options.ping_time), 0)
		try:
			while self.running:
				self.evt.set()
				try:
					sleep(0.01)
					events = self.sel.select(60)
				except:
					printError()
				if not self.running:
					printDebugMessage("Shutting down server...", 2)
					break
				for sock, event in events:
					if sock.fileobj in self.server_sockets:
						th = Thread(target=self.accept_new_connection, args=[sock.fileobj])
						th.daemon = True
						th.start()
						continue
					id = self.searchId(sock.fileobj)
					if id != 0:
						if event==selectors.EVENT_WRITE or event==selectors.EVENT_READ|selectors.EVENT_WRITE:
							self.clients[id].confirmSend()
							if self.clients[id].canClose:
								self.clients[id].close()
						if event==selectors.EVENT_READ or event==selectors.EVENT_READ|selectors.EVENT_WRITE:
							self.clients[id].handle_data()
						self.evt.set()
				if time.time() - self.last_ping_time >= self.ping_time:
					for client in list(self.clients.values()):
						client.close()
					for channel in list(self.channels.values()):
						channel.ping()
					self.last_ping_time = time.time()
			self.close()
		except:
			printError()

	def accept_new_connection(self, srv_sock):
		try:
			client_sock, addr = srv_sock.accept()
			printDebugMessage("New incoming connection from address " + addr[0] + ", port " + str(addr[1]), 1)
		except:
			printDebugMessage("Error while accepting a new connection.", 0)
			printError()
			return
		try:
			client_sock.settimeout(options.timeout)
			client_sock = wrap_socket(client_sock, keyfile=options.keyfile, certfile=options.certfile, server_side=True)
			client_sock.settimeout(None)
			printDebugMessage("Enabled ssl for client socket.", 2)
		except:
			printDebugMessage("SSL negotiation failed.", 2)
			printError()
			client_sock.close()
			return
		printDebugMessage("Setting socket options...", 2)
		client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		if system != 'Windows':
			client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack('LL', 60, 0))
			client_sock.setsockopt(socket.SOL_SOCKET, socket.SO_SNDTIMEO, struct.pack('LL', 60, 0))
		client = Client(server=self, socket=client_sock, address=addr)
		self.add_client(client)
		printDebugMessage("Added client " +str(client.id) +", address " + addr[0] + ", port " + str(addr[1]), 2)

	def close(self):
		self.running = False
		self.evt.set()
		printDebugMessage("Closing channels...", 2)
		for c in list(self.channels.values()):
			c.running = False
			c.join(10)
		printDebugMessage("Disconnecting clients...", 2)
		for c in list(self.clients.values()):
			c.close()
		printDebugMessage("Closing server socket...", 2)
		for s in self.server_sockets:
			try:
				s.shutdown(socket.SHUT_RDWR)
			except:
				printError()
			self.sel.unregister(s)
			s.close()
		self.sel.unregister(close_listener)
		self.sel.close()


class Channel(baseServer):
	idgen = IDGenerator()
	def __init__(self, server, password):
		super(Channel, self).__init__()
		self.server = server
		self.password = password
		self.id = self.idgen.next()
		printDebugMessage("Created channel " +str(self.id), 3)
		self.evt.set()
		self.checkThread = CheckThread(self)
		self.sel.register(close_listener, selectors.EVENT_READ)

	def run(self):
		self.running = True
		self.checkThread.start()
		while self.running and len(list(self.clients.values())) > 0:
			self.evt.set()
			try:
				sleep(0.01)  # Prevent 100% cpu usage when there's at least one writeable socket
				events = self.sel.select(60)
			except:
				printError()
			for sock, event in events:
				id = self.searchId(sock.fileobj)
				if id != 0:
					if event==selectors.EVENT_WRITE or event==selectors.EVENT_READ|selectors.EVENT_WRITE:
						self.clients[id].confirmSend()
					if event==selectors.EVENT_READ or event==selectors.EVENT_READ|selectors.EVENT_WRITE:
						self.clients[id].handle_data()
				self.evt.set()
		printDebugMessage("Terminating channel " + str(self.id), 3)
		self.terminate()
		self.checkThread.running = False
		self.evt.set()
		self.checkThread.join(5)
		del self.server.channels[self.password]

	def ping(self):
		for client in self.clients.values():
			client.send(type='ping')

	def terminate(self):
		for client in list(self.clients.values()):
			client.close()
		self.sel.unregister(close_listener)
		self.sel.close()


class CheckThread(Thread):
	def __init__(self, channel):
		super(CheckThread, self).__init__()
		self.daemon = True
		self.channel = channel
		self.server = channel.server
		self.timeout = 30
		self.running = False

	def run(self):
		self.running = True
		while self.running:
			try:
				sleep(1)
			except:
				pass
			self.channel.evt.wait(self.timeout)
			if not self.channel.evt.is_set():
				# The channel is blocked, we need to close it
				printDebugMessage("Channel " + str(self.channel.id) + " is blocked. Stopping thread...", 3)
				self.channel.terminate()
				del self.server.channels[self.channel.password]
			else:
				self.channel.evt.clear()
		printDebugMessage("Checker thread for channel " + str(self.channel.id) + " has finished", 3)


class Client(object):
	idgen = IDGenerator()

	def __init__(self, server, socket, address):
		self.server = server
		self.socket = socket
		self.address = address
		self.buffer = ""
		self.buffer2 = ""
		self.password = ""
		self.id = self.idgen.next()
		self.connection_type = None
		self.protocol_version = 1
		self.sendLock = Lock()
		self.canClose = False

	def handle_data(self):
		sock_data = ''
		try:
			sock_data = self.socket.recv(16384).decode()
		except:
			printDebugMessage("Socket error in client " + str(self.id) + " while receiving data", 0)
			printError()
			self.close()
			return
		self.server.evt.set()
		if sock_data == '':  # Disconnect
			printDebugMessage("Received empty buffer from client " + str(self.id) + ", disconnecting", 1)
			self.close()
			return
		data = self.buffer + sock_data
		if options.allowedMessageLength > 0 and len(data) > options.allowedMessageLength:
			printDebugMessage("Received too much data from client " + str(self.id) + ", disconnecting", 1)
			self.close()
			return
		if '\n' not in data:
			self.buffer = data
			return
		self.buffer = ""
		while '\n' in data:
			line, sep, data = data.partition('\n')
			printDebugMessage("Protocol log, received from client " + str(self.id) + "\n" + line, 4)
			self.parse(line)
		self.buffer += data

	def parse(self, line):
		try:
			parsed = json.loads(line)
		except ValueError:
			# We don't understand the parsed data, but we can send it to all clients in this channel
			printError()
			printDebugMessage("parse error, sending raw message", 0)
			self.send_data_to_others(line + "\n")
			return
		if 'type' not in parsed:
			return
		if self.password != "":
			if len(list(self.server.clients.values()))==1:
				self.send(type="nvda_not_connected")
			else:
				self.send_to_others(**parsed)
			return
		fn = 'do_' + parsed['type']
		if hasattr(self, fn):
			getattr(self, fn)(parsed)

	def as_dict(self):
		return dict(id=self.id, connection_type=self.connection_type)

	def do_join(self, obj):
		if 'channel' not in obj or not obj['channel']:
			self.send(type='error', error='invalid_parameters')
			self.canClose = True
			return
		if isinstance(self.server, Channel):
			self.send(type="error", error="already_joined")
			return
		self.password = obj.get('channel', None)
		if self.password not in list(self.server.channels.keys()):
			self.server.channels[self.password] = Channel(self.server, self.password)
		self.server.remove_client(self)
		self.server = self.server.channels[self.password]
		self.server.add_client(self)
		self.connection_type = obj.get('connection_type')
		clients = []
		client_ids = []
		for c in self.server.clients.values():
			if c is not self and self.password == c.password:
				clients.append(c.as_dict())
				client_ids.append(c.id)
		self.send(type='channel_joined', channel=self.password, user_ids=client_ids, clients=clients)
		if options.motd:
			self.send(type='motd', motd=options.motd, force_display=options.motd_force_display)
		self.send_to_others(type='client_joined', user_id=self.id, client=self.as_dict())
		if not self.server.is_alive():
			self.server.start()
		printDebugMessage("Client " + str(self.id) + " (" + str(self.connection_type) +") joined channel "
			+ str(self.server.id)
			+ " with client(s) "
			+ (", ".join([str(i) for i in client_ids]) or "None")
		, 3)


	def do_protocol_version(self, obj):
		version = obj.get('version')
		if not version:
			return
		self.protocol_version = version

	def do_generate_key(self, obj):
		if isinstance(self.server, Channel):
			return
		res = self.generate_key()
		while self.check_key(res):
			res = self.generate_key()
		self.send(type='generate_key', key=res)
		self.canClose = True
		printDebugMessage("Client " + str(self.id) + " generated a key", 2)

	def generate_key(self):
		return "".join([random.choice(string.digits) for i in range(9)])

	def check_key(self, key):
		check = False
		for v in list(self.server.channels.values()):
			if v.password == key:
				check = True
				break
		return check

	def close(self):
		try:
			self.socket.shutdown(socket.SHUT_RDWR)
		except:
			printError()
		self.socket.close()
		printDebugMessage("Connection from " + self.address[0] + ", port " + str(self.address[1]) + " closed.", 1)
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
		msgstr = json.dumps(msg)
		printDebugMessage("Protocol log, sent to client " + str(self.id) + "\n" + msgstr, 4)
		self.socket_send(msgstr + "\n")

	def socket_send(self, msgstr):
		self.sendLock.acquire()
		self.buffer2 = self.buffer2 + msgstr
		self.sendLock.release()

	def confirmSend(self):
		if self.buffer2 != "":
			try:
				self.socket.sendall(bytes(self.buffer2, "utf-8"))
				self.buffer2 = ""
			except:
				printDebugMessage("Socket error in client " + str(self.id) + " while sending data", 0)
				printError()
				self.close()

	def send_data_to_others(self, data):
		try:
			for c in self.server.clients.values():
				if (c.password == self.password) & (c != self):
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
				if (c.password == self.password) & (c != self):
					c.send(origin=origin, **obj)
		except:
			printDebugMessage("Error sending to others.", 0)
			printError()
			return


def startAndWait(service=False):
	global serverThread
	if service:
		printDebugMessage("This server is running as a Windows service, skipping signal handlers setup", 2)
	else:
		try:
			import signal
			if system == 'Linux' or system == 'Windows' or system == 'Darwin' or system.startswith('CYGWIN') or system.startswith('MSYS'):
				printDebugMessage("Configuring signal handlers", 2)
				signal.signal(signal.SIGINT, sighandler)
				signal.signal(signal.SIGTERM, sighandler)
			else:
				printDebugMessage("Warning: this server has not been tested on your platform. We don't have added signals handlers here to avoid errors. Probably you will have to kill the process manually to stop the server.", 0)
		except:
			printDebugMessage("Error setting handler for signals", 0)
			printError()
	serverThread = Server()
	serverThread.start()
	close_notifier.sendall(bytes('\n', "utf-8"))
	try:
		sleep(10)
	except:
		pass
	while serverThread.running:  # Wait actively to catch system signals
		try:
			gc.collect()
			sleep(1)
			serverThread.evt.wait(80)
			if serverThread.evt.is_set():  # clear and continue
				serverThread.evt.clear()
			else:
				if serverThread.running:  # The server is frozen
					printDebugMessage("The server thread seems frozen, stopping the daemon.", 0)
					break
		except:
			pass
	serverThread.join(70)
	close_listener.recv(16384)
	close_notifier.close()
	close_listener.close()
	loggerThread.running = False
	loggerThread.join()


if __name__ == "__main__":
	options.setup()
	logfile = options.logfile
	# If debug is enabled, all platform checks are skipped
	if "debug" in sys.argv:
		debug = True
		startAndWait()
	elif system == 'Linux' or system == 'Darwin' or system.startswith('MSYS'):
		import daemon

		class serverDaemon(daemon.Daemon):
			def run(self):
				startAndWait()
		dm = serverDaemon(options.pidfile)
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
				print("Unknown command")
				sys.exit(2)
			sys.exit(0)
		else:
			print("usage: {program} start|stop|restart|kill [options]. Read the server documentation for more information.".format(program=sys.argv[0]))
			sys.exit(2)
	elif system == 'Windows':
		import win32serviceutil
		import win32service
		import win32event
		import servicemanager

		class NVDARemoteService(win32serviceutil.ServiceFramework):
			_svc_name_ = "NVDARemoteService"
			_svc_display_name_ = "NVDARemote relay server"
			_svc_deps_ = []

			def __init__(self, args):
				win32serviceutil.ServiceFramework.__init__(self, args)
				self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

			def SvcStop(self):
				self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
				serverThread.running = False
				win32event.SetEvent(self.hWaitStop)

			def SvcDoRun(self):
				startAndWait(service=True)

		if len(sys.argv) == 1:
			servicemanager.Initialize(NVDARemoteService._svc_name_, os.path.abspath(servicemanager.__file__))
			servicemanager.PrepareToHostSingle(NVDARemoteService)
			try:
				servicemanager.StartServiceCtrlDispatcher()
			except:
				win32serviceutil.usage()
		else:
			win32serviceutil.HandleCommandLine(NVDARemoteService)
	else:
		startAndWait()
