#base image
FROM debian:latest
#image metadata
LABEL version="2.5" description="This image allows you to run NVDA Remote Server inside a docker container" org.opencontainers.image.authors="Jose Manuel Delicado"
#prepare image
RUN <<EOT bash
groupadd -g 991 nvdaremoteserver
useradd -l -u 991 -g 991 -M nvdaremoteserver
 apt update
apt -y full-upgrade
apt -y install openssl python3
apt clean
mkdir /usr/share/NVDARemoteServer
mkdir /data
chown -R 991:991 /data /usr/share/NVDARemoteServer
EOT
COPY --chmod=755 docker/docker-entrypoint.sh NVDARemoteCertificate /usr/bin/
COPY daemon.py options.py server.py server.pem /usr/share/NVDARemoteServer
COPY NVDARemoteServer.conf /etc
VOLUME /data
#expose the following ports to the host
EXPOSE 6837
USER nvdaremoteserver
WORKDIR /usr/share/NVDARemoteServer
#this program is executed when a container is started
CMD ["python3", "-B", "/usr/share/NVDARemoteServer/server.py", "debug", "--configfile=/data/NVDARemoteServer.conf"]
ENTRYPOINT ["docker-entrypoint.sh"]
