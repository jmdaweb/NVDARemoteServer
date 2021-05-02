# NVDA Remote Relay server

A free and open source relay server for NVDA Remote

## Introduction

The NVDA Remote Relay server is a multiplatform, free and open source server for NVDA Remote. It has the same functionality as the official NVDA Remote server (nvdaremote.com, allinaccess.com), but you can install and use it anywhere!

Do you want to control several computers located inside your home from outside? You can't forward the tcp port 6837 for all of them, so this server is for you.

This server is multiplatform, so you can install it under Windows, Mac and many Linux distributions, including Arch, Debian and Centos. If you have installed python 2.x or 3.x on your system, probably you will be able to run this server.

## Building

Building NVDA Remote Relay server is very easy. On most platforms, you only need to run the build.sh script corresponding to your platform, and install the generated package after that. Unless otherwise specified, you should clone this repository and run all commands as root.

### Building for debian based distributions

1. Navigate to the debian directory inside this repo (choose between Debian 7 or Debian 8). If you run Debian versions later than Debian 8, or Ubuntu 15.04 and later, the Debian 8 package is what you need.
2. Ensure that the build.sh script can be executed: `chmod +x build.sh`
3. Run the script: `./build.sh`
4. Install the package: `dpkg -i NVDARemoteServer.deb`

To uninstall it, run `dpkg --purge nvda-remote-server`

To uninstall it keeping the configuration files, run `dpkg --remove nvda-remote-server`

### Building for Centos and RHEL based distributions

To build the rpm version, the rpmdevtools package is required. Install it using your package manager.

1. Navigate to the RHEL directory inside this repo (choose between RHEL 6, RHEL 7 or RHEL 8). If you run Centos versions later than Centos 8, or Fedora, the RHL 8 package is what you need.
2. Ensure that the build.sh script can be executed: `chmod +x build.sh`
3. Run the script: `./build.sh`. The final rpm will be located at `~/rpmbuild/RPMS/noarch` directory.
4. Install the package using rpm: `rpm -U NVDARemoteServer.rpm`

To uninstall it, run `rpm -e NVDARemoteServer`

### Building for Mac Os x

1. Navigate to the Mac Os x directory inside this repo.
2. Ensure that the build.sh script can be executed: `chmod +x build.sh`
3. Run the script: `sudo ./build.sh`
4. Install the generated package using Finder or the terminal. Remember to allow untrusted software installation in System preferences > Security and privacy. To install from the terminal, run the following command: `installer -pkg NVDARemoteServer.pkg -target /`

To uninstall it, run `NVDARemoteUninstall`

### Building for Arch based distributions

Note: you must clone the repository and perform the following actions in a standard, non-privileged user account.

1. Navigate to the Arch directory inside this repo.
2. Ensure that the build.sh script can be executed: `chmod +x build.sh`
3. Run the script: `./build.sh`
4. Install the package with pacman: `sudo pacman -U NVDARemoteServer.pkg.tar.xz`

To uninstall it, run: `sudo pacman --remove NVDARemoteServer`

### Building for MSYS2 platform on Windows

1. Navigate to the MSYS directory inside this repo.
2. Repeat steps 3 and 4 from arch section.

### Installing on Cygwin

1. Navigate to the Cygwin directory from Cygwin Bash shell.
2. Run install.sh: `./install.sh`

To uninstall it, run `NVDARemoteUninstall`

### Building for Windows

