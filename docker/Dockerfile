#base image
FROM ubuntu
#image metadata
MAINTAINER Jose Manuel Delicado
LABEL version="2.2" description="This image allows you to run NVDA Remote Server inside a docker container"
#prepare image
ADD https://github.com/jmdaweb/NVDARemoteServer/releases/download/release-2.2/nvda-remote-server_2.2_debian_nonsystemd.deb nvda-remote-server.deb
run apt update && apt -y full-upgrade && apt -y install python3 nano openssl && dpkg -i nvda-remote-server.deb && rm -f nvda-remote-server.deb && apt clean
#expose the following ports to the host
EXPOSE 6837
#this program is executed when a container is started
ENTRYPOINT ["python3", "/usr/share/NVDARemoteServer/server.py", "debug"]
