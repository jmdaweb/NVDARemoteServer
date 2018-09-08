#base image
FROM ubuntu
#image metadata
MAINTAINER Jose Manuel Delicado
LABEL version="1.8" description="This image allows you to run NVDA Remote Server inside a docker container"
#prepare image
run apt-get update && apt-get -y dist-upgrade
run apt-get -y install python
ADD https://github.com/jmdaweb/NVDARemoteServer/releases/download/release-1.8/nvda-remote-server_1.8_debian7.deb nvda-remote-server.deb
run dpkg -i nvda-remote-server.deb && rm -f nvda-remote-server.deb
run apt-get clean
#expose the following ports to the host
EXPOSE 6837
#this program is executed when a container is started
ENTRYPOINT NVDARemoteServer debug
