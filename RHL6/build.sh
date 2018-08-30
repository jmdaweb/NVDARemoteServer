#!/bin/bash
CURDIR=$PWD
if ! test -e ~/rpmbuild
then
cd ~
rpmdev-setuptree
cd $CURDIR
fi
if ! test -e ~/rpmbuild/SOURCES/NVDARemoteServer-1.7
then
mkdir -p ~/rpmbuild/SOURCES/NVDARemoteServer-1.7
fi
if ! test -e ~/rpmbuild/SPECS
then
mkdir -p ~/rpmbuild/SPECS
fi
cp NVDARemoteServer NVDARemoteServerd ../*.py ../*.pem ../LICENSE ../manual/* ../*.conf ../NVDARemoteCertificate ~/rpmbuild/SOURCES/NVDARemoteServer-1.7
cd ~/rpmbuild/SOURCES
tar -czf server.tar.gz NVDARemoteServer-1.7
cd ..
rpmbuild -ba SPECS/NVDARemoteServer.spec
