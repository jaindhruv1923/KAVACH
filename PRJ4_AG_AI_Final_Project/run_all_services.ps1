# PRJ4 - Agentic AI Final Project Master PowerShell Launcher
# Starts Port 8001 (Main KAVACH), Port 8000 (Live Swarm), Port 8002 (Applications Work)

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "  PRJ4 - Agentic AI Final Project: KAVACH Master PowerShell Launcher" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition

Write-Host "[1/3] Launching Live Agent Swarm on Port 8000..." -ForegroundColor Yellow
Start-Process python -ArgumentList "live_agent_dashboard/agent_engine.py" -WorkingDirectory $ScriptDir

Write-Host "[2/3] Launching Applications Work Portal on Port 8002..." -ForegroundColor Yellow
Start-Process python -ArgumentList "applications_work/server.py" -WorkingDirectory $ScriptDir

Write-Host "[3/3] Launching Main KAVACH Platform on Port 8001..." -ForegroundColor Yellow
$BackendDir = "$ScriptDir\kavach_platform\01_KAVACH_Platform\backend"
Start-Process python -ArgumentList "-m uvicorn app.main:app --app-dir `"$BackendDir`" --host 127.0.0.1 --port 8001" -WorkingDirectory $ScriptDir

Write-Host "Waiting 3 seconds for service initialization..." -ForegroundColor DarkGray
Start-Sleep -Seconds 3

Write-Host "Opening Master Dashboard: http://localhost:8001/ ..." -ForegroundColor Green
Start-Process "http://localhost:8001/"
