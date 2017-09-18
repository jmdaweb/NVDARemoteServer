# NVDA Remote Relay server

A free and open source relay server for NVDA Remote

## Introduction

The NVDA Remote Relay server is a multiplatform, free and open source server for NVDA Remote. It has the same functionality as the official NVDA Remote server (nvdaremote.com, allinaccess.com), but you can install and use it anywhere!

Do you want to control several computers located inside your home from outside? You can't forward the tcp port 6837 for all of them, so this server is for you.

This server is multiplatform, so you can install it under Windows, Mac and many Linux distributions, including Arch, Debian and Centos. If you have installed python 2.x on your system, probably you will be able to run this server.

## Building

Building NVDA Remote Relay server is very easy. On most platforms, you only need to run the build.sh script corresponding to your platform, and install the generated package after that.

### Building for debian based distributions

1. Navigate to the debian directory inside this repo (choose between Debian 7 or Debian 8). If you run Debian versions later than Debian 8, or Ubuntu 15.04 and later, the Debian 8 package is what you need.
2. Ensure that the build.sh script can be executed: chmod +x build.sh
3. Run the script: sudo ./build.sh
4. Install the package: sudo dpkg -i NVDARemoteServer.deb

To uninstall it, run sudo dpkg --purge nvda-remote-server

To uninstall it keeping the configuration files, run sudo dpkg --remove nvda-remote-server

### Building for Centos and RHL based distributions

You must choose between Centos 6 (RHL6 folder) or Centos 7 (RHL 7). Follow the instructions included in that folders. Finally, install the package using rpm: rpm -U NVDARemoteServer.rpm

To uninstall it, run sudo rpm -e NVDARemoteServer

### Building for Mac Os x

1. Navigate to the Mac Os x directory inside this repo.
2. Ensure that the build.sh script can be executed: chmod +x build.sh
3. Run the script: sudo ./build.sh
4. Install the generated package using Finder or the terminal. Remember to allow untrusted software installation in System preferences > Security and privacy. To install from the terminal, run the following command: sudo installer -pkg NVDARemoteServer.pkg -target /

To uninstall it, run sudo NVDARemoteUninstall

### Building for Arch based distributions

1. Navigate to the Arch directory inside this repo.
2. Ensure that the build.sh script can be executed: chmod +x build.sh
3. Run the script without root privileges: ./build.sh
4. Install the package with pacman: sudo pacman -U NVDARemoteServer.pkg.tar.xz.

To uninstall it, run: sudo pacman --remove NVDARemoteServer

### Building for MSYS2 platform on Windows

1. Navigate to the MSYS directory inside this repo.
2. Repeat steps 3 and 4 from arch section.

### Installing on Cygwin

1. Navigate to the Cygwin directory from Cygwin Bash shell.
2. Run install.sh: ./install.sh

To uninstall it, run NVDARemoteUninstall

### Building for Windows

You only need Python 2.7.x and the pywin32 and py2exe packages. Open a command prompt and navigate to the root folder of this repository, then run:

python setup_windows.py py2exe

The binaries will be placed in the dist folder.

The server is almost portable, there is no installation required. If you install the Windows service, remember uninstalling it before moving the server to another location or removing it.

### Building for Windows x64

You need Python 2.7.x for x64 installed and the pywin32 and py2exe packages. The steps are the same for Windows x86 and x64.

### Building the Docker image

You need Docker installed on a Linux system. Navigate to the docker directory and run:

docker build -t nvda-remote-server .

Change or add more tags if you plan to push the image to a Docker registry.

## Running

Before you start, check that the tcp port 6837 is allowed through your firewall.

On Unix platforms, including Mac Os x, there is a script located in /usr/bin called NVDARemoteServer. You can run this script without parameters to get a short help message.

If you want to start the server in debugging mode (useful to see activity and errors) run:

sudo NVDARemoteServer debug

On most platforms, you can stop the server by pressing ctrl+c if it is running in this mode.

To start the server, run:

sudo NVDARemoteServer start

To stop it, run:

sudo NVDARemoteServer stop

Run sudo NVDARemoteServer restart to restart the server.

If the server freezes, run sudo NVDARemoteServer kill to kill the process.

