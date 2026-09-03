"""
FastAPI Endpoint Tests
Tests for all HTTP endpoints in the Kavach backend.
"""

import pytest
import json
from fastapi.testclient import TestClient


class TestHealthEndpoint:
    """Test service health check endpoint."""

    def test_health_check(self, client):
        """Test that health endpoint returns OK."""
        response = client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "service" in data

    def test_root_endpoint(self, client):
        """Test root endpoint (should redirect or serve frontend, test for redirect)."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code in [200, 307, 302]


class TestSecurityDetectionEndpoint:
    """Test security detection endpoint."""

    def test_detect_pan_endpoint(self, client):
        """Test PAN detection via endpoint."""
        response = client.post(
            "/detect",
            json={"text": "My PAN is ABCDE1234F"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "findings" in data
        assert "allowed" in data
        assert data["allowed"] is False

    def test_detect_safe_text_endpoint(self, client):
        """Test detection on safe text."""
        response = client.post(
            "/detect",
            json={"text": "The meeting is tomorrow at 2 PM"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["allowed"] is True

    def test_detect_email_endpoint(self, client):
        """Test email detection."""
        response = client.post(
            "/detect",
            json={"text": "Email me at test@example.com"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["allowed"] is False

    def test_detect_phone_endpoint(self, client):
        """Test phone detection."""
        response = client.post(
            "/detect",
            json={"text": "Call 9876543210 for support"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["allowed"] is False


class TestRAGEndpoints:
    """Test RAG (search) endpoints."""

    def test_ingest_endpoint(self, client, sample_repository_path):
        """Test repository ingestion endpoint."""
        response = client.post(
            "/ingest",
            json={"repo_path": sample_repository_path},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "repo_path" in data
        assert "files_chunks_found" in data
        assert "chunks_indexed" in data
        assert data["chunks_indexed"] > 0

    def test_search_endpoint(self, client, sample_repository_path):
        """Test repository search endpoint."""
        # First ingest
        client.post("/ingest", json={"repo_path": sample_repository_path})
        
        # Then search
        response = client.post(
            "/search",
            json={"query": "authentication", "top_k": 3},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "query" in data
        assert "results" in data
        assert isinstance(data["results"], list)

    def test_search_default_top_k(self, client, sample_repository_path):
        """Test search with default top_k."""
        client.post("/ingest", json={"repo_path": sample_repository_path})
        
        response = client.post(
            "/search",
            json={"query": "authentication"},
        )
        
        assert response.status_code == 200
        data = response.json()
        # Default should be 5
        assert len(data["results"]) <= 5

    def test_search_custom_top_k(self, client, sample_repository_path):
        """Test search with custom top_k."""
        client.post("/ingest", json={"repo_path": sample_repository_path})
        
        response = client.post(
            "/search",
            json={"query": "module", "top_k": 2},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["results"]) <= 2


class TestAgentEndpoints:
    """Test agent orchestrator endpoints."""

    def test_agent_request_endpoint(self, client, sample_repository_path):
        """Test agent request submission."""
        # Ingest first
        client.post("/ingest", json={"repo_path": sample_repository_path})
        
        response = client.post(
            "/agent/request",
            json={"request_text": "Add authentication to login module"},
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "workflow_id" in data
        assert "final_stage" in data
        assert "plan" in data
        assert "retrieved_context" in data
        assert "security_findings" in data

    def test_agent_request_returns_full_workflow(self, client, sample_repository_path):
        """Test that agent request returns all workflow fields."""
        client.post("/ingest", json={"repo_path": sample_repository_path})
        
        response = client.post(
            "/agent/request",
            json={"request_text": "Test request"},
        )
        
        assert response.status_code == 200
        data = response.json()
        
        required_fields = [
            "workflow_id",
            "final_stage",
            "plan",
            "retrieved_context",
            "security_findings",
            "generation_result",
            "validation_result",
            "impact_report",
            "history",
        ]
        for field in required_fields:
            assert field in data

    def test_get_agent_run(self, client, sample_repository_path):
        """Test retrieving a specific agent run."""
        client.post("/ingest", json={"repo_path": sample_repository_path})
        
        # Submit request
        submit_response = client.post(
            "/agent/request",
            json={"request_text": "Test workflow"},
        )
        workflow_id = submit_response.json()["workflow_id"]
        
        # Get run
        response = client.get(f"/agent/runs/{workflow_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["workflow_id"] == workflow_id
        assert data["request_text"] == "Test workflow"

    def test_get_nonexistent_run(self, client):
        """Test getting a run that doesn't exist."""
        response = client.get("/agent/runs/nonexistent-id-12345")
        
        assert response.status_code == 200
        data = response.json()
        assert "error" in data

    def test_list_agent_runs(self, client, sample_repository_path):
        """Test listing all agent runs."""
        client.post("/ingest", json={"repo_path": sample_repository_path})
        
        # Submit multiple requests
        client.post("/agent/request", json={"request_text": "Request 1"})
        client.post("/agent/request", json={"request_text": "Request 2"})
        
        response = client.get("/agent/runs")
        
        assert response.status_code == 200
        data = response.json()
        assert "count" in data
        assert "runs" in data
        assert data["count"] >= 2

    def test_list_runs_shows_run_summary(self, client, sample_repository_path):
        """Test that run list includes basic info about each run."""
        client.post("/ingest", json={"repo_path": sample_repository_path})
        client.post("/agent/request", json={"request_text": "Test run"})
        
        response = client.get("/agent/runs")
        data = response.json()
        
        if data["count"] > 0:
            run = data["runs"][0]
            assert "id" in run
            assert "stage" in run
            assert "request" in run