You need one or multiple Python installations, depending on what you want to build. Install the x86 and x64 versions if you want to build the server for both architectures. Go to the [Python downloads page](https://www.python.org/downloads/) and choose:

* Python 2.x (2.7.15 or later) if you want to maximize compatibility with older Windows versions, including Windows xp. The server will also work on Windows 10.
* Python 3.x (3.6.6 or later) if you want to take advantage of all the Python performance and security improvements. Windows service currently is not working on Python 3.7.0, so official builds still use Python 3.6.

You need also Python for Windows Extensions, build 223 or later. Install this package running `pip install pywin32` command.

Finally, you must install a packager in order to build the binary version. If you are building with Python 2.x, you can use Pyinstaller (install with `pip install pyinstaller`), cx-freeze (install with `pip install cx-freeze`), or [py2exe 0.6.9](https://sourceforge.net/projects/py2exe/files/py2exe/0.6.9/). On Python 3, only pyinstaller and cx-freeze are supported.

Once the build environment is ready, open a command prompt and navigate to the root folder of this repository, then:

* If you want to use py2exe, run: `python setup_windows.py py2exe`
* If you prefer pyinstaller, run: `pyinstaller pyinstaller.spec`. Run `python -OO -m PyInstaller pyinstaller.spec` if you want to apply code optimizations.
* If you prefer cx-freeze, run: `python setup_windows_cxfreeze.py build`.

Note: if you build with several Python versions on the same machine, don't add python to the path environment variable during installation. Instead, use the Python launcher included with Python 3, or specify the full path to your python executable. For example: `C:\\python27x86\\python setup_windows.py py2exe`.

The binaries will be placed in the dist folder. For cx-freeze builds, the binaries will be placed in the build folder. If you build for multiple architectures, using multiple Python installations and packagers, remember saving the dist folder contents (in case of cx-freeze, the build folder) to another location before building again. To avoid conflicts, remove the build and dist directories after saving their contents.

The server is almost portable, there is no installation required. If you install the Windows service, remember uninstalling it before moving the server to another location or removing it.

### Building the Docker image

You need Docker installed on a Linux system. Navigate to the docker directory and run:

`docker build -t nvda-remote-server .`

Change or add more tags if you plan to push the image to a Docker registry. For example: `docker build -t jmdaweb/nvda-remote-server:latest -t jmdaweb/nvda-remote-server:2.0 .`

## Running

Before you begin, check that the tcp port you have chosen for the server (by default 6837) is allowed through your firewall.

On Unix platforms, including Mac Os x, there is a script located in /usr/bin called NVDARemoteServer. You can run this script without parameters to get a short help message.

If you want to start the server in debugging mode (useful to see activity and errors) run:

`sudo NVDARemoteServer debug`

On most platforms, you can stop the server by pressing ctrl+c if it is running in this mode.

To start the server, run:

`sudo NVDARemoteServer start`

To stop it, run:

`sudo NVDARemoteServer stop`

Run `sudo NVDARemoteServer restart` to restart the server.

If the server freezes, run `sudo NVDARemoteServer kill` to kill the process.

On Centos 6, Centos 7, Centos 8, Arch and Debian based distributions, the NVDA Remote Relay server is also installed as a service, so you can configure it to run at system startup, and manage it with the service and systemctl utilities. You can run `NVDARemoteServer status` to see if the service is running.

If you want to configure the service to run at system startup, run `sudo NVDARemoteServer enable`. Run `sudo NVDARemoteServer disable` to configure the service to start manually.

If you want to install the server as a system service on Windows, run service_manager.cmd as administrator and choose the right options on the displayed menu.

Run debug.cmd to start the server in debugging mode.

If you want to run the server inside a Docker container, use a command similar to the following:

`docker run -d -p 6837:6837 --rm jmdaweb/nvda-remote-server:latest`

The command above destroys the container once it is stopped. If you want a permanent container which you can start and stop without creation and removal, run:

`docker run -d -p 6837:6837 --name my_nvda_remote jmdaweb/nvda-remote-server:latest`

Or, if you want to create it and run later:

`docker create -p 6837:6837 --name my_nvda_remote jmdaweb/nvda-remote-server:latest`

You can change jmdaweb/nvda-remote-server:latest to your custom image name if you have built it. The --name argument specifies the container name. If you want to use a diferent port, change the first part after -p. The second must be always 6837.

Once created, you can start your container with the following command:

`docker start my_nvda_remote`

To stop it, run this command:

`docker stop my_nvda_remote`

Run this command to remove the container:

`docker rm my_nvda_remote`

## Log files

Do you run the server in production mode and it suddenly is stopped? Now you can look at the following files:

On most Linux distributions and Mac Os x: go to /var/log/NVDARemoteServer.log

On Arch Linux: go to /run/NVDARemoteServer/NVDARemoteServer.log

On Windows: NVDARemoteServer.log is located inside the program folder.

On a Docker container: run `docker logs containername`. For example: `docker logs my_nvda_remote`

Read the Docker documentation to see all available commands.

## Creating your own self-signed certificate

The server includes a default self-signed certificate to encrypt connections. This certificate is also included in the official NVDA Remote add-on, so this is a big security risk.

It is strongly recommended that you create your own certificate before starting the server for the first time. You can do it by running the NVDARemoteCertificate script on almost all platforms:

`sudo NVDARemoteCertificate`

The script takes no arguments. Follow the on-screen instructions to complete the process.

The script will create a 4096 bit RSA private key and a certificate, and combine them in a single server.pem file. Once finished, if the server is running, restart it.

On Windows, a pre-built OpenSSL version is included in the server directory. You can run NVDARemoteCertificate.cmd to create a certificate.

If your server is running inside a Docker container, you can run a command similar to the following:

`docker exec -t -i my_nvda_remote NVDARemoteCertificate`

## Configuration file and extra commandline options

Starting with version 1.5, NVDARemoteServer includes a configuration file that you can modify to change some server settings. You must restart the server after modifying this file. The comments in the file will guide you when changing settings.

By default, the configuration file is located inside the program folder (Windows) or in /etc (all other distributions), and it is named `NVDARemoteServer.conf`.

You can test your changes in debugging mode before modifying the configuration file. Although the changes in the configuration also are applied when you run the server in debug mode, you can pass some commandline parameters to perform tests. The following options are available:

* `--interface=ip`: listen only on the specified ip address. This setting doesn't affect IPV6 interfaces. In some platforms, this setting will not work if IPV6 socket binds to all interfaces.
* `--interface6=ip`: listen only on the specified IPV6 address. This setting doesn't affect IPV4 interfaces.
* `--port=port`: listen only on the specified tcp port.
* `--port6=port`: listen on the specified port, but only for IPV6. By default, use the value specified in --port. Use this value if you want different ports for IPV4 and IPV6 sockets.
* `--logfile=path`, `--pidfile=path`: these parameters are available, but unuseful in debug mode. You can use them on init.d and systemd units, but it's not recommended. Use --configfile instead. If you change pidfile in the configuration file and use the server as a system daemon, update the pidfile variable in the service units for the status command to work properly.
* `--loglevel=n`, where n is a number between 0 (almost quiet) and 4 (very verbose).
* `--pemfile=path`: path to the private key and certificate used for ssl connections. They must be in the same file.
* `--motd=string`: specify the message of the day displayed to all clients when they join a channel. Enclose the message between quotes.
* `--motd_force_display=integer`: display the message of the day even if it has not changed since last time the client joined a channel. 0 means do not force display, 1 means force display.
* `--configfile=path`: read config file from path. All the previous options can be edited in the configuration file.

Note: the command line arguments take precedence over the supplied ones in the configuration file.

Note for Docker container users: run a command similar to the following to edit the configuration file for your container:

`docker exec -t -i my_nvda_remote nano /etc/NVDARemoteServer.conf`

When the Nano editor loads, you can use arrow keys to move the cursor and perform changes. Once finished, press control+x. If you have made any changes, press y and then enter. Tipically, unless you know very well what you are doing, you should only update the parameters related to the message of the day.

## Known problems

### Installing on Mac os x El Capitan and later

Mac os x El Capitan adds a new feature called system integrity protection to prevent malware from modifying system files. If this feature is enabled, you won't be able to install NVDA Remote Server on your Mac.

If you want to disable it, follow these steps:

* Reboot your system. While rebooting, hold the command+r key to enter in recovery mode.
* Go to the utilities menu, and choose terminal.
* Type the following command: `csrutil disable`
* Reboot your system and go back to the main operating system.
* Install NVDA Remote Server.

Caution! Disabling system integrity protection is a security risk. To enable it back, run `csrutil enable` in recovery mode.

### Problems with the server in OpenVZ or Docker containers

If you run a Debian 8, RHEL 7 or RHEL 8 based OpenVZ or Docker container, don't install the Debian 8 or RHEL packages. They will fail and leave the installation in a bad state. In these containers, Systemd produces errors because it can't connect directly to the kernel.

Solution: install Debian 7 or RHL 6 package instead, or run systemd in a privileged container.

### Problems installing the Debian 8 package when systemd-sysv is not installed

Sometimes, calling systemctl causes an error because systemd is not running (for example, after upgrading from Debian 7 to Debian 8). As a consequence, the server package is not installed.

Solution: systemd-sysv is required to install this package. If you tried installing it, run apt -f install or apt-get -f install. Then, reboot your computer. Finally, run dpkg --configure nvda-remote-server.

### Installing on Mac os x Sierra and later

Mac Os Sierra doesn't allow untrusted software to be installed or used by default. In addition, this option has been removed from System Preferences application. To allow untrusted software:

* Go to the utilities folder, and open terminal.
* Type the following command: `sudo spctl --master-disable`
* Enter your password. Now, if system integrity protection has been disabled, you can install the package as described above.

Caution! Allowing untrusted applications is a security risk. To revert to the recommended settings, run `sudo spctl --master-enable`
