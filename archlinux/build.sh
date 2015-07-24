#!/bin/bash
mkdir -p src/usr/share/NVDARemoteServer
mkdir -p src/usr/share/man/man1
mkdir pkg
cp ../server.py ../server.pem ../daemon.py src/usr/share/NVDARemoteServer
cp ../manual/NVDARemoteServer.1 src/usr/share/man/man1
makepkg