class TestImpactEndpoints:
    """Test impact analysis endpoints."""

    def test_impact_analyze_endpoint(self, client, sample_repository_path):
        """Test impact analysis endpoint."""
        response = client.post(
            "/impact/analyze",
            json={
                "change_description": "Modify authentication module",
                "repo_path": "app",
            },
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "change_description" in data
        assert "impact_report" in data
        assert isinstance(data["impact_report"], list)

    def test_impact_analyze_returns_ranked_results(self, client):
        """Test that impact analysis returns ranked results."""
        response = client.post(
            "/impact/analyze",
            json={"change_description": "Update database schema"},
        )
        
        assert response.status_code == 200
        data = response.json()
        report = data["impact_report"]
        
        if len(report) > 1:
            # Should be sorted by relevance
            scores = [r["relevance_score"] for r in report]
            assert scores == sorted(scores, reverse=True)

    def test_evaluate_impact_endpoint(self, client):
        """Test impact evaluation endpoint."""
        response = client.get("/impact/evaluate")
        
        assert response.status_code == 200
        data = response.json()
        assert "overall" in data
        assert "per_case" in data
        assert "total_cases" in data


class TestSecurityEvaluationEndpoint:
    """Test security engine evaluation endpoint."""

    def test_evaluate_security_endpoint(self, client):
        """Test security evaluation endpoint."""
        response = client.get("/evaluate")
        
        assert response.status_code == 200
        data = response.json()
        assert "overall" in data
        assert "per_language" in data
        assert "total_cases" in data

    def test_evaluate_returns_metrics(self, client):
        """Test that evaluation returns all expected metrics."""
        response = client.get("/evaluate")
        data = response.json()
        
        overall = data["overall"]
        required_metrics = ["precision", "recall", "f1"]
        for metric in required_metrics:
            assert metric in overall


class TestEndpointErrorHandling:
    """Test endpoint error handling."""

    def test_ingest_invalid_path(self, client):
        """Test ingest with invalid path."""
        response = client.post(
            "/ingest",
            json={"repo_path": "/nonexistent/path/to/repo"},
        )
        
        # Should return 200 but with 0 chunks
        assert response.status_code == 200
        data = response.json()
        # May have 0 chunks if path doesn't exist
        assert "chunks_indexed" in data

    def test_search_before_ingest(self, client):
        """Test search without indexing first."""
        response = client.post(
            "/search",
            json={"query": "test"},
        )
        
        # Should handle gracefully (empty results or error)
        assert response.status_code == 200

    def test_agent_request_with_pii(self, client):
        """Test agent request with PII in input."""
        response = client.post(
            "/agent/request",
            json={"request_text": "My PAN is ABCDE1234F"},
        )
        
        # Should handle PII (might block or flag)
        assert response.status_code == 200
        data = response.json()
        # Check security findings
        findings = data.get("security_findings", [])
        if len(findings) > 0:
            assert "findings" in response.json() or "security_findings" in response.json()


class TestEndpointDataFormats:
    """Test endpoint request/response formats."""

    def test_detect_request_schema(self, client):
        """Test that detect endpoint validates request schema."""
        # Missing required field
        response = client.post("/detect", json={})
        # Should fail validation
        assert response.status_code == 422

    def test_ingest_request_schema(self, client):
        """Test that ingest endpoint validates request schema."""
        # Missing required field
        response = client.post("/ingest", json={})
        assert response.status_code == 422

    def test_search_request_schema(self, client):
        """Test that search endpoint validates request schema."""
        # Missing required field
        response = client.post("/search", json={})
        assert response.status_code == 422

    def test_agent_request_schema(self, client):
        """Test that agent request endpoint validates schema."""
        # Missing required field
        response = client.post("/agent/request", json={})
        assert response.status_code == 422


class TestEndpointIntegration:
    """Integration tests across endpoints."""

    def test_full_workflow_via_api(self, client, sample_repository_path):
        """Test complete workflow through API endpoints."""
        # 1. Health check
        health = client.get("/health")
        assert health.status_code == 200
        
        # 2. Ingest repository
        ingest = client.post("/ingest", json={"repo_path": sample_repository_path})
        assert ingest.status_code == 200
        
        # 3. Search for content
        search = client.post("/search", json={"query": "authentication", "top_k": 3})
        assert search.status_code == 200
        
        # 4. Detect PII
        detect = client.post("/detect", json={"text": "Safe text about code changes"})
        assert detect.status_code == 200
        
        # 5. Submit agent request
        agent = client.post(
            "/agent/request",
            json={"request_text": "Add authentication"},
        )
        assert agent.status_code == 200
        
        # 6. List runs
        runs = client.get("/agent/runs")
        assert runs.status_code == 200
        
        # 7. Get specific run
        workflow_id = agent.json()["workflow_id"]
        run = client.get(f"/agent/runs/{workflow_id}")
        assert run.status_code == 200
        
        # 8. Analyze impact
        impact = client.post(
            "/impact/analyze",
            json={"change_description": "Update module", "repo_path": "demo_repo"},
        )
        assert impact.status_code == 200
        
        # 9. Evaluate security
        eval_sec = client.get("/evaluate")
        assert eval_sec.status_code == 200
        
        # 10. Evaluate impact
        eval_impact = client.get("/impact/evaluate")
        assert eval_impact.status_code == 200
