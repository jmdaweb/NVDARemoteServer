# -*- mode: python -*-
import sys
import platform
block_cipher = None
arch = platform.architecture()[0][:2]
libs = []
if sys.version.startswith("3"):
	arch = arch + "_py3"
	libs = [("windows/msvc" + arch + "/*.dll", ".")]

a = Analysis(['server.py'], pathex=[], binaries=libs, datas=[("windows/*.cmd", "."), ("windows/msvc" + arch + "/openssl*", "."), ("server.pem", "."), ("NVDARemoteServer.conf", ".")], hiddenimports=["win32timezone"], hookspath=[], runtime_hooks=[], excludes=[], win_no_prefer_redirects=False, win_private_assemblies=False, cipher=block_cipher, optimize=2)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz, a.scripts, exclude_binaries=True, name='NVDARemoteServer', debug=False, strip=False, upx=False, console=True, contents_directory=".")
coll = COLLECT(exe, a.binaries, a.zipfiles, a.datas, strip=False, upx=False, name='NVDARemoteServer')
