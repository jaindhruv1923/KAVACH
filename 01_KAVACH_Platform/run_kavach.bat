@echo off
REM ==============================================================================
REM KAVACH: Enterprise Security-Governed Agentic AI DevOps Platform
REM Full Project Production Engine & Multi-Service Highway
REM Lead Engineer: Dhruv Jain (B.Tech Final Year, BML Munjal University)
REM ==============================================================================

echo ==============================================================================
echo [KAVACH] Launching Full Enterprise Platform & Multi-Service Highway...
echo Port: http://127.0.0.1:8000
echo ==============================================================================

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

set PYTHONPATH=%SCRIPT_DIR%backend

REM Detect Python
set "PY_EXE=python"
if exist "%SCRIPT_DIR%..\.venv\Scripts\python.exe" (
    set "PY_EXE=%SCRIPT_DIR%..\.venv\Scripts\python.exe"
    echo [OK] Using dedicated project virtual environment Python.
) else (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python not found in PATH! Please ensure Python 3.10+ is installed.
        pause
        exit /b 1
    )
)

REM Launch browser in background after 2.5 seconds
start "" powershell -NoProfile -Command "Start-Sleep -Milliseconds 2500; Start-Process 'http://127.0.0.1:8000'"

echo.
echo [INFO] Starting FastAPI Enterprise Core on http://127.0.0.1:8000 ...
echo [INFO] Bharat Bank mounted at http://127.0.0.1:8000/bank/
echo [INFO] Results Cockpit mounted at http://127.0.0.1:8000/results/
echo [INFO] Press Ctrl+C in this terminal to stop the platform.
echo.

"%PY_EXE%" -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
