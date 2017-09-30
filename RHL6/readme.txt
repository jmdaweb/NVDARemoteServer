This package can't be safely built in an automatic way, so you have to build it manually. Follow these steps, and respect the filenames. They aren't an example.
1. If you haven't installed it yet, install the rpmdevtools package using yum.
2. Go to your home folder and call rpmdev-setuptree to create the required directory structure.
3. Copy NVDARemoteServer.spec into ~rpmbuild/SPECS
4. Copy daemon.py, server.py, options.py, NVDARemoteServer.conf, LICENSE, NVDARemoteServer, NVDARemoteServer.1 (manual), NVDARemoteServer.conf.5 (manual), NVDARemoteCertificate.1 (manual), NVDARemoteCertificate, NVDARemoteServerd and server.pem into ~/rpmbuild/SOURCES/NVDARemoteServer-1.6, creating the directory if it doesn't exist
5. Navigate to the SOURCES directory, and tar the NVDARemoteServer-1.6 folder: tar -czf server.tar.gz NVDARemoteServer-1.6
6. Go back to the ~/rpmbuild, and run: rpmbuild -ba SPECS/NVDARemoteServer.spec
7. You will find the rpm file in ~/rpmbuild/RPMS/noarch
Enjoy!