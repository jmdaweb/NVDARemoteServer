#!/bin/bash
mkdir -p src/etc
mkdir -p src/usr/share/NVDARemoteServer
mkdir -p src/usr/share/man/man1
mkdir pkg
cp ../server.py ../options.py ../server.pem ../daemon.py src/usr/share/NVDARemoteServer
cp ../NVDARemoteCertificate src/usr/bin
cp ../NVDARemoteServer.conf src/etc
cp ../manual/NVDARemoteServer.1 ../manual/NVDARemoteCertificate.1 src/usr/share/man/man1
makepkg
