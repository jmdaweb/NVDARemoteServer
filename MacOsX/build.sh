#!/bin/bash
mkdir -p package/usr/bin
mkdir -p package/usr/share/NVDARemoteServer
cp ../server.py ../daemon.py ../server.pem package/usr/share/NVDARemoteServer
cp NVDARemoteServer package/usr/bin
chmod +x package/usr/bin/NVDARemoteServer
pkgbuild --identifier NVDARemoteServer --version 1.1 --install-location / --root package NVDARemoteServer.pkg