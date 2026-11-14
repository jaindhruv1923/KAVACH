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
    assert data["tools_count"] == 11
    assert data["agents_count"] == 5


def test_server_tools_endpoint(client):
    """Verify /api/tools endpoint returns all 11 MCP schemas."""
    resp = client.get("/api/tools")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["tools"]) == 11


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
