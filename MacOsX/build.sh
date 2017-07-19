#!/bin/bash
mkdir -p package/usr/bin
mkdir -p package/usr/share/NVDARemoteServer
mkdir -p package/usr/share/man/man1
cp ../server.py ../daemon.py ../server.pem package/usr/share/NVDARemoteServer
cp NVDARemoteServer ../NVDARemoteCertificate package/usr/bin
cp ../manual/NVDARemoteServer.1 ../manual/NVDARemoteCertificate.1 package/usr/share/man/man1
gzip -n -9 package/usr/share/man/man1/NVDARemoteServer.1
gzip -n -9 package/usr/share/man/man1/NVDARemoteCertificate.1
chmod +x package/usr/bin/NVDARemoteServer
chmod +x package/usr/bin/NVDARemoteCertificate
pkgbuild --identifier NVDARemoteServer --version 1.4.2 --install-location / --root package NVDARemoteServer.pkg