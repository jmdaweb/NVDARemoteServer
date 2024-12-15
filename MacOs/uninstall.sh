#!/bin/bash
if test -e /var/run/NVDARemoteServer.pid
then
echo Stopping server...
NVDARemoteServer stop
fi
echo Uninstalling NVDA Remote Server...
rm -rf /usr/share/NVDARemoteServer
rm -rf /usr/share/doc/NVDARemoteServer
rm -f /usr/bin/NVDARemoteServer /usr/bin/NVDARemoteCertificate /usr/bin/NVDARemoteCertificate-letsencrypt /usr/bin/NVDARemoteUninstall /usr/share/man/man1/NVDARemoteServer.1.gz /usr/share/man/man1/NVDARemoteUninstall.1.gz /usr/share/man/man1/NVDARemoteCertificate.1.gz /var/log/NVDARemoteServer.log /etc/NVDARemoteServer.conf /usr/share/man/man5/NVDARemoteServer.conf.5.gz
pkgutil --forget NVDARemoteServer
echo NVDA Remote Server has been uninstalled.
exit 0