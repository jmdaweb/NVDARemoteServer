import win32serviceutil
import win32service
import win32event
import server
import os
import sys
class NVDARemoteService(win32serviceutil.ServiceFramework):
	_svc_name_ = "NVDARemoteService"
	_svc_display_name_ = "NVDARemote relay server"
	_svc_deps_ = []
	def __init__(self, args):
		win32serviceutil.ServiceFramework.__init__(self, args)
		self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
		self.srv=server.Server(6837, service=True)
		server.logfile=os.path.join(os.path.abspath(os.path.dirname(sys.executable)), "NVDARemoteServer.log")

	def SvcStop(self):
		self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
		self.srv.close()
		win32event.SetEvent(self.hWaitStop)

	def SvcDoRun(self):
		self.srv.run()
