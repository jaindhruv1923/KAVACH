@echo off
title KAVACH Unified Ecosystem Launcher
color 0B
echo ===============================================================================
echo   PRJ4 - Agentic AI Final Project: KAVACH Ecosystem Master Launcher
echo   Developers: Dhruv Jain ^| Instructors: Dr. Soharab Hossain Shaikh ^& Mr. Pranshu Tiwari
echo ===============================================================================
echo.
echo [1/3] Starting KAVACH Real Autonomous Multi-Agent Swarm on Port 8003...
start "KAVACH Real Autonomous Swarm (Port 8003)" cmd /k "cd /d %~dp0 && set PORT=8003 && python -m uvicorn kavach_agent_core.server:app --host 127.0.0.1 --port 8003"

echo [2/3] Starting Bharat Core Bank Web Portal on Port 8002...
start "Bharat Core Bank Portal (Port 8002)" cmd /k "cd /d %~dp0bharat_core_banking && python server.py"

echo [3/3] Starting Main KAVACH Security Platform on Port 8001...
start "KAVACH Main Platform (Port 8001)" cmd /k "cd /d %~dp0kavach_platform\01_KAVACH_Platform\backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8001"

echo.
echo Waiting 3 seconds for services to initialize...
timeout /t 3 /nobreak >nul

echo Opening Master Control Hub: http://localhost:8001/ ...
start http://localhost:8001/

echo.
echo ===============================================================================
echo   ALL 3 SERVICES ARE NOW RUNNING IN DEDICATED CONSOLES:
echo   - Master Security Platform:   http://localhost:8001/
echo   - Bharat Core Bank Portal:    http://localhost:8002/
echo   - Live Agent Swarm Engine:    http://localhost:8003/
echo   - Core Banking Highway:       http://localhost:8001/bank/
echo ===============================================================================
pause

