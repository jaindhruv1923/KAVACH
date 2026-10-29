@echo off
title KAVACH Unified Ecosystem Launcher
color 0B
echo ===============================================================================
echo   PRJ4 - Agentic AI Final Project: KAVACH Ecosystem Master Launcher
echo   Developers: Dhruv Jain ^| Instructors: Dr. Soharab Hossain Shaikh ^& Mr. Pranshu Tiwari
echo ===============================================================================
echo.
echo [1/3] Starting KAVACH Live Agent Swarm Engine on Port 8000...
start "KAVACH Live Agent Engine (Port 8000)" cmd /k "cd /d %~dp0live_agent_dashboard && python agent_engine.py"

echo [2/3] Starting Bharat Core Bank Applications Portal on Port 8002...
start "Bharat Core Bank Applications (Port 8002)" cmd /k "cd /d %~dp0applications_work && python server.py"

echo [3/3] Starting Main KAVACH Platform Backend on Port 8001...
start "KAVACH Main Platform (Port 8001)" cmd /k "cd /d %~dp0kavach_platform\01_KAVACH_Platform\backend && python -m uvicorn app.main:app --host 127.0.0.1 --port 8001"

echo.
echo Waiting 3 seconds for services to initialize...
timeout /t 3 /nobreak >nul

echo Opening Master Control Hub: http://localhost:8001/ ...
start http://localhost:8001/

echo.
echo ===============================================================================
echo   ALL 3 SERVICES ARE NOW RUNNING IN DEDICATED CONSOLES:
echo   - Master Platform:       http://localhost:8001/
echo   - Live Agent Swarm:      http://localhost:8000/
echo   - Applications Work:     http://localhost:8002/
echo   - Core Banking Highway:  http://localhost:8001/bank/
echo ===============================================================================
pause
