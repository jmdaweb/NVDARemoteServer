from setuptools import setup, find_packages
import py2exe
import platform
from glob import glob

def get_data():
 if platform.architecture()[0][:2] == "32":
  return [
  ("Microsoft.VC90.CRT", glob("windows/msvc32/Microsoft.VC90.CRT/*")),
  ("Microsoft.VC90.MFC", glob("windows/msvc32/Microsoft.VC90.MFC/*")),]
 elif platform.architecture()[0][:2] == "64":
  return [
  ("Microsoft.VC90.CRT", glob("windows/msvc64/Microsoft.VC90.CRT/*")),
  ("Microsoft.VC90.MFC", glob("windows/msvc64/Microsoft.VC90.MFC/*")),]

if __name__ == '__main__':
 setup(
  name = "NVDARemote relay server",
  author = "Jose Manuel Delicado",
  author_email = "jm.delicado@technow.es",
  version = "1.0",
  url = "https://www.technow.es",
  data_files = get_data()+[("", ["server.pem", "windows/service_manager.cmd"])],
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
}
  ],
  service = [
   {
    'modules': ['service'],
    'cmdline_style':'pywin32',
    'dest_base': 'NVDARemoteService',
}
  ],
  install_requires = [
  ]
 )
