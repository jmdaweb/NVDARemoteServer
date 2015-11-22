#NVDA Remote Relay server
A free and open source relay server for NVDA Remote

##introduction

The NVDA Remote Relay server is a multiplatform, free and open source server for NVDA Remote. It has the same functionality as the official NVDA Remote server (nvdaremote.com, allinaccess.com), but you can install and use it anywhere!
Do you want to control several computers located inside your home from outside? You can't forward the tcp port 6837 for all of them, so this server is for you.
This server is multiplatform, so you can install it under Windows, Mac and many Linux distributions, including Arch, Debian and Centos. If you have installed python 2.x on your system, probably you will be able to run this server.

##building

Building NVDA Remote Relay server is very easy. On most platforms, you only need to run the build.sh script corresponding to your platform, and install the generated package after that.

###Building for debian based distributions

1. Navigate to the debian directory inside this repo.

2. Ensure that the build.sh script can be executed: chmod +x build.sh

3. Run the script: sudo ./build.sh

4. Install the package: sudo dpkg -i NVDARemoteServer.deb

###Building for Centos and RHL based distributions

You must choose between Centos 6 (RHL6 folder) or Centos 7 (RHL 7). Follow the instructions included in that folders. Finally, install the package using rpm: rpm -U NVDARemoteServer.rpm

###Building for Mac Os x

1. Navigate to the Mac Os x directory inside this repo.

2. Ensure that the build.sh script can be executed: chmod +x build.sh

3. Run the script: ./build.sh

4. Install the generated package using Finder or the terminal.

###Building for Arch based distributions

1. Navigate to the Arch directory inside this repo.

2. Ensure that the build.sh script can be executed: chmod +x build.sh

3. Run the script: ./build.sh

4. Install the package with pacman: pacman -U NVDARemoteServer.pkg.tar.xz

###Building for Windows

You only need Python 2.7.x and the pywin32 and py2exe packages. Open a command prompt and navigate to the root folder of this repository, then run:
python setup_windows.py py2exe
The binaries will be placed in the dist folder.

###Building for Windows x64

You need Python 2.7.x for x64 installed and the pywin32 and py2exe packages. The steps are the same for Windows x86 and x64.

##Running

Before you start, check that the tcp port 6837 is allowed through your firewall.
If you want to start the server in debugging mode (useful to see activity and errors) run:
NVDARemoteServer debug
On Unix platforms, including Mac Os x, there is a script located in /usr/bin called NVDARemoteServer. You can run this script without parameters to get a short help message. To start the server, run:
NVDARemoteServer start
To stop it, run:
NVDARemoteServer stop
Run NVDARemoteServer restart to restart the server.
If the server freezes, run NVDARemoteServer kill to kill the process.
On Centos 6, Centos 7, Arch and Debian based distributions, the NVDA Remote Relay server is also installed as a service, so you can configure it to run at system startup, and manage it with the service and systemctl utilities. Remember to run these commands with sudo if you are an unprivileged user. You can run NVDARemoteServer status to see if the service is running.
If you want to configure the service to run at system startup, run NVDARemoteServer enable
The procedure to run the server on Windows is different. There is an executable in the dist folder that you can run to start the server in console mode. To stop, simply close the console window or kill the process.
If you want to install the server as a system service, run service_manager.cmd as administrator and choose the right options on the displayed menu.
Run debug.cmd to start the server in debugging mode.

##Log files
Do you run the server in production mode and it suddenly is stopped? Now you can look at the following files:
On Linux and Mac Os x: go to /var/log/NVDARemoteServer.log
On Windows: NVDARemoteServer.log is located inside the program folder.

##known problems

There aren't known problems at this time.
