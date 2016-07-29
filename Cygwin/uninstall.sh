#!/bin/bash
echo Uninstalling NVDA Remote Server...
rm -rf /usr/share/NVDARemoteServer
rm -rf /usr/share/doc/NVDARemoteServer
rm -f /usr/bin/NVDARemoteServer /usr/bin/NVDARemoteCertificate /usr/bin/NVDARemoteUninstall /usr/share/man/man1/NVDARemoteServer.1 /usr/share/man/man1/NVDARemoteCertificate /var/log/NVDARemoteServer.log
echo NVDA Remote Server has been uninstalled.
exit 0