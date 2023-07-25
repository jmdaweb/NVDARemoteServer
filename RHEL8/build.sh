#!/bin/bash
VERSION=2.3
CURDIR=$PWD
if ! test -e ~/rpmbuild
then
cd ~
rpmdev-setuptree
cd $CURDIR
fi
if ! test -e ~/rpmbuild/SOURCES/NVDARemoteServer-$VERSION
then
mkdir -p ~/rpmbuild/SOURCES/NVDARemoteServer-$VERSION
fi
if ! test -e ~/rpmbuild/SPECS
then
mkdir -p ~/rpmbuild/SPECS
fi
cp NVDARemoteServer.spec ~/rpmbuild/SPECS
cp ../systemd/NVDARemoteServer.sysusers ../systemd/NVDARemoteServer.tmpfiles ../*.py ../*.pem ../LICENSE ../manual/* ../*.conf ../NVDARemoteCertificate ~/rpmbuild/SOURCES/NVDARemoteServer-$VERSION
cp NVDARemoteServer NVDARemoteServer.service ~/rpmbuild/SOURCES/NVDARemoteServer-$VERSION
cd ~/rpmbuild/SOURCES
sed -i "s/.*=\/var\/run\/NVDARemoteServer.pid.*/pidfile=\/run\/NVDARemoteServer\/NVDARemoteServer.pid/" NVDARemoteServer-$VERSION/NVDARemoteServer.conf
tar -czf server.tar.gz NVDARemoteServer-$VERSION
cd ..
rpmbuild -ba SPECS/NVDARemoteServer.spec
