#!/bin/bash
mkdir -p src/usr/share/NVDARemoteServer
mkdir -p src/usr/share/man/man1
mkdir -p src/usr/share/man/man5
mkdir -p src/etc
mkdir pkg
cp ../server.py ../options.py ../server.pem ../daemon.py src/usr/share/NVDARemoteServer
cp ../NVDARemoteCertificate ../NVDARemoteCertificate-letsencrypt src/usr/bin
cp ../manual/NVDARemoteServer.1 ../manual/NVDARemoteCertificate.1 ../manual/NVDARemoteCertificate-letsencrypt.1 src/usr/share/man/man1
cp ../manual/NVDARemoteServer.conf.5 src/usr/share/man/man5
cp ../NVDARemoteServer.conf src/etc
makepkg
rm -rf pkg
