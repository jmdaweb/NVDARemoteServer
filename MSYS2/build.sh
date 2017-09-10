#!/bin/bash
mkdir -p src/usr/share/NVDARemoteServer
mkdir -p src/usr/share/man/man1
mkdir -p src/etc
mkdir pkg
cp ../server.py ../options.py ../server.pem ../daemon.py src/usr/share/NVDARemoteServer
cp ../NVDARemoteCertificate src/usr/bin
cp ../manual/NVDARemoteServer.1 ../manual/NVDARemoteCertificate.1 src/usr/share/man/man1
cp ../NVDARemoteServer.conf src/etc
makepkg
