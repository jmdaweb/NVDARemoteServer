# -*- coding: utf-8 -*-
import sys
import os
import time
import atexit
from signal import SIGTERM, SIGKILL


class Daemon(object):
	"""
	A generic daemon class.
	
	Usage: subclass the Daemon class and override the run() method
	"""
	def __init__(self, pidfile, stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
		self.stdin = stdin
		self.stdout = stdout
		self.stderr = stderr
		self.pidfile = pidfile
	
	def daemonize(self):
		"""
		do the UNIX double-fork magic, see Stevens' "Advanced
		Programming in the UNIX Environment" for details (ISBN 0201563177)
		http://www.erlenstar.demon.co.uk/unix/faq_2.html#SEC16
		"""
		try:
			pid = os.fork()
			if pid > 0:
				# exit first parent
				sys.exit(0)
		except OSError as e:
			sys.stderr.write("fork #1 failed: {code} ({msg})\n".format(code=e.errno, msg=e.strerror))
			sys.exit(1)
		# decouple from parent environment
		os.chdir("/")
		os.setsid()
		os.umask(0)
		# do second fork
		try:
			pid = os.fork()
			if pid > 0:
				# exit from second parent
				sys.exit(0)
		except OSError as e:
			sys.stderr.write("fork #2 failed: {code} ({msg})\n".format(code=e.errno, msg=e.strerror))
			sys.exit(1)
		# redirect standard file descriptors
		sys.stdout.flush()
		sys.stderr.flush()
		si = open(self.stdin, 'r')
		so = open(self.stdout, 'a+')
		# http://bugs.python.org/issue17404
		se = open(self.stderr, 'a+', buffering=1)
		os.dup2(si.fileno(), sys.stdin.fileno())
		os.dup2(so.fileno(), sys.stdout.fileno())
		os.dup2(se.fileno(), sys.stderr.fileno())
		si.close()
		so.close()
		se.close()
		# write pidfile
		atexit.register(self.delpid)
		pid = str(os.getpid())
		try:
			file = open(self.pidfile, 'w+')
		except:
			print("Can't open file '{file}' for writing. Perhaps the config is broken. If this instance is started by a service manager such as systemd or open-rc it might have consequences!".format(file=self.pidfile))
			return
		file.write("{id}\n".format(id=pid))
		file.close()

	def delpid(self):
		os.remove(self.pidfile)

	def start(self):
		"""
		Start the daemon
		"""
		# Check for a pidfile to see if the daemon already runs
		try:
			pf = open(self.pidfile, 'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
		if pid:
			message = "pidfile {pidfile} already exist. Daemon already running?\n"
			sys.stderr.write(message.format(pidfile=self.pidfile))
			sys.exit(1)
		
		# Start the daemon
		self.daemonize()
		self.run()

	def stop(self):
		"""
		Stop the daemon
		"""
		# Get the pid from the pidfile
		try:
			pf = open(self.pidfile, 'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
		if not pid:
			message = "pidfile {pidfile} does not exist. Daemon not running?\n"
			sys.stderr.write(message.format(pidfile=self.pidfile))
			return  # not an error in a restart

		# Try killing the daemon process
		try:
			while 1:
				os.kill(pid, SIGTERM)
				time.sleep(0.1)
		except OSError as err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print(str(err))
				sys.exit(1)

	def kill(self):
		"""
		Force kill of daemon
		"""
		# Get the pid from the pidfile
		try:
			pf = open(self.pidfile, 'r')
			pid = int(pf.read().strip())
			pf.close()
		except IOError:
			pid = None
		if not pid:
			message = "pidfile {pidfile} does not exist. Daemon not running?\n"
			sys.stderr.write(message.format(self.pidfile))
			return  # not an error in a restart

		# Try killing the daemon process
		try:
			while 1:
				os.kill(pid, SIGKILL)
				time.sleep(0.1)
		except OSError as err:
			err = str(err)
			if err.find("No such process") > 0:
				if os.path.exists(self.pidfile):
					os.remove(self.pidfile)
			else:
				print(str(err))
				sys.exit(1)

	def restart(self):
		"""
		Restart the daemon
		"""
		self.stop()
		self.start()

	def run(self):
		"""
		You should override this method when you subclass Daemon. It will be called after the process has been
		daemonized by start() or restart().
		"""
