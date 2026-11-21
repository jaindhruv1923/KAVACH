@echo off
setlocal
title KAVACH Platform Launcher
REM ===========================================================================
REM  KAVACH - Agentic AI Final Project launcher
REM
REM  One server (port 8001) serves the main website AND every dashboard:
REM    /            Main platform          /cockpit/   Real AI Agents
REM    /swarm/      Live Agent Swarm       /bharat/    Bharat Core Bank
REM    /bank/       Banking Highway        /console    Live Console
REM    /motion/     Motion Graphics        /guide      Stakeholder Guide
REM    /reports/    Mid-Sem Reports
REM
REM  Usage:
REM    run_all_services.bat              start the unified platform (recommended)
REM    run_all_services.bat standalone   also start each dashboard on its own port
REM ===========================================================================
set ROOT=%~dp0
echo.
echo  KAVACH Platform Launcher
echo  ------------------------------------------------------------
echo  [1] Starting the unified platform on http://localhost:8001/
start "KAVACH Platform (8001)" cmd /k "cd /d %ROOT% && python -m uvicorn app.main:app --app-dir kavach_platform\01_KAVACH_Platform\backend --host 127.0.0.1 --port 8001"

if /I "%~1"=="standalone" (
  echo  [2] Starting Live Agent Swarm on http://localhost:8000/
  start "KAVACH Live Agent Swarm (8000)" cmd /k "cd /d %ROOT%live_agent_swarm && set PORT=8000 && python agent_engine.py"
  echo  [3] Starting Bharat Core Bank on http://localhost:8002/
  start "Bharat Core Bank (8002)" cmd /k "cd /d %ROOT%bharat_core_banking && set PORT=8002 && python server.py"
  echo  [4] Starting Real AI Agents cockpit on http://localhost:8003/
  start "KAVACH Real AI Agents (8003)" cmd /k "cd /d %ROOT% && python -m uvicorn kavach_agent_core.server:app --host 127.0.0.1 --port 8003"
)

echo.
echo  Waiting for the platform to start...
timeout /t 4 /nobreak >nul
start http://localhost:8001/
echo.
echo  Open http://localhost:8001/ - every dashboard is reachable from the top bar.
echo  Close the server windows to stop KAVACH.
endlocal
