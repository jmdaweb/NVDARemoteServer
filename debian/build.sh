#!/bin/bash
#please, run this script as root
#This script builds a debian package, but lintian still reports some errors and warnings. Despite of that, it can be installed.
#make directories
mkdir -p package/usr/share/NVDARemoteServer
#copy files
cp ../server.py ../server.pem ../daemon.py package/usr/share/NVDARemoteServer
#change permissions
chown -R root package
chgrp -R root package
chmod -R 755 package
chmod 644 package/DEBIAN/control
chmod 644 package/DEBIAN/conffiles
chmod -x package/usr/share/NVDARemoteServer/server.py
chmod -x package/usr/share/NVDARemoteServer/server.pem
chmod -x package/usr/share/NVDARemoteServer/daemon.py
chmod -x package/usr/share/doc/nvda-remote-server/copyright
chmod -x package/usr/share/man/man1/NVDARemoteServer.1.gz
chmod -x package/usr/share/lintian/overrides/nvda-remote-server
#build the package
dpkg-deb --build package
mv package.deb nvda-remote-server.deb
