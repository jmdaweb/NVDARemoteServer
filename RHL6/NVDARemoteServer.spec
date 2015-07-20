Name: NVDARemoteServer
Version: 1
Release: 0
Summary: NVDARemote server rpm
Source0: server.tar.gz
License: GPL
Requires: python
Group: Rahul
BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-buildroot
%description
This remote server allows NVDARemote users to redirect their traffic.
%prep
%setup -q
%build
%install
install -m 0755 -d $RPM_BUILD_ROOT/usr/share/NVDARemoteServer
install -m 0755 -d $RPM_BUILD_ROOT/usr/bin
install -m 0755 -d $RPM_BUILD_ROOT/etc/init.d
install -m 0644 server.py $RPM_BUILD_ROOT/usr/share/NVDARemoteServer/server.py
install -m 0644 server.pem $RPM_BUILD_ROOT/usr/share/NVDARemoteServer/server.pem
install -m 0644 daemon.py $RPM_BUILD_ROOT/usr/share/NVDARemoteServer/daemon.py
install -m 0755 NVDARemoteServer $RPM_BUILD_ROOT/usr/bin/NVDARemoteServer
install -m 0755 NVDARemoteServerd $RPM_BUILD_ROOT/etc/init.d/NVDARemoteServer
%clean
rm -rf $RPM_BUILD_ROOT
%post
%files
/etc/init.d/NVDARemoteServer
/usr/bin/NVDARemoteServer
%dir /usr/share/NVDARemoteServer
/usr/share/NVDARemoteServer/server.py
/usr/share/NVDARemoteServer/server.pyc
/usr/share/NVDARemoteServer/server.pyo
/usr/share/NVDARemoteServer/server.pem
/usr/share/NVDARemoteServer/daemon.py
/usr/share/NVDARemoteServer/daemon.pyc
/usr/share/NVDARemoteServer/daemon.pyo
