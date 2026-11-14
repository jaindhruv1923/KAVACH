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
    assert data["tools_count"] == 19
    assert data["agents_count"] == 5


def test_server_tools_endpoint(client):
    """Verify /api/tools endpoint returns all 19 MCP schemas."""
    resp = client.get("/api/tools")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["tools"]) == 19


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


def test_server_saga_endpoints(client):
    """Verify /api/saga/status and /api/saga/simulate endpoints."""
    # Status
    resp_status = client.get("/api/saga/status")
    assert resp_status.status_code == 200
    data_status = resp_status.json()
    assert data_status["status"] == "ACTIVE"
    assert "mathematical_invariant" in data_status

    # Simulate
    resp_sim = client.post("/api/saga/simulate")
    assert resp_sim.status_code == 200
    data_sim = resp_sim.json()
    assert data_sim["success"] is True
    assert data_sim["state"] == "ROLLED_BACK"
    assert data_sim["is_clean_restored"] is True
    assert data_sim["mathematical_invariant"]["satisfied"] is True


def test_server_differential_privacy_endpoints(client):
    """Verify /api/dp/budget, /api/dp/query, and /api/dp/simulate endpoints."""
    # 1. Budget endpoint
    resp_budget = client.get("/api/dp/budget")
    assert resp_budget.status_code == 200
    data_b = resp_budget.json()
    assert data_b["status"] == "ACTIVE"
    assert "mathematical_invariant" in data_b
    assert data_b["total_budget"] >= 5.0

    # 2. DP Query endpoint
    resp_q = client.post("/api/dp/query", json={"query_type": "COUNT", "epsilon": 0.5})
    assert resp_q.status_code == 200
    data_q = resp_q.json()
    assert data_q["success"] is True
    assert "privatized_value" in data_q
    assert data_q["sensitivity"] == 1.0

    # 3. Simulate reconstruction resistance
    resp_sim = client.post("/api/dp/simulate")
    assert resp_sim.status_code == 200
    data_sim = resp_sim.json()
    assert data_sim["success"] is True
    assert len(data_sim["trials"]) == 3


def test_server_stackelberg_and_ingress_endpoints(client):
    """Verify /api/game/status, /api/game/optimize, /api/ingress/consume, and /api/game/simulate."""
    # 1. Status
    resp_status = client.get("/api/game/status")
    assert resp_status.status_code == 200
    data_status = resp_status.json()
    assert data_status["status"] == "ACTIVE"
    assert "stackelberg_game" in data_status
    assert "token_bucket" in data_status

    # 2. Optimize
    resp_opt = client.post("/api/game/optimize")
    assert resp_opt.status_code == 200
    data_opt = resp_opt.json()
    assert data_opt["status"] == "EQUILIBRIUM_SOLVED"
    assert "defense_allocation_s_star" in data_opt

    # 3. Ingress Consume
    resp_consume = client.post("/api/ingress/consume", json={"client_id": "test_client", "cost": 1.0, "threat_level": 0.2})
    assert resp_consume.status_code == 200
    data_c = resp_consume.json()
    assert data_c["success"] is True
    assert data_c["admitted"] is True
    assert data_c["telemetry"]["client_id"] == "test_client"

    # 4. Simulate Comparison
    resp_sim = client.post("/api/game/simulate")
    assert resp_sim.status_code == 200
    data_sim = resp_sim.json()
    assert data_sim["success"] is True
    assert "comparison" in data_sim




