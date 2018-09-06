# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable
import platform

def get_data():
 data=["server.pem", "windows/service_manager.cmd", "windows/debug.cmd", "windows/NVDARemoteCertificate.cmd", "NVDARemoteServer.conf"]
 if platform.architecture()[0][:2] == "32":
  return data+["windows/msvc32/openssl.exe", "windows/msvc32/openssl.cnf"]
 elif platform.architecture()[0][:2] == "64":
  return data+["windows/msvc64/openssl.exe", "windows/msvc64/openssl.cnf"]

build_exe_options={
  'optimize': 2,
  'include_msvcr': True,
  'bin_excludes':['CRYPT32.dll'],
  'include_files': get_data(),
  'zip_exclude_packages':"*"
}

if __name__ == '__main__':
 setup(
  name = "NVDARemote server",
  author = "Jose Manuel Delicado",
  author_email = "jm.delicado@nvda.es",
  version = "1.7",
  url = "https://github.com/jmdaweb/NVDARemoteServer",
  description="NVDA Remote Relay Server",
options = {
   'build_exe': build_exe_options,
  },
  executables = [
    Executable("server.py", targetName="NVDARemoteServer.exe")
  ]
 )
