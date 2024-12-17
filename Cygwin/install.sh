#!/bin/bash
if ! test -e ../server.py
then
echo This script must be run from Cygwin directory inside the NVDA Remote Server source folder. Exiting.
exit 1
fi
if test -e /usr/bin/NVDARemoteServer
then
echo NVDA Remote Server is already installed. Exiting...
exit 1
fi
echo installing...
cp NVDARemoteServer /usr/bin
cp uninstall.sh /usr/bin/NVDARemoteUninstall
cp ../NVDARemoteCertificate ../NVDARemoteCertificate-letsencrypt /usr/bin
mkdir /usr/share/NVDARemoteServer
cp ../server.py ../daemon.py ../options.py ../server.pem /usr/share/NVDARemoteServer
cp ../manual/NVDARemoteServer.1 ../manual/NVDARemoteCertificate.1 ../manual/NVDARemoteUninstall.1 ../manual/NVDARemoteCertificate-letsencrypt.1 /usr/share/man/man1
cp ../manual/NVDARemoteServer.conf.5 /usr/share/man/man5
mkdir /usr/share/doc/NVDARemoteServer
cp ../LICENSE /usr/share/doc/NVDARemoteServer
cp ../NVDARemoteServer.conf /etc
if test $? -eq 0
then
echo NVDA Remote Server has been installed succesfully.
exit 0
else
echo There was a problem installing NVDA Remote Server. Please, run the uninstall script and try again.
exit 1
fi
