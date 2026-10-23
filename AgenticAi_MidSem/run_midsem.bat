@echo off
REM ==============================================================================
REM KAVACH: Security-Governed Agentic AI Platform
REM CSE3101: Agentic AI — Mid-Sem Project Evaluation & Working Prototype
REM Instructors: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari
REM Department of Computer Science & Engineering, BML Munjal University
REM ==============================================================================

echo ==============================================================================
echo [CSE3101] Launching Agentic AI Mid-Sem Platform & Evaluation Cockpit...
echo Faculty: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari
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
echo [INFO] Starting FastAPI Agentic AI Core on http://127.0.0.1:8000 ...
echo [INFO] Interactive Mid-Sem Cockpit will open automatically in your browser.
echo [INFO] Press Ctrl+C in this terminal to stop the platform.
echo.

"%PY_EXE%" -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