On Centos 6, Centos 7, Arch and Debian based distributions, the NVDA Remote Relay server is also installed as a service, so you can configure it to run at system startup, and manage it with the service and systemctl utilities. You can run NVDARemoteServer status to see if the service is running.

If you want to configure the service to run at system startup, run sudo NVDARemoteServer enable. Run sudo NVDARemoteServer disable to configure the service to start manually.

The procedure to run the server on Windows is different. There is an executable in the dist folder that you can run to start the server in console mode. To stop, simply close the console window or kill the process.

If you want to install the server as a system service, run service_manager.cmd as administrator and choose the right options on the displayed menu.

Run debug.cmd to start the server in debugging mode.

If you want to run the server inside a Docker container, use a command similar to the following:

docker run -d -p 6837:6837 --name my_nvda_remote jmdaweb/nvda-remote-server:latest

You can change jmdaweb/nvda-remote-server:latest to your custom image name if you have built it. The --name argument specifies the container name. If you want to use a diferent port, change the first part after -p. The second must be always 6837.

## Log files

Do you run the server in production mode and it suddenly is stopped? Now you can look at the following files:

On Linux and Mac Os x: go to /var/log/NVDARemoteServer.log

On Windows: NVDARemoteServer.log is located inside the program folder.

On a Docker container: run docker logs containername. For example: docker logs my_nvda_remote

Read the Docker documentation to see all available commands.

## Creating your own self-signed certificate

The server includes a default self-signed certificate to encrypt connections. This certificate is also included in the official NVDA Remote add-on, so this is a big security risk.

It is strongly recommended that you create your own certificate before starting the server for the first time. You can do it by running the NVDARemoteCertificate script on almost all platforms:

sudo NVDARemoteCertificate

The script takes no arguments. Follow the on-screen instructions to complete the process.

The script will create a 4096 bit RSA private key and a certificate, and combine them in a single server.pem file. Once finished, if the server is running, restart it.

On Windows, a pre-built OpenSSL version is included in the server directory. You can run NVDARemoteCertificate.cmd to create a certificate.

## Configuration file and extra commandline options

Starting with version 1.5, NVDARemoteServer includes a configuration file that you can modify to change some server settings. You must restart the server after modifying this file. The comments in the file will guide you when changing settings.

You can test your changes in debugging mode before modifying the configuration file. Although the changes in the configuration also are applied when you run the server in debug mode, you can pass some commandline parameters to perform tests. The following options are available:

* --interface=ip: listen only on the specified ip address. This setting doesn't affect IPV6 interfaces. In some platforms, this setting will not work if IPV6 socket binds to all interfaces.
* --interface6=ip: listen only on the specified IPV6 address. This setting doesn't affect IPV4 interfaces.
* --port=port: listen only on the specified tcp port.
* --logfile=path, --pidfile=path: these parameters are available, but unuseful in debug mode. You can use them on init.d and systemd units, but it's not recommended. Use --configfile instead.
* --configfile=path: read config file from path. All the previous options can be edited in the configuration file.
* --loglevel=n, where n is a number between 0 (almost quiet) and 3 (very verbose).
* --pemfile=path: path to the private key and certificate used for ssl connections. They must be in the same file.

Note: the command line arguments take precedence over the supplied ones in the configuration file.

## Known problems

### Installing on Mac os x El Capitan and later

Mac os x El Capitan adds a new feature called system integrity protection to prevent malware from modifying system files. If this feature is enabled, you won't be able to install NVDA Remote Server on your Mac.

If you want to disable it, follow these steps:

* Reboot your system. While rebooting, hold the command+r key to enter in recovery mode.
* Go to the utilities menu, and choose terminal.
* Type the following command: csrutil disable
* Reboot your system and go back to the main operating system.
* Install NVDA Remote Server.

Caution! Disabling system integrity protection is a security risk. To enable it back, run csrutil enable in recovery mode.

### Problems with the server in OpenVZ or Docker containers

If you run a Debian 8 or RHL 7 based OpenVZ or Docker container, don't install the Debian 8 or RHL 7 packages. They will fail and leave the installation in a bad state. In these containers, Systemd produces errors because it can't connect directly to the kernel.

Solution: install Debian 7 or RHL 6 package instead, or run systemd in a privileged container.

