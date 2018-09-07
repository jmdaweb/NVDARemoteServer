# -*- mode: python -*-
import sys
block_cipher = None
import platform
arch=platform.architecture()[0][:2]
libs=[("win32serviceutil.pyd", ".")]
if sys.version.startswith("3"):
 arch=arch+"_py3"
 libs=libs+[("windows/msvc"+arch+"/*.dll", ".")]

a = Analysis(['server.py'],
             pathex=[],
             binaries=libs,
             datas=[("windows/*.cmd", "."), ("windows/msvc"+arch+"/openssl*", "."), ("server.pem", ".")],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='NVDARemoteServer',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='NVDARemoteServer')
