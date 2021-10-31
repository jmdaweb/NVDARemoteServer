@echo off
title NVDA Remote Server self-signed certificate generator
cd %~dp0
setlocal
set OPENSSL_CONF=%~dp0openssl.cnf
openssl genpkey -out key.key -algorithm EC -pkeyopt ec_paramgen_curve:secp384r1
openssl req -new -key key.key -out cert.csr -sha512
openssl x509 -req -days 3650 -in cert.csr -signkey key.key -out cert.crt
del server.pem
copy key.key + cert.crt server.pem
del key.key
del cert.csr
del cert.crt
endlocal
echo Certificate successfully created
echo You should restart the server for the changes to take effect on all connected clients. Press any key to exit.
pause