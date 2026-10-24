# ==============================================================================
# KAVACH: Enterprise Security-Governed Agentic AI DevOps Platform
# Full Project Production Engine & Multi-Service Highway
# Lead Engineer: Dhruv Jain (B.Tech Final Year, BML Munjal University)
# ==============================================================================

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host " [KAVACH] Launching Full Enterprise Platform & Multi-Service Highway..." -ForegroundColor White
Write-Host " Port: http://127.0.0.1:8000" -ForegroundColor Green
Write-Host "==============================================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

$env:PYTHONPATH = "$scriptDir\backend"

$pyExe = "python"
if (Test-Path "$scriptDir\..\.venv\Scripts\python.exe") {
    $pyExe = "$scriptDir\..\.venv\Scripts\python.exe"
    Write-Host "[OK] Using dedicated project virtual environment Python." -ForegroundColor Green
}

Start-Job -ScriptBlock {
    Start-Sleep -Milliseconds 2500
    Start-Process "http://127.0.0.1:8000"
} | Out-Null

Write-Host ""
Write-Host "[INFO] Starting FastAPI Enterprise Core on http://127.0.0.1:8000 ..." -ForegroundColor Cyan
Write-Host "[INFO] Bharat Bank mounted at http://127.0.0.1:8000/bank/" -ForegroundColor Yellow
Write-Host "[INFO] Results Cockpit mounted at http://127.0.0.1:8000/results/" -ForegroundColor Yellow
Write-Host "[INFO] Press Ctrl+C in this terminal to stop the platform." -ForegroundColor DarkGray
Write-Host ""

& $pyExe -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
