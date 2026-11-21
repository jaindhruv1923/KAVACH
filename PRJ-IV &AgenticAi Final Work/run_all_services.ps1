# ===========================================================================
#  KAVACH - Agentic AI Final Project launcher (PowerShell)
#
#  One server (port 8001) serves the main website AND every dashboard:
#    /  main platform   /cockpit/  Real AI Agents   /swarm/  Live Agent Swarm
#    /bharat/  Bharat Core Bank   /bank/  Banking Highway   /console  Live Console
#    /motion/  Motion Graphics    /guide  Stakeholder Guide /reports/ Mid-Sem Reports
#
#  Usage:
#    .\run_all_services.ps1              start the unified platform (recommended)
#    .\run_all_services.ps1 -Standalone  also start each dashboard on its own port
# ===========================================================================
param([switch]$Standalone)

$Root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Write-Host ""
Write-Host " KAVACH Platform Launcher" -ForegroundColor Cyan
Write-Host " ------------------------------------------------------------"

Write-Host " [1] Unified platform        http://localhost:8001/"
Start-Process python -ArgumentList "-m uvicorn app.main:app --app-dir `"kavach_platform\01_KAVACH_Platform\backend`" --host 127.0.0.1 --port 8001" -WorkingDirectory $Root

if ($Standalone) {
    Write-Host " [2] Live Agent Swarm        http://localhost:8000/"
    Start-Process powershell -ArgumentList "-NoProfile -Command `"`$env:PORT='8000'; python agent_engine.py`"" -WorkingDirectory "$Root\live_agent_swarm"
    Write-Host " [3] Bharat Core Bank        http://localhost:8002/"
    Start-Process powershell -ArgumentList "-NoProfile -Command `"`$env:PORT='8002'; python server.py`"" -WorkingDirectory "$Root\bharat_core_banking"
    Write-Host " [4] Real AI Agents cockpit  http://localhost:8003/"
    Start-Process python -ArgumentList "-m uvicorn kavach_agent_core.server:app --host 127.0.0.1 --port 8003" -WorkingDirectory $Root
}

Start-Sleep -Seconds 4
Start-Process "http://localhost:8001/"
Write-Host ""
Write-Host " Open http://localhost:8001/ - every dashboard is reachable from the top bar." -ForegroundColor Green
