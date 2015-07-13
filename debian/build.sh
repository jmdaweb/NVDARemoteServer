#!/bin/bash
#please, run this script as root
#make directories
mkdir -p nvda-remote-server_1.0/usr/share/NVDARemoteServer
#copy files
cp ../server.py ../server.pem ../daemon.py nvda-remote-server_1.0/usr/share/NVDARemoteServer
#change permissions
chown -R root nvda-remote-server_1.0
chgrp -R root nvda-remote-server_1.0
chmod -R 755 nvda-remote-server_1.0
chmod 644 nvda-remote-server_1.0/DEBIAN/control
chmod 644 nvda-remote-server_1.0/DEBIAN/conffiles
chmod -x nvda-remote-server_1.0/usr/share/NVDARemoteServer/server.py
chmod -x nvda-remote-server_1.0/usr/share/NVDARemoteServer/server.pem
chmod -x nvda-remote-server_1.0/usr/share/NVDARemoteServer/daemon.py
chmod -x nvda-remote-server_1.0/usr/share/doc/nvda-remote-server/copyright
chmod -x nvda-remote-server_1.0/usr/share/man/man1/NVDARemoteServer.1.gz
chmod -x nvda-remote-server_1.0/usr/share/doc/nvda-remote-server/changelog.Debian.gz
#build the package
dpkg-deb --build nvda-remote-server_1.0
