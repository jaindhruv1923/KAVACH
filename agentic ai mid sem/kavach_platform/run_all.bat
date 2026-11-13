@echo off
setlocal
cd /d "%~dp0"
echo [KAVACH Unified] Redirecting to unified master launcher...
call "%~dp0run_kavach.bat" %*
