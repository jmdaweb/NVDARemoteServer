#!/bin/sh
if ! test -e /data/NVDARemoteServer.conf
then
cp /etc/NVDARemoteServer.conf /data
fi
exec "$@"
