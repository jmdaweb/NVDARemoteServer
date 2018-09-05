# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import py2exe
import platform
from glob import glob

def get_data():
 if platform.architecture()[0][:2] == "32":
  return [
  ("Microsoft.VC90.CRT", glob("windows/msvc32/Microsoft.VC90.CRT/*")),
  ("Microsoft.VC90.MFC", glob("windows/msvc32/Microsoft.VC90.MFC/*")),
  ("", ["windows/msvc32/openssl.exe", "windows/msvc32/openssl.cnf"])]
 elif platform.architecture()[0][:2] == "64":
  return [
  ("Microsoft.VC90.CRT", glob("windows/msvc64/Microsoft.VC90.CRT/*")),
  ("Microsoft.VC90.MFC", glob("windows/msvc64/Microsoft.VC90.MFC/*")),
  ("", ["windows/msvc64/openssl.exe", "windows/msvc64/openssl.cnf"])]

if __name__ == '__main__':
 setup(
  name = "NVDARemote server",
  author = "Jose Manuel Delicado",
  author_email = "jm.delicado@nvda.es",
  version = "1.7",
  url = "https://github.com/jmdaweb/NVDARemoteServer",
  data_files = get_data()+[("", ["server.pem", "windows/service_manager.cmd", "windows/debug.cmd", "windows/NVDARemoteCertificate.cmd", "NVDARemoteServer.conf"])],
options = {
   'py2exe': {   
    'optimize':2,
    'dll_excludes': ["CRYPT32.dll"],
    'compressed': True
   },
  },
  console = [
   {
    'script': 'server.py',
    'dest_base': 'NVDARemoteServer',
},
   {
    'script': 'service.py',
    'dest_base': 'NVDARemoteService',
}
  ],
  install_requires = [
  ]
 )
