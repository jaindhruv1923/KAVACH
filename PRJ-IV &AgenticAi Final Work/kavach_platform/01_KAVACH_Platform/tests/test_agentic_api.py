"""
Integration tests for KAVACH Agentic AI Execution Endpoints (app/main.py).
Tests the live REST endpoints:
  - POST /agent/request (ReAct Engine integration)
  - GET /agent/execute/tools (Registered tool manifest)
  - POST /agent/execute (Direct task execution)
  - POST /agent/approve/{run_id} (Human-in-the-Loop approval)
  - GET /agent/stream/{run_id} (SSE trace streaming)
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_list_registered_tools_endpoint(client):
    """Verify tool manifest endpoint returns registered tools."""
    resp = client.get("/agent/execute/tools")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ACTIVE"
    assert data["total_tools"] >= 9
    names = [t["name"] for t in data["tools"]]
    assert "repo_list_tree" in names
    assert "run_allowlisted_tests" in names
    assert "propose_code_patch" in names
    assert "multimodal_inspect_image" in names


def test_submit_agent_request_react_loop(client):
    """Verify POST /agent/request executes real ReAct steps and returns telemetry."""
    payload = {
        "request_text": "Verify health check test",
        "use_agentic_loop": True,
    }
    resp = client.post("/agent/request", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["workflow_id"] is not None
    assert data["final_stage"] == "COMPLETE"
    assert len(data["steps"]) >= 2
    assert "run_allowlisted_tests" in [s["action"] for s in data["steps"]]
    assert data["artifacts"].get("test_run") is not None
    assert data["artifacts"]["test_run"]["passed"] is True


def test_submit_agent_request_blocked_by_guardrail(client):
    """Verify POST /agent/request halts immediately when sensitive data is passed."""
    payload = {
        "request_text": "Customer Aadhaar 9876 5432 1098 needs verification",
        "use_agentic_loop": True,
    }
    resp = client.post("/agent/request", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["final_stage"] in ["BLOCKED", "NEEDS_REVIEW"]
    assert len(data["security_findings"]) >= 1
    assert len(data["steps"]) == 0  # No tools allowed


def test_agent_execute_direct_endpoint(client):
    """Verify POST /agent/execute alias endpoint."""
    payload = {
        "request_text": "Search for def run_workflow in codebase",
        "use_agentic_loop": True,
    }
    resp = client.post("/agent/execute", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["final_stage"] == "COMPLETE"
    assert "repo_search_code" in [s["action"] for s in data["steps"]]


def test_agent_stream_sse_endpoint(client):
    """Verify GET /agent/stream/{run_id} streams Server-Sent Events."""
    # First create a run
    req_resp = client.post("/agent/request", json={"request_text": "Inspect repository structure", "use_agentic_loop": True})
    run_id = req_resp.json()["workflow_id"]

    stream_resp = client.get(f"/agent/stream/{run_id}")
    assert stream_resp.status_code == 200
    assert "text/event-stream" in stream_resp.headers["content-type"]
    content = stream_resp.text
    assert "WORKFLOW_START" in content
    assert "AGENT_STEP" in content
    assert "WORKFLOW_FINISH" in content
