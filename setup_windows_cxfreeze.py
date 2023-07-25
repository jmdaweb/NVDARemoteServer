# -*- coding: utf-8 -*-
from cx_Freeze import setup, Executable
import platform
import sys
from glob import glob


def get_data():
	data = ["server.pem", "windows/service_manager.cmd", "windows/debug.cmd", "windows/NVDARemoteCertificate.cmd", "NVDARemoteServer.conf"]
	if platform.architecture()[0][:2] == "32" and sys.version.startswith("2"):
		return data + ["windows/msvc32/openssl.exe", "windows/msvc32/openssl.cnf"]
	elif platform.architecture()[0][:2] == "64" and sys.version.startswith("2"):
		return data + ["windows/msvc64/openssl.exe", "windows/msvc64/openssl.cnf"]
	elif platform.architecture()[0][:2] == "32" and sys.version.startswith("3"):
		return data + glob("windows/msvc32_py3/*")
	elif platform.architecture()[0][:2] == "64" and sys.version.startswith("3"):
		return data + glob("windows/msvc64_py3/*")


build_exe_options = {
	'optimize': 2,
	'include_msvcr': True,
	'bin_excludes': ['CRYPT32.dll'],
	'include_files': get_data(),
	'includes': ['win32timezone'],
	'zip_include_packages': "*",
	'zip_exclude_packages': [],
}

if __name__ == '__main__':
	setup(
		name="NVDARemote server",
		author="Jose Manuel Delicado",
		author_email="jm.delicado@nvda.es",
		version="2.3",
		url="https://github.com/jmdaweb/NVDARemoteServer",
		description="NVDA Remote Relay Server",
		options={
			'build_exe': build_exe_options,
		},
		executables=[
			Executable("server.py", targetName="NVDARemoteServer.exe")
		]
	)
