Name: NVDARemoteServer
Version: 1
Release: 0
Summary: NVDARemote server rpm
Source0: server.tar.gz
License: GPLv2
URL: http://remote.technow.es
Requires: python
Group: System Environment/Daemons
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
%description
This remote server allows NVDARemote users to redirect their traffic.
%prep
%setup -q
%build
%install
install -m 0755 -d $RPM_BUILD_ROOT/usr/share/NVDARemoteServer
install -m 0755 -d $RPM_BUILD_ROOT/usr/lib/systemd/system
install -m 0755 -d $RPM_BUILD_ROOT/usr/bin
install -m 0644 server.py $RPM_BUILD_ROOT/usr/share/NVDARemoteServer/server.py
install -m 0644 server.pem $RPM_BUILD_ROOT/usr/share/NVDARemoteServer/server.pem
install -m 0644 daemon.py $RPM_BUILD_ROOT/usr/share/NVDARemoteServer/daemon.py
install -m 0755 NVDARemoteServer $RPM_BUILD_ROOT/usr/bin/NVDARemoteServer
install -m 0644 NVDARemoteServer.service $RPM_BUILD_ROOT/usr/lib/systemd/system/NVDARemoteServer.service
%clean
rm -rf $RPM_BUILD_ROOT
%post
%files
/usr/bin/NVDARemoteServer
%dir /usr/share/NVDARemoteServer
/usr/share/NVDARemoteServer/server.py
/usr/share/NVDARemoteServer/server.pyc
/usr/share/NVDARemoteServer/server.pyo
/usr/share/NVDARemoteServer/server.pem
/usr/share/NVDARemoteServer/daemon.py
/usr/share/NVDARemoteServer/daemon.pyc
/usr/share/NVDARemoteServer/daemon.pyo
/usr/lib/systemd/system/NVDARemoteServer.service
