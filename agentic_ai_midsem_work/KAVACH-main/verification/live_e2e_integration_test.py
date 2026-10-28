"""
KAVACH Master End-to-End Live Integration Verification Suite.
Validates the single working system across Backend, Agentic ReAct Engine,
Security Boundaries, State Persistence, and Multi-Service Mounts.
"""

import sys
import os
import json
import time

# Ensure backend and banking paths are available
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BACKEND_DIR = os.path.join(PROJECT_ROOT, "01_KAVACH_Platform", "backend")
BANKING_DIR = os.path.join(PROJECT_ROOT, "02_Banking_and_Results_Dashboard")

for p in [BACKEND_DIR, BANKING_DIR, os.path.join(BANKING_DIR, "implementation_banks")]:
    if p not in sys.path and os.path.exists(p):
        sys.path.insert(0, p)

from fastapi.testclient import TestClient
from app.main import app
from app.agent.tools import repo_read_file, apply_approved_patch, run_allowlisted_tests

client = TestClient(app)

results_ledger = []

def record_check(name: str, status: str, detail: str = ""):
    results_ledger.append({"check": name, "status": status, "detail": detail})
    symbol = "PASS" if status == "PASS" else ("FAIL" if status == "FAIL" else status)
    print(f"[{symbol:5}] {name}: {detail}")

def test_liveness():
    res = client.get("/health")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert data.get("status") == "ok", "Expected status ok"
    assert data.get("service") == "kavach-backend", "Expected service kavach-backend"
    assert "timestamp" in data, "Expected timestamp"
    record_check("Backend Liveness (/health)", "PASS", f"Status: {data['status']}, Service: {data['service']}")

def test_readiness():
    res = client.get("/ready")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert data.get("status") in ("ready", "degraded"), f"Unexpected status: {data.get('status')}"
    sub = data.get("subsystems", {})
    assert "registered_agent_tools" in sub, "Missing registered_agent_tools in readiness"
    assert sub["registered_agent_tools"]["total_tools"] >= 9, f"Expected >= 9 tools, got {sub['registered_agent_tools']['total_tools']}"
    assert "llm_provider" in sub, "Missing llm_provider in readiness"
    assert "core_banking_highway" in sub, "Missing core_banking_highway in readiness"
    record_check("Subsystem Readiness (/ready)", "PASS", f"Status: {data['status']}, Tools: {sub['registered_agent_tools']['total_tools']}, Provider: {sub['llm_provider']['provider']}")

def test_frontend_serving():
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert "text/html" in res.headers.get("content-type", ""), "Expected HTML content type"
    assert "Kavach" in res.text, "Expected 'Kavach' in HTML title/body"
    assert "agentic-trace-card" in res.text, "Expected '#agentic-trace-card' in HTML workspace"
    record_check("Root Frontend Serving (/)", "PASS", "HTTP 200 with index.html containing Kavach and agentic-trace-card")

def test_highways_mounted():
    res_bank = client.get("/bank", follow_redirects=True)
    assert res_bank.status_code == 200, f"Expected 200 for /bank, got {res_bank.status_code}"
    record_check("Core Bharat Banking Highway Mount", "PASS", f"Bank Highway: {res_bank.status_code}")

def test_tools_registry():
    res = client.get("/agent/execute/tools")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert data.get("total_tools") >= 9, f"Expected >= 9 tools, got {data.get('total_tools')}"
    tool_names = [t["name"] for t in data.get("tools", [])]
    assert "repo_list_tree" in tool_names, "Missing repo_list_tree"
    assert "repo_read_file" in tool_names, "Missing repo_read_file"
    assert "propose_code_patch" in tool_names, "Missing propose_code_patch"
    assert "apply_approved_patch" in tool_names, "Missing apply_approved_patch"
    assert "run_allowlisted_tests" in tool_names, "Missing run_allowlisted_tests"
    assert "multimodal_inspect_image" in tool_names, "Missing multimodal_inspect_image"
    record_check("Agent Tool Registry (/agent/execute/tools)", "PASS", f"Verified {len(tool_names)} registered tools with schemas")

def test_safe_task_execution():
    res = client.post("/agent/request", json={"request_text": "Add a health-check endpoint on port 8080 returning JSON status"})
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert data.get("final_stage") == "COMPLETE", f"Expected COMPLETE, got {data.get('final_stage')}"
    assert len(data.get("steps", [])) > 0, "Expected at least 1 ReAct step"
    assert "run_allowlisted_tests" in data.get("tools_executed", []), f"Expected run_allowlisted_tests in tools_executed: {data.get('tools_executed')}"
    record_check("Autonomous Safe Task ReAct Loop", "PASS", f"Stage: {data['final_stage']}, Steps: {len(data['steps'])}, Tools: {data['tools_executed']}")

