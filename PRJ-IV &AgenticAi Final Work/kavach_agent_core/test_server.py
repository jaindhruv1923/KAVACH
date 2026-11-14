"""
Unit tests for KAVACH Server & Live Streaming API.
Course: CSE3101 Agentic AI - Final Capstone Project
"""

import os
import sys
import pytest
from starlette.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kavach_agent_core.server import app


@pytest.fixture
def client():
    return TestClient(app)


def test_server_status_endpoint(client):
    """Verify /api/status endpoint returns active status and tools."""
    resp = client.get("/api/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ONLINE"
    assert data["tools_count"] == 13
    assert data["agents_count"] == 5


def test_server_tools_endpoint(client):
    """Verify /api/tools endpoint returns all 13 MCP schemas."""
    resp = client.get("/api/tools")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["tools"]) == 13


def test_server_swarm_execute_api(client):
    """Verify /api/swarm/execute runs and returns complete result."""
    payload = {"goal": "Audit transaction for user with Aadhaar 9999 9999 0019 and PAN ABCDE1234F"}
    resp = client.post("/api/swarm/execute", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "COMPLETE"
    assert "blackboard" in data
    assert "timeline" in data


def test_server_cockpit_html_endpoint(client):
    """Verify root / serves the live cockpit HTML."""
    resp = client.get("/")
    assert resp.status_code == 200
    assert "KAVACH Multi-Agent AI Defense Platform" in resp.text


def test_server_benchmark_endpoints(client):
    """Verify /api/benchmark/summary and /api/benchmark/run endpoints."""
    resp = client.get("/api/benchmark/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "EVALUATION_SUCCESS"
    assert data["total_test_vectors"] == 30
    assert data["accuracy_pct"] == 100.0
    assert "confusion_matrix" in data
    assert "domain_breakdown" in data

    resp_run = client.post("/api/benchmark/run")
    assert resp_run.status_code == 200
    data_run = resp_run.json()
    assert data_run["tests_passed"] == 30


def test_server_reflexion_endpoints(client):
    """Verify /api/reflexion/status and /api/reflexion/simulate endpoints."""
    resp = client.get("/api/reflexion/status")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ACTIVE"
    assert "convergence_rate_pct" in data

    resp_sim = client.post("/api/reflexion/simulate")
    assert resp_sim.status_code == 200
    sim_data = resp_sim.json()
    assert sim_data["status"] == "COMPLETE"
    assert sim_data["verdict"] == "REFLEXION_SELF_CORRECTED"
    assert "reflexion_audit" in sim_data["audit_dossier"]


def test_server_ast_and_supply_chain_endpoints(client):
    """Verify /api/ast/rules, /api/ast/scan, and /api/supply-chain/audit endpoints."""
    # 1. Rules endpoint
    resp_rules = client.get("/api/ast/rules")
    assert resp_rules.status_code == 200
    data_rules = resp_rules.json()
    assert data_rules["status"] == "ACTIVE"
    assert len(data_rules["forbidden_sinks"]) == 5
    assert "requests" in data_rules["verified_ecosystem_packages"]

    # 2. AST scan endpoint with vulnerable payload
    vulnerable_code = "import colorma\ndef run_job(user_input):\n    eval(user_input)\n"
    resp_scan = client.post("/api/ast/scan", json={"code": vulnerable_code})
    assert resp_scan.status_code == 200
    data_scan = resp_scan.json()
    assert data_scan["success"] is True
    assert data_scan["is_safe"] is False
    assert data_scan["sinks_found_count"] >= 1
    assert data_scan["slopsquats_found_count"] >= 1

    # 3. Supply chain audit endpoint with typosquatted dependency
    resp_sc = client.post("/api/supply-chain/audit", json={"requirements": "reqeusts>=2.31.0\nnumpy==1.24.0"})
    assert resp_sc.status_code == 200
    data_sc = resp_sc.json()
    assert data_sc["success"] is True
    assert data_sc["is_safe"] is False
    assert data_sc["slopsquatting_anomalies_count"] == 1

