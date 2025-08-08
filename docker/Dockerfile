#base image
FROM debian:latest
#image metadata
LABEL version="2.4" description="This image allows you to run NVDA Remote Server inside a docker container" org.opencontainers.image.authors="Jose Manuel Delicado"
#prepare image
RUN <<EOT bash
groupadd -g 991 nvdaremoteserver
 useradd -l -u 991 -g 991 -M nvdaremoteserver
apt update
apt -y full-upgrade
apt install -y python3 openssl
apt clean
mkdir /usr/share/NVDARemoteServer
mkdir /data
chown -R 991:991 /data
EOT
COPY --chmod=755 docker/docker-entrypoint.sh /usr/bin/
COPY daemon.py options.py server.py server.pem /usr/share/NVDARemoteServer
COPY NVDARemoteServer.conf /etc
VOLUME /data
#expose the following ports to the host
EXPOSE 6837
USER nvdaremoteserver
#this program is executed when a container is started
CMD ["python3", "/usr/share/NVDARemoteServer/server.py", "debug", "--configfile=/data/NVDARemoteServer.conf"]
ENTRYPOINT ["docker-entrypoint.sh"]
