Name: NVDARemoteServer
Version: 2.5
Release: 1.generic
Summary: NVDARemote server rpm
Source0: server.tar.gz
License: GPL-2.0-or-later
URL: https://github.com/jmdaweb/NVDARemoteServer
Requires: python3, systemd-sysv, openssl
Group: System Environment/Daemons
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
%description
This remote server allows NVDARemote users to redirect their traffic.
%prep
%setup -q
%build
%install
chmod -x LICENSE
install -m 0755 -d $RPM_BUILD_ROOT/usr/share/NVDARemoteServer
install -m 0755 -d $RPM_BUILD_ROOT/usr/lib/systemd/system
install -m 0755 -d $RPM_BUILD_ROOT/usr/bin
install -m 0755 -d $RPM_BUILD_ROOT/etc
install -m 0755 -d $RPM_BUILD_ROOT/usr/share/man/man1
install -m 0755 -d $RPM_BUILD_ROOT/usr/share/man/man5
install -m 0644 server.py $RPM_BUILD_ROOT/usr/share/NVDARemoteServer/server.py
install -m 0644 options.py $RPM_BUILD_ROOT/usr/share/NVDARemoteServer/options.py
install -m 0644 server.pem $RPM_BUILD_ROOT/usr/share/NVDARemoteServer/server.pem
install -m 0644 daemon.py $RPM_BUILD_ROOT/usr/share/NVDARemoteServer/daemon.py
install -m 0755 NVDARemoteServer $RPM_BUILD_ROOT/usr/bin/NVDARemoteServer
install -m 0755 NVDARemoteCertificate $RPM_BUILD_ROOT/usr/bin/NVDARemoteCertificate
install -m 0755 NVDARemoteCertificate-letsencrypt $RPM_BUILD_ROOT/usr/bin/NVDARemoteCertificate-letsencrypt
install -m 0644 NVDARemoteServer.conf $RPM_BUILD_ROOT/etc/NVDARemoteServer.conf
install -m 0644 NVDARemoteServer.service $RPM_BUILD_ROOT/usr/lib/systemd/system/NVDARemoteServer.service
gzip -n -9 NVDARemoteServer.1
install -m 0644 NVDARemoteServer.1.gz $RPM_BUILD_ROOT/usr/share/man/man1/NVDARemoteServer.1.gz
gzip -n -9 NVDARemoteServer.conf.5
install -m 0644 NVDARemoteServer.conf.5.gz $RPM_BUILD_ROOT/usr/share/man/man5/NVDARemoteServer.conf.5.gz
gzip -n -9 NVDARemoteCertificate.1
install -m 0644 NVDARemoteCertificate.1.gz $RPM_BUILD_ROOT/usr/share/man/man1/NVDARemoteCertificate.1.gz
gzip -n -9 NVDARemoteCertificate-letsencrypt.1
install -m 0644 NVDARemoteCertificate-letsencrypt.1.gz $RPM_BUILD_ROOT/usr/share/man/man1/NVDARemoteCertificate-letsencrypt.1.gz
%clean
rm -rf $RPM_BUILD_ROOT
%post
systemctl daemon-reload
NVDARemoteServer enable
NVDARemoteServer start
%postun
if test -e /run/NVDARemoteServer
then
rm -rf /run/NVDARemoteServer
fi
if test -e /var/log/NVDARemoteServer
then
rm -rf /var/log/NVDARemoteServer
fi
systemctl daemon-reload
%preun
NVDARemoteServer stop
NVDARemoteServer disable
%files
/usr/bin/NVDARemoteServer
/usr/bin/NVDARemoteCertificate
/usr/bin/NVDARemoteCertificate-letsencrypt
%config(noreplace) /etc/NVDARemoteServer.conf
%dir /usr/share/NVDARemoteServer
/usr/share/NVDARemoteServer/server.py
/usr/share/NVDARemoteServer/options.py
/usr/share/NVDARemoteServer/server.pem
/usr/share/NVDARemoteServer/daemon.py
/usr/lib/systemd/system/NVDARemoteServer.service
/usr/share/man/man1/NVDARemoteServer.1.gz
/usr/share/man/man5/NVDARemoteServer.conf.5.gz
/usr/share/man/man1/NVDARemoteCertificate.1.gz
/usr/share/man/man1/NVDARemoteCertificate-letsencrypt.1.gz
%license LICENSE
%changelog
* Tue Aug 12 2025 Jose Manuel Delicado <jm.delicado@nvda.es> - 2.5-1.generic
- Security and stability fixes.
* Mon Dec 16 2024 Jose Manuel Delicado <jm.delicado@nvda.es> - 2.4-1
- Code optimization and other small tweaks.
* Mon Jul 31 2023 Jose Manuel Delicado <jm.delicado@nvda.es> - 2.3-1
- Added a new parameter to specify maximum allowed length for a message.
* Wed Dec 29 2021 Jose Manuel Delicado <jm.delicado@nvda.es> - 2.2-1
- The NVDARemoteCertificate program now allows choosing a private key type.
* Sun Dec 19 2021 Jose Manuel Delicado <jm.delicado@nvda.es> - 2.1-1
- Security enhancements, stability improvements and new settings.
* Mon Nov 30 2020 Jose Manuel Delicado <jm.delicado@nvda.es> - 2.0-1
- Bug fixes.
* Wed Oct 10 2018 Jose Manuel Delicado <jm.delicado@nvda.es> - 1.9-1
- Stability improvements.
* Sat Sep 15 2018 Jose Manuel Delicado <jm.delicado@nvda.es> - 1.8-1
- Stability and performance improvements
* Sat Sep 01 2018 Jose Manuel Delicado <jm.delicado@nvda.es> - 1.7-1
- Added compatibility with Python 3. Added message of the day.
* Fri Oct 06 2017 Jose Manuel Delicado <jmdaweb@hotmail.com> - 1.6-1
- Added IPV6 support and more options
* Sat Sep 09 2017 Jose Manuel Delicado <jmdaweb@hotmail.com> - 1.5-1
- Added options module and a separate thread for loggin.
* Wed Jul 19 2017 Jose Manuel Delicado <jmdaweb@hotmail.com> - 1.4.2-1
- Fixed CPU usage eficiency problem.
* Wed Mar 01 2017 Jose Manuel Delicado <jmdaweb@hotmail.com> - 1.4.1-1
- Fixed massive memory allocation problem.
* Sat Jan 14 2017 Jose Manuel Delicado <jmdaweb@hotmail.com> - 1.4-1
- The server is now threaded. Support for more platforms and protocol v2.
* Mon Apr 4 2016 Technow <info@technow.es> - 1.3-1
- Bugs fixed. New utility to generate server certificates.
* Mon Mar 21 2016 Technow <info@technow.es> - 1.2-1
- Security and stability improvements
* Thu Feb 25 2016 Technow <info@technow.es> - 1.1-1
- Fixed lots of bugs
* Tue Jul 21 2015 Technow <info@technow.es> - 1.0-1
 - First release
