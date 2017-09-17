# -*- coding: utf-8 -*-
import platform
import sys
import codecs
import os
#global variables
configfile=None
interface=None
interface6=None
port=None
logfile=None
pidfile=None
loglevel=None
pemfile=None
def setup():
	global configfile, port, interface, pidfile, logfile, loglevel, pemfile, interface6
	#set default arguments
	port=6837
	interface=""
	interface6=""
	loglevel=3
	if (platform.system()=='Linux')|(platform.system()=='Darwin')|(platform.system().startswith('MSYS'))|(platform.system().startswith('CYGWIN')):
		pidfile="/var/run/NVDARemoteServer.pid"
		logfile="/var/log/NVDARemoteServer.log"
		configfile="/etc/NVDARemoteServer.conf"
		pemfile="/usr/share/NVDARemoteServer/server.pem"
	else:
		if hasattr(sys, 'frozen'):
			logfile=os.path.join(os.path.abspath(os.path.dirname(sys.executable)), "NVDARemoteServer.log")
			configfile=os.path.join(os.path.abspath(os.path.dirname(sys.executable)), "NVDARemoteServer.conf")
			pemfile=os.path.join(sys.prefix, 'server.pem')
		else:
			logfile=os.path.join(os.path.abspath(os.path.dirname(__file__)), "NVDARemoteServer.log")
			configfile=os.path.join(os.path.abspath(os.path.dirname(__file__)), "NVDARemoteServer.conf")
			pemfile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'server.pem')
		pidfile=""
	arguments=parseArguments()
	if "configfile" in arguments.keys():
		configfile=arguments['configfile']
	config={}
	try:
		config=readConfig()
	except:
		print "Can't open the configuration file, using default or commandline values"
	for k, v in config.iteritems():
		setattr(sys.modules[__name__], k, v)
	#the command line arguments are parsed after the configfile. They take priority over the options in the file
	for k, v in arguments.iteritems():
		setattr(sys.modules[__name__], k, v)

def parseArguments():
	options={}
	for arg in sys.argv:
		if arg.startswith("--"):
			option=arg.split("=")
			try:
				option[0]=option[0].replace("--", "")
				if option[0] in ["port", "loglevel"]:
					option[1]=int(option[1])
				options[option[0]]=option[1]
			except:
				pass
	return options

def readConfig():
	options={}
	global configfile
	f=codecs.open(configfile, "r", "utf-8")
	content=f.read()
	f.close()
	lines=content.split("\n")
	for line in lines:
		if line.startswith("#") or line=="":
			continue
		option=line.split("=")
		try:
			if option[0] in ["port", "loglevel"]:
				option[1]=int(option[1])
			options[option[0]]=option[1]
		except:
			pass
	return options
