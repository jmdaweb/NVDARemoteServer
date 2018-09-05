# -*- coding: utf-8 -*-
import win32serviceutil
import win32service
import win32event
import server
import os
import sys
import options
import servicemanager

class NVDARemoteService(win32serviceutil.ServiceFramework):
	_svc_name_ = "NVDARemoteService"
	_svc_display_name_ = "NVDARemote relay server"
	_svc_deps_ = []
	def __init__(self, args):
		options.setup()
		server.logfile=options.logfile
		win32serviceutil.ServiceFramework.__init__(self, args)
		self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
		self.srv=server.Server()

	def SvcStop(self):
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		self.srv.running=False
		win32event.SetEvent(self.hWaitStop)

	def SvcDoRun(self):
		self.srv.run()

if __name__ == '__main__':
	if len(sys.argv)==1:
		servicemanager.Initialize(NVDARemoteService._svc_name_, os.path.abspath(servicemanager.__file__))
		servicemanager.PrepareToHostSingle(NVDARemoteService)
		try:
			servicemanager.StartServiceCtrlDispatcher()
		except:
			win32serviceutil.usage()
	else:
		win32serviceutil.HandleCommandLine(NVDARemoteService)
