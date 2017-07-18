#!/bin/bash
#please, run this script as root
#make directories
mkdir -p nvda-remote-server_1.4.1/usr/share/doc/nvda-remote-server
mkdir -p nvda-remote-server_1.4.1/usr/share/NVDARemoteServer
mkdir -p nvda-remote-server_1.4.1/usr/share/man/man1
#copy files
cp ../NVDARemoteCertificate nvda-remote-server_1.4.1/usr/bin
cp ../server.py ../server.pem ../daemon.py nvda-remote-server_1.4.1/usr/share/NVDARemoteServer
cp ../manual/NVDARemoteServer.1 ../manual/NVDARemoteCertificate.1 nvda-remote-server_1.4.1/usr/share/man/man1
cp ../copyright nvda-remote-server_1.4.1/usr/share/doc/nvda-remote-server
cp ../changelog.Debian nvda-remote-server_1.4.1/usr/share/doc/nvda-remote-server
#compress manual and changelog
gzip -n -9 nvda-remote-server_1.4.1/usr/share/man/man1/NVDARemoteServer.1
gzip -n -9 nvda-remote-server_1.4.1/usr/share/man/man1/NVDARemoteCertificate.1
gzip -n -9 nvda-remote-server_1.4.1/usr/share/doc/nvda-remote-server/changelog.Debian
#change permissions
chown -R root.root nvda-remote-server_1.4.1
chmod -R 755 nvda-remote-server_1.4.1
chmod 644 nvda-remote-server_1.4.1/DEBIAN/control
chmod -x nvda-remote-server_1.4.1/usr/share/NVDARemoteServer/server.py
chmod -x nvda-remote-server_1.4.1/usr/share/NVDARemoteServer/server.pem
chmod -x nvda-remote-server_1.4.1/usr/share/NVDARemoteServer/daemon.py
chmod -x nvda-remote-server_1.4.1/usr/share/doc/nvda-remote-server/copyright
chmod -x nvda-remote-server_1.4.1/usr/share/man/man1/NVDARemoteServer.1.gz
chmod -x nvda-remote-server_1.4.1/usr/share/man/man1/NVDARemoteCertificate.1.gz
chmod -x nvda-remote-server_1.4.1/usr/share/doc/nvda-remote-server/changelog.Debian.gz
chmod -x nvda-remote-server_1.4.1/lib/systemd/system/NVDARemoteServer.service
#build the package
dpkg-deb --build nvda-remote-server_1.4.1
