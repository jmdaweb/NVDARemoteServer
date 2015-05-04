#!/bin/bash
mkdir -p src/usr/share/NVDARemoteServer
mkdir pkg
cp ../server.py ../server.pem ../daemon.py src/usr/share/NVDARemoteServer
makepkg
