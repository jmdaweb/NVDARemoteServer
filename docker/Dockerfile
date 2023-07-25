#base image
FROM debian
#image metadata
LABEL version="2.3" description="This image allows you to run NVDA Remote Server inside a docker container" org.opencontainers.image.authors="Jose Manuel Delicado"
#prepare image
ADD https://github.com/jmdaweb/NVDARemoteServer/releases/download/release-2.3/nvda-remote-server_2.3_debian_nonsystemd.deb nvda-remote-server.deb
COPY --chmod=755 docker-entrypoint.sh /usr/bin/
run groupadd -g 991 nvdaremoteserver && useradd -l -u 991 -g 991 -M nvdaremoteserver
run apt update && apt -y full-upgrade && apt -y install python3 openssl && dpkg -i nvda-remote-server.deb && rm -f nvda-remote-server.deb && apt clean
run mkdir /data && chown -R 991:991 /data
volume /data
#expose the following ports to the host
EXPOSE 6837
user nvdaremoteserver
#this program is executed when a container is started
CMD ["python3", "/usr/share/NVDARemoteServer/server.py", "debug", "--configfile=/data/NVDARemoteServer.conf"]
ENTRYPOINT ["docker-entrypoint.sh"]
