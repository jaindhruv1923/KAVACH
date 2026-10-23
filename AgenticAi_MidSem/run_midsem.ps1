# ==============================================================================
# KAVACH: Security-Governed Agentic AI Platform
# CSE3101: Agentic AI — Mid-Sem Project Evaluation & Working Prototype
# Instructors: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari
# Department of Computer Science & Engineering, BML Munjal University
# ==============================================================================

Write-Host "==============================================================================" -ForegroundColor Cyan
Write-Host " [CSE3101] Launching Agentic AI Mid-Sem Platform & Evaluation Cockpit..." -ForegroundColor Green
Write-Host " Faculty: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari" -ForegroundColor Yellow
Write-Host "==============================================================================" -ForegroundColor Cyan

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

$env:PYTHONPATH = Join-Path $ScriptDir "backend"

# Detect Python executable
$venvPy = Join-Path $ScriptDir "..\.venv\Scripts\python.exe"
if (Test-Path $venvPy) {
    $pyCmd = $venvPy
    Write-Host "[OK] Using dedicated project virtual environment: $venvPy" -ForegroundColor Green
} else {
    try {
        $pyVer = & python --version 2>&1
        $pyCmd = "python"
        Write-Host "[OK] Detected System Python: $pyVer" -ForegroundColor Green
    } catch {
        Write-Host "[ERROR] Python was not found in PATH. Please install Python 3.10+." -ForegroundColor Red
        exit 1
    }
}

# Auto-open browser after a short delay
Start-Job -ScriptBlock {
    Start-Sleep -Seconds 3
    Start-Process "http://127.0.0.1:8000"
} | Out-Null

Write-Host "`n[INFO] Starting FastAPI Agentic AI Core on http://127.0.0.1:8000 ..." -ForegroundColor Cyan
Write-Host "[INFO] Interactive Mid-Sem Cockpit will open automatically in your browser." -ForegroundColor Cyan
Write-Host "[INFO] Press Ctrl+C to terminate.`n" -ForegroundColor Gray

& $pyCmd -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
