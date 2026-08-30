import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

project = Path(r"c:\Users\dhruv\OneDrive\Desktop\PRJ-IV\Kavach_AllPhases\Complete_Merged_Project")
env = os.environ.copy()
env["PYTHONPATH"] = str(project / "backend")

print("== FULL PYTEST ==")
pytest_result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests", "-q"],
    cwd=str(project),
    env=env,
    capture_output=True,
    text=True,
)
summary = (pytest_result.stdout or "") + (pytest_result.stderr or "") + f"\nEXIT {pytest_result.returncode}\n"
(project / "pytest_summary_final.txt").write_text(summary, encoding="utf-8")
print(summary)

print("== BACKEND STARTUP ==")
proc = subprocess.Popen(
    [sys.executable, "-m", "uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
    cwd=str(project),
    env=env,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
)
try:
    started = False
    for _ in range(40):
        time.sleep(0.5)
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/health", timeout=3) as resp:
                body = resp.read().decode('utf-8')
                print("HEALTH", resp.status, body)
                started = True
                break
        except Exception:
            pass
    if not started:
        print("HEALTH_CHECK_FAILED")
        output = proc.stdout.read() if proc.stdout else ""
        print(output)
        raise RuntimeError("Backend did not become healthy")

    with urllib.request.urlopen("http://127.0.0.1:8000/docs", timeout=5) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
        print("DOCS_STATUS", resp.status, "len=", len(html))
        print("HAS_SWAGGER", "Swagger UI" in html or "swagger" in html.lower())

    with urllib.request.urlopen("http://127.0.0.1:8000/openapi.json", timeout=5) as resp:
        openapi = json.loads(resp.read().decode('utf-8'))
        print("OPENAPI_TITLE", openapi.get("info", {}).get("title"))
        print("PATH_COUNT", len(openapi.get("paths", {})))
finally:
    proc.terminate()
    try:
        proc.wait(timeout=10)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=10)

print("VERIFY_COMPLETE")
