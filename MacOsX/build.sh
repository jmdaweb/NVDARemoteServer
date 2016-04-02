#!/bin/bash
mkdir -p package/usr/bin
mkdir -p package/usr/share/NVDARemoteServer
cp ../server.py ../daemon.py ../server.pem package/usr/share/NVDARemoteServer
cp NVDARemoteServer ../NVDARemoteCertificate package/usr/bin
chmod +x package/usr/bin/NVDARemoteServer
chmod +x package/usr/bin/NVDARemoteCertificate
pkgbuild --identifier NVDARemoteServer --version 1.3 --install-location / --root package NVDARemoteServer.pkg