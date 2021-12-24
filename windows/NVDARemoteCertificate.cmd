@echo off
title NVDA Remote Server self-signed certificate generator
cd %~dp0
setlocal
set OPENSSL_CONF=%~dp0openssl.cnf
:pkey
cls
echo Welcome to the NVDARemoteCertificate utility
echo This program generates a new private key and public certificate for your NVDA Remote Server instance
echo Press control+c at any time to abort the process
echo Select your private key type
echo 1) RSA 4096-bit (compatible with older systems)
echo 2) Ecdsa secp384r1 (recommended on more recent systems)
set /p choice=select an option: 
if %choice%==1 goto rsa
if %choice%==2 goto ecdsa
goto pkey
:rsa
openssl genrsa -out key.key 4096
goto cert
:ecdsa
openssl genpkey -out key.key -algorithm EC -pkeyopt ec_paramgen_curve:secp384r1
:cert
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