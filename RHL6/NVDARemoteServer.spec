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
install -m 0755 server.py $RPM_BUILD_ROOT/usr/share/NVDARemoteServer/server.py
install -m 0755 server.pem $RPM_BUILD_ROOT/usr/share/NVDARemoteServer/server.pem
install -m 0755 daemon.py $RPM_BUILD_ROOT/usr/share/NVDARemoteServer/daemon.py
install -m 0755 NVDARemoteServer $RPM_BUILD_ROOT/usr/bin/NVDARemoteServer
%clean
rm -rf $RPM_BUILD_ROOT
%post
ln -s /usr/bin/NVDARemoteServer /etc/init.d/NVDARemoteServer
%files
/usr/bin/NVDARemoteServer
%dir /usr/share/NVDARemoteServer
/usr/share/NVDARemoteServer/server.py
/usr/share/NVDARemoteServer/server.pem
/usr/share/NVDARemoteServer/daemon.py
