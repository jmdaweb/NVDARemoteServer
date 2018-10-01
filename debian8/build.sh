#!/bin/bash
#please, run this script as root
#make directories
VERSION=1.8
mkdir -p nvda-remote-server_$VERSION/usr/bin
mkdir -p nvda-remote-server_$VERSION/usr/share/doc/nvda-remote-server
mkdir -p nvda-remote-server_$VERSION/usr/share/NVDARemoteServer
mkdir -p nvda-remote-server_$VERSION/usr/share/man/man1
mkdir -p nvda-remote-server_$VERSION/usr/share/man/man5
mkdir -p nvda-remote-server_$VERSION/etc
mkdir -p nvda-remote-server_$VERSION/lib/systemd/system
mkdir -p nvda-remote-server_$VERSION/usr/lib/tmpfiles.d
#copy files
cp ../NVDARemoteCertificate ../systemd/NVDARemoteServer nvda-remote-server_$VERSION/usr/bin
cp ../NVDARemoteServer.conf nvda-remote-server_$VERSION/etc
cp ../server.py ../options.py ../server.pem ../daemon.py nvda-remote-server_$VERSION/usr/share/NVDARemoteServer
cp ../manual/NVDARemoteServer.1 ../manual/NVDARemoteCertificate.1 nvda-remote-server_$VERSION/usr/share/man/man1
cp ../manual/NVDARemoteServer.conf.5 nvda-remote-server_$VERSION/usr/share/man/man5
cp ../copyright nvda-remote-server_$VERSION/usr/share/doc/nvda-remote-server
cp ../changelog.Debian nvda-remote-server_$VERSION/usr/share/doc/nvda-remote-server
cp ../systemd/NVDARemoteServer.service nvda-remote-server_$VERSION/lib/systemd/system
cp ../systemd/NVDARemoteServer.tmpfiles nvda-remote-server_$VERSION/usr/lib/tmpfiles.d/NVDARemoteServer.conf
#compress manual and changelog
gzip -n -9 nvda-remote-server_$VERSION/usr/share/man/man1/NVDARemoteServer.1
gzip -n -9 nvda-remote-server_$VERSION/usr/share/man/man5/NVDARemoteServer.conf.5
gzip -n -9 nvda-remote-server_$VERSION/usr/share/man/man1/NVDARemoteCertificate.1
gzip -n -9 nvda-remote-server_$VERSION/usr/share/doc/nvda-remote-server/changelog.Debian
#change permissions
chown -R root.root nvda-remote-server_$VERSION
chmod -R 755 nvda-remote-server_$VERSION
chmod 644 nvda-remote-server_$VERSION/DEBIAN/control
chmod 644 nvda-remote-server_$VERSION/DEBIAN/conffiles
chmod -x nvda-remote-server_$VERSION/usr/share/NVDARemoteServer/server.py
chmod -x nvda-remote-server_$VERSION/usr/share/NVDARemoteServer/options.py
chmod -x nvda-remote-server_$VERSION/usr/share/NVDARemoteServer/server.pem
chmod -x nvda-remote-server_$VERSION/usr/share/NVDARemoteServer/daemon.py
chmod -x nvda-remote-server_$VERSION/usr/share/doc/nvda-remote-server/copyright
chmod -x nvda-remote-server_$VERSION/usr/share/man/man1/NVDARemoteServer.1.gz
chmod -x nvda-remote-server_$VERSION/usr/share/man/man5/NVDARemoteServer.conf.5.gz
chmod -x nvda-remote-server_$VERSION/usr/share/man/man1/NVDARemoteCertificate.1.gz
chmod -x nvda-remote-server_$VERSION/usr/share/doc/nvda-remote-server/changelog.Debian.gz
chmod -x nvda-remote-server_$VERSION/lib/systemd/system/NVDARemoteServer.service
chmod -x nvda-remote-server_$VERSION/usr/lib/tmpfiles.d/NVDARemoteServer.conf
chmod -x nvda-remote-server_$VERSION/etc/NVDARemoteServer.conf
sed -i "s/.*=\/var\/run\/NVDARemoteServer.pid.*/pidfile=\/run\/NVDARemoteServer\/NVDARemoteServer.pid/" nvda-remote-server_$VERSION/etc/NVDARemoteServer.conf
#build the package
dpkg-deb --build nvda-remote-server_$VERSION
