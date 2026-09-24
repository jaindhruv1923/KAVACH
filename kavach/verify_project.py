import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

project = Path(__file__).resolve().parent
backend_dir = project / "backend"
env = os.environ.copy()
env["PYTHONPATH"] = str(backend_dir)

print("=" * 60)
print("1. RUNNING FULL PYTEST SUITE")
print("=" * 60)
pytest_result = subprocess.run(
    [sys.executable, "-m", "pytest", "tests", "-q"],
    cwd=str(project),
    env=env,
    capture_output=True,
    text=True,
)
summary = (pytest_result.stdout or "") + (pytest_result.stderr or "")
print(summary.strip())
print(f"Pytest Exit Code: {pytest_result.returncode} (0 = PASS)\n")
assert pytest_result.returncode == 0, "Pytest suite failed!"

print("=" * 60)
print("2. RUNNING CI SECURITY GATE")
print("=" * 60)
gate_result = subprocess.run(
    [sys.executable, "ci_security_gate.py"],
    cwd=str(backend_dir),
    env=env,
    capture_output=True,
    text=True,
)
print(gate_result.stdout.strip())
print(f"Gate Exit Code: {gate_result.returncode} (0 = PASS)\n")
assert gate_result.returncode == 0, "CI Security Gate failed!"

print("=" * 60)
print("3. TESTING LIVE BACKEND API & SENSITIVE NUMBER DETECTION")
print("=" * 60)
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Health Check
resp = client.get("/health")
assert resp.status_code == 200
print("✓ Backend Health Check:", resp.json())

# Test 1: Bare number 12454323454
resp1 = client.post("/detect", json={"text": "12454323454"})
res1 = resp1.json()
print("✓ Detection test (12454323454):")
print("  Allowed:", res1["allowed"], "(Expected: False)")
print("  Findings:", res1["findings"])
assert not res1["allowed"], "12454323454 should be flagged!"

# Test 2: Bare 12-digit Aadhaar number
resp2 = client.post("/detect", json={"text": "123456789012"})
res2 = resp2.json()
print("✓ Detection test (123456789012):")
print("  Allowed:", res2["allowed"], "(Expected: False)")
print("  Findings:", res2["findings"])
assert not res2["allowed"], "123456789012 should be flagged!"

# Test 3: Safe developer prompt
resp3 = client.post("/detect", json={"text": "Add a health check endpoint on port 8080"})
res3 = resp3.json()
print("✓ Detection test (Safe prompt with port 8080):")
print("  Allowed:", res3["allowed"], "(Expected: True)")
assert res3["allowed"], "Safe prompt should be allowed!"

# Test 4: Agent workflow halting on bare number
resp4 = client.post("/agent/request", json={"request_text": "12454323454"})
res4 = resp4.json()
print("✓ Agent workflow halting test (12454323454):")
print("  Final stage:", res4["final_stage"], "(Expected: NEEDS_REVIEW or BLOCKED)")
print("  Policy decision:", res4["policy_decision"]["decision"])
assert res4["final_stage"] in ("NEEDS_REVIEW", "BLOCKED"), "Workflow should halt on sensitive number!"

# Test 5: Static frontend serving
resp5 = client.get("/static/index.html")
assert resp5.status_code == 200
assert "Security-Governed Agentic AI DevOps Platform" in resp5.text
assert "12454323454" in resp5.text
print("✓ Frontend Dashboard is active and correctly configured!")

print("\n" + "=" * 60)
print("ALL VERIFICATIONS PASSED AUTOMATICALLY (100% SUCCESS)!")
print("=" * 60)

