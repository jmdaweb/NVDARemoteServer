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
echo 5) exit
set /p choice=select an option: 
if %choice%==1 goto install
if %choice%==2 goto remove
if %choice%==3 goto start
if %choice%==4 goto stop
if %choice%==5 goto quit
goto menu
:install
echo installing...
"%~dp0NVDARemoteService.exe" -install
pause
goto menu
:remove
echo uninstalling...
"%~dp0NVDARemoteService.exe" -remove
pause
goto menu
:start
echo starting...
net start NVDARemoteService
pause
goto menu
:stop
echo stopping...
net stop NVDARemoteService
pause
goto menu
:quit
