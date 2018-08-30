#!/bin/bash
VERSION=1.7
mkdir -p package/usr/bin
mkdir -p package/etc
mkdir -p package/usr/share/NVDARemoteServer
mkdir -p package/usr/share/man/man1
mkdir -p package/usr/share/man/man5
cp ../server.py ../daemon.py ../options.py ../server.pem package/usr/share/NVDARemoteServer
cp NVDARemoteServer ../NVDARemoteCertificate package/usr/bin
cp uninstall.sh package/usr/bin/NVDARemoteUninstall
cp ../NVDARemoteServer.conf package/etc
cp ../manual/NVDARemoteServer.1 ../manual/NVDARemoteUninstall.1 ../manual/NVDARemoteCertificate.1 package/usr/share/man/man1
cp ../manual/NVDARemoteServer.conf.5 package/usr/share/man/man5
gzip -n -9 package/usr/share/man/man1/NVDARemoteServer.1
gzip -n -9 package/usr/share/man/man1/NVDARemoteUninstall.1
gzip -n -9 package/usr/share/man/man1/NVDARemoteCertificate.1
gzip -n -9 package/usr/share/man/man5/NVDARemoteServer.conf.5
chmod +x package/usr/bin/NVDARemoteServer
chmod +x package/usr/bin/NVDARemoteCertificate
chmod +x package/usr/bin/NVDARemoteUninstall
pkgbuild --identifier NVDARemoteServer --version $VERSION --install-location / --root package NVDARemoteServer.pkg