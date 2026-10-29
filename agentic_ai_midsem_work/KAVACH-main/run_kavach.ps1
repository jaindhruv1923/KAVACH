<#
.SYNOPSIS
    KAVACH Master Launcher — Multilingual Security-Governed Agentic AI DevOps Platform.
.DESCRIPTION
    Starts the unified FastAPI backend + frontend and ensures genuine readiness before opening browser.
    Supports -Stop, -Restart, -Port, -HostAddress, -NoBrowser, -Dev flags.
#>
[CmdletBinding()]
param (
    [int]$Port = 8000,
    [string]$HostAddress = "127.0.0.1",
    [switch]$NoBrowser,
    [switch]$Stop,
    [switch]$Restart,
    [switch]$Dev,
    [int]$TimeoutSeconds = 45
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $ScriptDir

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "  KAVACH - Multilingual Security-Governed Agentic AI DevOps Platform" -ForegroundColor Green
Write-Host "  Unified Dev & Demonstration Launcher | Developer: Dhruv Jain" -ForegroundColor Yellow
Write-Host "============================================================================" -ForegroundColor Cyan

function Get-KavachProcessId {
    param([int]$TargetPort)
    try {
        $conns = Get-NetTCPConnection -LocalPort $TargetPort -State Listen -ErrorAction SilentlyContinue
        if ($conns) {
            return $conns[0].OwningProcess
        }
    } catch {
        # Fallback to netstat if Get-NetTCPConnection is unavailable
        $netstat = netstat -ano | Select-String ":$TargetPort\s+.*LISTENING\s+(\d+)"
        if ($netstat) {
            if ($netstat.Matches.Groups[1].Value) {
                return [int]$netstat.Matches.Groups[1].Value
            }
        }
    }
    return $null
}

function Stop-KavachServer {
    param([int]$TargetPort)
    $pidToKill = Get-KavachProcessId -TargetPort $TargetPort
    if ($pidToKill) {
        Write-Host "[STOP] Found active process listening on port $TargetPort (PID: $pidToKill). Terminating..." -ForegroundColor Yellow
        try {
            Stop-Process -Id $pidToKill -Force -ErrorAction SilentlyContinue
            Start-Sleep -Seconds 1
            Write-Host "[STOP] Successfully stopped KAVACH process (PID: $pidToKill)." -ForegroundColor Green
            return $true
        } catch {
            Write-Warning "Could not stop PID ${pidToKill}: $_"
            return $false
        }
    } else {
        Write-Host "[INFO] No process listening on port $TargetPort." -ForegroundColor DarkGray
        return $false
    }
}

# --- Action: Stop ---
if ($Stop) {
    $null = Stop-KavachServer -TargetPort $Port
    exit 0
}

# --- Action: Restart ---
if ($Restart) {
    $null = Stop-KavachServer -TargetPort $Port
    Start-Sleep -Seconds 2
}

# --- Check if already running ---
try {
    $healthCheck = Invoke-RestMethod -Uri "http://$HostAddress`:$Port/health" -Method Get -TimeoutSec 2 -ErrorAction SilentlyContinue
    if ($healthCheck -and $healthCheck.service -eq "kavach-backend") {
        Write-Host "[INFO] KAVACH backend is ALREADY running and healthy on http://$HostAddress`:$Port." -ForegroundColor Green
        if (-not $NoBrowser) {
            Write-Host "[LAUNCH] Opening browser to http://localhost:$Port ..." -ForegroundColor Cyan
            Start-Process "http://localhost:$Port"
        }
        Write-Host "[READY] Ready for requests. Use '.\run_kavach.ps1 -Stop' to terminate." -ForegroundColor Green
        exit 0
    }
} catch {
    # Port is not currently answering KAVACH health check, proceed with startup
}

# Verify port availability
$existingPid = Get-KavachProcessId -TargetPort $Port
if ($existingPid) {
    Write-Host "[WARNING] Port $Port is currently occupied by PID $existingPid." -ForegroundColor Yellow
    Write-Host "Attempting to release port $Port..." -ForegroundColor Yellow
    Stop-KavachServer -TargetPort $Port
    Start-Sleep -Seconds 1
}

# --- Locate Python Interpreter ---
$PythonExe = "python"
$VenvPaths = @(
    "$ScriptDir\.venv\Scripts\python.exe",
    "$ScriptDir\venv\Scripts\python.exe",
    "$ScriptDir\01_KAVACH_Platform\.venv\Scripts\python.exe",
    "$ScriptDir\01_KAVACH_Platform\venv\Scripts\python.exe"
)
foreach ($vp in $VenvPaths) {
    if (Test-Path $vp) {
        $PythonExe = $vp
        Write-Host "[ENV] Using detected Virtual Environment: $vp" -ForegroundColor Cyan
        break
    }
}

try {
    $pyVer = & $PythonExe --version 2>&1
    Write-Host "[ENV] Python interpreter: $PythonExe ($pyVer)" -ForegroundColor DarkGray
} catch {
    Write-Host "[FATAL] Python interpreter not found in PATH or virtual environments." -ForegroundColor Red
    exit 1
}

# Verify required core dependencies
$depCheck = & $PythonExe -c "import fastapi, uvicorn, pydantic; print('OK')" 2>&1
if ($depCheck -notmatch "OK") {
    Write-Host "[ERROR] Required Python packages missing (FastAPI, Uvicorn, Pydantic)." -ForegroundColor Red
    Write-Host "Please install dependencies via:" -ForegroundColor Yellow
    Write-Host "  $PythonExe -m pip install -r 01_KAVACH_Platform/backend/requirements.txt" -ForegroundColor White
    exit 1
}

# --- Validate Environment Configuration (Without Printing Secrets) ---
$EnvFile = "$ScriptDir\01_KAVACH_Platform\backend\.env"
if (-not (Test-Path $EnvFile)) {
    $EnvFile = "$ScriptDir\.env"
}

$HasGeminiKey = $false
$GeminiKeyMasked = "Not Configured"
if (Test-Path $EnvFile) {
    $envLines = Get-Content $EnvFile -ErrorAction SilentlyContinue
    foreach ($line in $envLines) {
        if ($line -match "^\s*GEMINI_API_KEY\s*=\s*(.+)$") {
            $val = $matches[1].Trim().Trim('"').Trim("'")
            if ($val -and $val.Length -gt 6) {
                $HasGeminiKey = $true
                $GeminiKeyMasked = $val.Substring(0, 6) + "..." + $val.Substring($val.Length - 4)
            }
        }
    }
}
if ($env:GEMINI_API_KEY) {
    $HasGeminiKey = $true
    $val = $env:GEMINI_API_KEY.Trim()
    if ($val.Length -gt 6) {
        $GeminiKeyMasked = $val.Substring(0, 6) + "..." + $val.Substring($val.Length - 4)
    }
}

Write-Host "[CONFIG] Model Provider : $(if ($HasGeminiKey) { "Google Gemini Cloud (API Key: $GeminiKeyMasked)" } else { "Deterministic Heuristic Engine (Offline Safe Mode)" })" -ForegroundColor $(if ($HasGeminiKey) { "Green" } else { "Yellow" })
Write-Host "[CONFIG] Port           : $Port" -ForegroundColor DarkGray
Write-Host "[CONFIG] Host           : $HostAddress" -ForegroundColor DarkGray

# --- Configure Directory and PYTHONPATH ---
$BackendDir = "$ScriptDir\01_KAVACH_Platform\backend"
if (-not (Test-Path $BackendDir)) {
    Write-Host "[ERROR] Backend directory not found at $BackendDir!" -ForegroundColor Red
    exit 1
}

$BankingDir = "$ScriptDir\02_Banking_and_Results_Dashboard"
$env:PYTHONPATH = "$BackendDir;$BankingDir;$BankingDir\implementation_banks;$env:PYTHONPATH"
$env:PYTHONUNBUFFERED = "1"

# --- Launch Backend Process ---
Write-Host "[STARTUP] Launching Uvicorn backend server on http://$HostAddress`:$Port ..." -ForegroundColor White

$uvicornArgs = @(
    "-m", "uvicorn", "app.main:app",
    "--app-dir", $BackendDir,
    "--host", $HostAddress,
    "--port", "$Port"
)
if ($Dev) {
    $uvicornArgs += "--reload"
}

$backendProc = Start-Process -FilePath $PythonExe -ArgumentList $uvicornArgs -WorkingDirectory $ScriptDir -PassThru

# --- Polling Readiness Check ---
Write-Host "[WAIT] Waiting for backend readiness at http://$HostAddress`:$Port/ready (timeout: $TimeoutSeconds s)..." -ForegroundColor White

$ready = $false
$readyRes = $null
$elapsed = 0
$interval = 1

while ($elapsed -lt $TimeoutSeconds) {
    if ($backendProc.HasExited) {
        Write-Host ""
        Write-Host "[ERROR] Backend process terminated unexpectedly with exit code $($backendProc.ExitCode)." -ForegroundColor Red
        Write-Host "Diagnostic command:" -ForegroundColor Yellow
        Write-Host "  $PythonExe -m uvicorn app.main:app --app-dir 01_KAVACH_Platform/backend --host $HostAddress --port $Port" -ForegroundColor White
        exit 1
    }

    try {
        $readyRes = Invoke-RestMethod -Uri "http://$HostAddress`:$Port/ready" -Method Get -TimeoutSec 2 -ErrorAction SilentlyContinue
        if ($readyRes -and ($readyRes.status -eq "ready" -or $readyRes.status -eq "degraded")) {
            $ready = $true
            break
        }
    } catch {
        # Backend warming up
    }

    Start-Sleep -Seconds $interval
    $elapsed += $interval
    Write-Host "." -NoNewline -ForegroundColor DarkGray
}
Write-Host ""

if (-not $ready) {
    Write-Host "[ERROR] Backend failed to report ready status within $TimeoutSeconds seconds." -ForegroundColor Red
    if (-not $backendProc.HasExited) {
        Stop-Process -Id $backendProc.Id -Force -ErrorAction SilentlyContinue
    }
    exit 1
}

# --- Display Detailed Readiness Telemetry ---
Write-Host "----------------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "  [OK] KAVACH UNIFIED PLATFORM READY & VERIFIED" -ForegroundColor Green
Write-Host "  Status          : $($readyRes.status.ToUpper())" -ForegroundColor Green
Write-Host "  Version         : $($readyRes.version)" -ForegroundColor DarkGray
Write-Host "  Agent Tools     : $($readyRes.subsystems.registered_agent_tools.total_tools) tools registered" -ForegroundColor Cyan
Write-Host "  Core Banking    : $($readyRes.subsystems.core_banking_highway)" -ForegroundColor Cyan
Write-Host "  LLM Provider    : $($readyRes.subsystems.llm_provider.provider)" -ForegroundColor Cyan
Write-Host "----------------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host "  Active System Endpoints:" -ForegroundColor Yellow
Write-Host "  1. KAVACH Security Console  : http://$HostAddress`:$Port" -ForegroundColor White
Write-Host "  2. Bharat Banking Highway   : http://$HostAddress`:$Port/bank/" -ForegroundColor White
Write-Host "  3. Interactive Swagger Docs : http://$HostAddress`:$Port/docs" -ForegroundColor White
Write-Host "----------------------------------------------------------------------------" -ForegroundColor DarkGray

# --- Open Browser Only After Verified Readiness ---
if (-not $NoBrowser) {
    Write-Host "[BROWSER] Opening dashboard at http://localhost:$Port ..." -ForegroundColor Cyan
    Start-Process "http://localhost:$Port"
}

Write-Host ""
Write-Host "[RUNNING] KAVACH is active (PID: $($backendProc.Id))." -ForegroundColor Green
Write-Host "[RUNNING] Press Ctrl+C in this terminal to stop cleanly." -ForegroundColor White
Write-Host "[RUNNING] Or run '.\run_kavach.ps1 -Stop' from another terminal." -ForegroundColor DarkGray
Write-Host ""

try {
    # Keep script open while process is active
    Wait-Process -Id $backendProc.Id
} finally {
    if (-not $backendProc.HasExited) {
        Write-Host "`n[SHUTDOWN] Stopping backend process (PID $($backendProc.Id))..." -ForegroundColor Yellow
        Stop-Process -Id $backendProc.Id -Force -ErrorAction SilentlyContinue
        Write-Host "[SHUTDOWN] Server stopped cleanly." -ForegroundColor Green
    }
}
