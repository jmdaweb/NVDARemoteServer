#base image
FROM python:3.13-alpine
#image metadata
LABEL version="2.4" description="This image allows you to run NVDA Remote Server inside a docker container" org.opencontainers.image.authors="Jose Manuel Delicado"
#prepare image
RUN <<EOT sh
addgroup -g 991 -S nvdaremoteserver
 adduser -S -u 991 -G nvdaremoteserver -H nvdaremoteserver
apk update
apk upgrade --no-cache
apk add --no-cache openssl
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