def test_security_halt_on_pii():
    res = client.post("/agent/request", json={"request_text": "My Aadhaar is 1234 5678 9012, please fix production bug"})
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert data.get("final_stage") in ("NEEDS_REVIEW", "BLOCKED"), f"Expected halt, got {data.get('final_stage')}"
    assert len(data.get("tools_executed", [])) == 0, f"Expected 0 tools executed on PII halt, got {data.get('tools_executed')}"
    assert len(data.get("security_findings", [])) > 0, "Expected security findings detected"
    record_check("Zero-Trust Security Gate on Sensitive Input", "PASS", f"Halted at stage {data['final_stage']}, Findings: {len(data['security_findings'])}, 0 tools run")

def test_inspection_task():
    res = client.post("/agent/request", json={"request_text": "Inspect security vulnerabilities in app/security/detector.py"})
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert "repo_list_tree" in data.get("tools_executed", []), f"Expected repo_list_tree executed, got {data.get('tools_executed')}"
    record_check("Repository Inspection Agent Task", "PASS", f"Executed tools: {data.get('tools_executed')}")

def test_approval_enforcement():
    # Attempt write without token
    write_res = apply_approved_patch("test.txt", "content", approval_token="")
    assert write_res["success"] is False, "Expected write failure without token"
    assert "approval required" in write_res["error"].lower(), f"Unexpected error: {write_res['error']}"

    # Attempt path traversal
    try:
        repo_read_file("../../windows/win.ini")
        traversal_blocked = False
    except PermissionError:
        traversal_blocked = True
    assert traversal_blocked, "Path traversal was NOT blocked"

    # Attempt non-allowlisted test
    test_res = run_allowlisted_tests("arbitrary/test.py")
    assert test_res["success"] is False, "Expected non-allowlisted test to fail"
    assert "outside allowlisted" in test_res["error"], f"Unexpected error: {test_res['error']}"

    record_check("Security Bounds & Approval Enforcement", "PASS", "Verified token required for writes, path traversal blocked, allowlist enforced")

def test_persistence_and_recovery():
    # Submit task to get ID
    res = client.post("/agent/request", json={"request_text": "Verify test suite execution"})
    assert res.status_code == 200
    run_id = res.json()["workflow_id"]

    # Verify run is retrieved from /agent/runs
    runs_res = client.get("/agent/runs")
    assert runs_res.status_code == 200
    runs = runs_res.json().get("runs", [])
    found = any(r.get("id") == run_id for r in runs)
    assert found, f"Run {run_id} not found in /agent/runs"

    # Verify run detail retrieved from /agent/runs/{id}
    detail_res = client.get(f"/agent/runs/{run_id}")
    assert detail_res.status_code == 200
    detail = detail_res.json()
    assert detail.get("id") == run_id, "Mismatch in retrieved run id"
    record_check("State Persistence & Retrieval (/agent/runs)", "PASS", f"Successfully saved and retrieved workflow {run_id}")

def test_supervisor_approval_endpoint():
    res = client.post("/agent/request", json={"request_text": "Propose patch for config.py"})
    run_id = res.json()["workflow_id"]
    token = "SUPERVISOR_ELEVATED_TOKEN"
    
    appr_res = client.post(f"/agent/approve/{run_id}", json={
        "approved": True,
        "approval_token": token,
        "supervisor_id": "Prof. Reviewer"
    })
    assert appr_res.status_code == 200, f"Expected 200, got {appr_res.status_code}"
    data = appr_res.json()
    assert data.get("status") == "APPROVED", f"Expected APPROVED, got {data.get('status')}"
    record_check("Supervisor HITL Approval Flow (/agent/approve)", "PASS", f"Run {run_id} approved with token")

def main():
    print("=" * 76)
    print("  KAVACH MASTER END-TO-END LIVE INTEGRATION VERIFICATION")
    print("=" * 76)
    tests = [
        test_liveness,
        test_readiness,
        test_frontend_serving,
        test_highways_mounted,
        test_tools_registry,
        test_safe_task_execution,
        test_security_halt_on_pii,
        test_inspection_task,
        test_approval_enforcement,
        test_persistence_and_recovery,
        test_supervisor_approval_endpoint,
    ]
    all_passed = True
    for t in tests:
        try:
            t()
        except AssertionError as ae:
            record_check(t.__name__, "FAIL", str(ae))
            all_passed = False
        except Exception as e:
            record_check(t.__name__, "FAIL", f"Unexpected error: {e}")
            all_passed = False

    print("=" * 76)
    passed_count = sum(1 for r in results_ledger if r["status"] == "PASS")
    total_count = len(results_ledger)
    print(f"SUMMARY: {passed_count}/{total_count} CHECKS PASSED.")
    if all_passed:
        print("RESULT: ALL E2E INTEGRATION CHECKS PASSED.")
        sys.exit(0)
    else:
        print("RESULT: SOME CHECKS FAILED.")
        sys.exit(1)

if __name__ == "__main__":
    main()
