#!/bin/bash
VERSION=2.4
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
cp ../*.py ../*.pem ../LICENSE ../manual/* ../*.conf ../NVDARemoteCertificate ../NVDARemoteCertificate-letsencrypt ~/rpmbuild/SOURCES/NVDARemoteServer-$VERSION
cp NVDARemoteServer NVDARemoteServer.service ~/rpmbuild/SOURCES/NVDARemoteServer-$VERSION
cd ~/rpmbuild/SOURCES
tar -czf server.tar.gz NVDARemoteServer-$VERSION
cd ..
rpmbuild -ba SPECS/NVDARemoteServer.spec
