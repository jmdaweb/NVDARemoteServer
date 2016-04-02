@echo off
title NVDA Remote Server self-signed certificate generator
cd %~dp0
openssl genrsa -out key.key 4096
openssl req -new -key key.key -out cert.csr
openssl x509 -req -days 3650 -in cert.csr -signkey key.key -out cert.crt
del server.pem
copy key.key + cert.crt server.pem
del key.key
del cert.csr
del cert.crt
echo Certificate successfully created
echo You must restart the server for the changes to take effect. Press any key to exit.
pause