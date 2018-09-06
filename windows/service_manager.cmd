@echo off
title NVDARemote server service manager
:menu
cls
echo Welcome to the NVDARemote server service manager.
echo if you haven't done it yet, run this script as administrator.
echo 1) install service
echo 2) uninstall service
echo 3) start service
echo 4) stop service
echo 5) Enable interactive mode
echo 6) set automatic startup
echo 7) set manual startup
echo 8) disable service
echo 9) exit
set /p choice=select an option: 
if %choice%==1 goto install
if %choice%==2 goto remove
if %choice%==3 goto start
if %choice%==4 goto stop
if %choice%==5 goto interactive
if %choice%==6 goto auto
if %choice%==7 goto manual
if %choice%==8 goto disable
if %choice%==9 goto quit
goto menu
:install
echo installing...
"%~dp0NVDARemoteServer.exe" install
pause
goto menu
:remove
echo uninstalling...
"%~dp0NVDARemoteServer.exe" remove
pause
goto menu
:start
echo starting...
"%~dp0NVDARemoteServer.exe" start
pause
goto menu
:stop
echo stopping...
"%~dp0NVDARemoteServer.exe" stop
pause
goto menu
:interactive
echo Enabling interactive mode...
"%~dp0NVDARemoteServer.exe" --interactive update
pause
goto menu
:auto
echo configuring service to run at system startup...
"%~dp0NVDARemoteServer.exe" --startup auto update
pause
goto menu
:manual
echo configuring service to run manually...
"%~dp0NVDARemoteServer.exe" --startup manual update
pause
goto menu
:disable
echo disabling service...
"%~dp0NVDARemoteServer.exe" --startup disabled update
pause
goto menu
:quit
