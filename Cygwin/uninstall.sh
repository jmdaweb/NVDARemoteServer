#!/bin/bash
echo Uninstalling NVDA Remote Server...
rm -rf /usr/share/NVDARemoteServer
rm -rf /usr/share/doc/NVDARemoteServer
rm -rf /usr/bin/NVDARemoteServer /usr/bin/NVDARemoteCertificate /usr/bin/NVDARemoteCertificate-letsencrypt /usr/bin/NVDARemoteUninstall /usr/share/man/man1/NVDARemoteServer.1 /usr/share/man/man1/NVDARemoteUninstall.1 /usr/share/man/man1/NVDARemoteCertificate.1 /var/log/NVDARemoteServer /etc/NVDARemoteServer.conf /usr/share/man/man5/NVDARemoteServer.conf.5
echo NVDA Remote Server has been uninstalled.
exit 0