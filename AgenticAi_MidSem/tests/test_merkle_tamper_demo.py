"""
Unit tests for Cryptographic Merkle Tree Ledger Tamper Demo Endpoint (Step 4 / Kaikei).
Verifies:
- Isolated clone tamper injection without corrupting live global ledger
- Deterministic detection and exact corrupted leaf index isolation
- Mathematical non-repudiation and DPDP statutory audit verification
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.security.merkle_ledger import global_merkle_ledger


@pytest.fixture
def client():
    return TestClient(app)


class TestMerkleTamperDemo:
    """Tests for POST /security/merkle/tamper-demo."""

    def test_tamper_demo_detects_corruption_on_clone(self, client):
        """Test tamper detection identifies corrupted leaf index on in-memory clone."""
        res = client.post("/security/merkle/tamper-demo", json={"target_index": 1})
        assert res.status_code == 200
        data = res.json()

        assert data["status"] == "TAMPER_DETECTED"
        assert data["real_ledger_untouched"] is True
        assert data["demo_scope"] == "IN_MEMORY_ISOLATED_LEDGER_CLONE"
        assert data["target_index"] == 1

        # Pre-tamper was completely valid
        assert data["pre_tamper_verification"]["is_valid"] is True
        assert data["pre_tamper_verification"]["tamper_detected"] is False

        # Post-tamper isolated exact corrupted index
        assert data["post_tamper_verification"]["is_valid"] is False
        assert data["post_tamper_verification"]["tamper_detected"] is True
        assert data["post_tamper_verification"]["corrupted_index"] == 1

    def test_tamper_demo_custom_index_and_payload(self, client):
        """Test tamper demo with custom target index and custom adversarial payload."""
        res = client.post(
            "/security/merkle/tamper-demo",
            json={
                "target_index": 0,
                "tamper_payload": "FORGED_UNAUTHORIZED_ACCOUNT_DEBIT_RECORD",
            },
        )
        assert res.status_code == 200
        data = res.json()

        assert data["status"] == "TAMPER_DETECTED"
        assert data["target_index"] == 0
        assert data["post_tamper_verification"]["corrupted_index"] == 0
        assert "FORGED_UNAUTHORIZED_ACCOUNT_DEBIT_RECORD" in str(data["tampered_entry_details"])

    def test_live_ledger_remains_uncompromised(self, client):
        """Verify that executing tamper demo leaves live global ledger completely pristine."""
        # 1. Run tamper demo
        demo_res = client.post("/security/merkle/tamper-demo")
        assert demo_res.status_code == 200

        # 2. Check live verification endpoint
        live_res = client.get("/security/merkle/verify")
        assert live_res.status_code == 200
        live_data = live_res.json()

        assert live_data["is_valid"] is True
        assert live_data["tamper_detected"] is False
