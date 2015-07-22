#!/bin/bash
#please, run this script as root
#make directories
mkdir -p nvda-remote-server_1.0/usr/share/NVDARemoteServer
mkdir -p nvda-remote-server_1.0/usr/share/man/man1
#copy files
cp ../server.py ../server.pem ../daemon.py nvda-remote-server_1.0/usr/share/NVDARemoteServer
cp ../manual/NVDARemoteServer.1 nvda-remote-server_1.0/usr/share/man/man1
#compress manual
gzip -9 nvda-remote-server_1.0/usr/share/man/man1/NVDARemoteServer.1
#change permissions
chown -R root nvda-remote-server_1.0
chgrp -R root nvda-remote-server_1.0
chmod -R 755 nvda-remote-server_1.0
chmod 644 nvda-remote-server_1.0/DEBIAN/control
chmod -x nvda-remote-server_1.0/usr/share/NVDARemoteServer/server.py
chmod -x nvda-remote-server_1.0/usr/share/NVDARemoteServer/server.pem
chmod -x nvda-remote-server_1.0/usr/share/NVDARemoteServer/daemon.py
chmod -x nvda-remote-server_1.0/usr/share/doc/nvda-remote-server/copyright
chmod -x nvda-remote-server_1.0/usr/share/man/man1/NVDARemoteServer.1.gz
chmod -x nvda-remote-server_1.0/usr/share/doc/nvda-remote-server/changelog.Debian.gz
chmod -x nvda-remote-server_1.0/lib/systemd/system/NVDARemoteServer.service
#build the package
dpkg-deb --build nvda-remote-server_1.0
