#!/bin/bash
mkdir -p src/etc
mkdir -p src/usr/bin
mkdir -p src/usr/share/NVDARemoteServer
mkdir -p src/usr/share/man/man1
mkdir -p src/usr/share/man/man5
mkdir -p src/usr/lib/sysusers.d
mkdir -p src/usr/lib/tmpfiles.d
mkdir -p src/usr/lib/systemd/system
mkdir pkg
cp ../server.py ../options.py ../server.pem ../daemon.py src/usr/share/NVDARemoteServer
cp ../NVDARemoteCertificate ../systemd/NVDARemoteServer src/usr/bin
chmod +x src/usr/bin/NVDARemoteServer
chmod +x src/usr/bin/NVDARemoteCertificate
cp ../NVDARemoteServer.conf src/etc
cp ../manual/NVDARemoteServer.1 ../manual/NVDARemoteCertificate.1 src/usr/share/man/man1
cp ../manual/NVDARemoteServer.conf.5 src/usr/share/man/man5
cp ../systemd/NVDARemoteServer.tmpfiles src/usr/lib/tmpfiles.d/NVDARemoteServer.conf
cp ../systemd/NVDARemoteServer.sysusers src/usr/lib/sysusers.d/NVDARemoteServer.conf
cp ../systemd/NVDARemoteServer.service src/usr/lib/systemd/system
makepkg
