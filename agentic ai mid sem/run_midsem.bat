@echo off
title KAVACH MidSem Platform Launcher (Port 8000)
color 0A
cd /d "%~dp0kavach_platform"
call "%~dp0kavach_platform\run_kavach.bat" %*
