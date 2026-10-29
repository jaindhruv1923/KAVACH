"""
Test Suite: Elite Agentic AI Ideations 1 to 5
Verifies:
1. Constitutional Red-Team Autonomous Self-Play (RLAIF)
2. Conformal Risk Control & Epistemic Uncertainty (Smart HITL)
3. Byzantine Fault Tolerant (pBFT) Multi-Agent Swarm Consensus
4. Zero-Knowledge Agentic Attestation (zk-SNARK style Proofs over Merkle DAG)
5. Turnkey Statutory Regulatory Compliance Engine (India DPDP 2023, RBI 10A, EU AI Act)
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.security.constitutional_redteam import ConstitutionalRedTeamEngine
from app.security.conformal_risk import ConformalRiskEngine
from app.security.byzantine_consensus import ByzantineSwarmEngine
from app.security.zk_attestation import ZkAgenticAttestationEngine
from app.security.statutory_compliance import StatutoryRegulatoryEngine

client = TestClient(app)


# 1. Test Constitutional Red-Teaming Self-Play
def test_constitutional_redteam_self_play():
    engine = ConstitutionalRedTeamEngine()
    mutated, desc = engine.mutate_payload("api_key = 'sk-live-93820194829019283019'", strategy="HOMOGLYPH")
    assert len(mutated) > 0
    assert "homoglyph" in desc.lower()

    # Test via API
    res = client.post("/api/v1/redteam/mutate", json={"code": "sk-live-93820194829019283019"})
    assert res.status_code == 200
    data = res.json()
    assert data["rounds_executed"] == 4
    assert data["adversarial_resilience_rate_pct"] == 100.0


# 2. Test Conformal Risk Control
def test_conformal_risk_control_epistemic_bounds():
    engine = ConformalRiskEngine(target_error_rate=0.01)
    
    # High confidence clean action
    safe_eval = engine.evaluate_proposal_uncertainty("log_telemetry", predicted_confidence=0.99, payload_entropy=2.1)
    assert safe_eval["verdict"] == "AUTONOMOUS_APPROVED"
    assert safe_eval["hitl_escalation_required"] is False

    # Ambiguous action with high payload entropy
    risky_eval = engine.evaluate_proposal_uncertainty("drop_tables", predicted_confidence=0.45, payload_entropy=5.2)
    assert risky_eval["hitl_escalation_required"] is True
    assert "DYNAMIC_HITL_MANDATORY" in risky_eval["verdict"]

    # Test via API
    res = client.post("/api/v1/conformal/evaluate", json={
        "action_name": "high_value_wire_transfer",
        "confidence": 0.40,
        "code": "sk-live-high-entropy-crypto-token-payload"
    })
    assert res.status_code == 200
    assert res.json()["hitl_escalation_required"] is True


# 3. Test Byzantine Swarm Consensus
def test_byzantine_swarm_consensus_quorum_and_isolation():
    engine = ByzantineSwarmEngine()
    
    # 3 honest nodes approving
    votes_clean = [
        {"agent_id": "A1", "vote": "APPROVE", "taint_detected": False},
        {"agent_id": "A2", "vote": "APPROVE", "taint_detected": False},
        {"agent_id": "A3", "vote": "APPROVE", "taint_detected": False},
    ]
    res_clean = engine.evaluate_swarm_action("TASK-01", "deploy_service", {}, votes_clean)
    assert res_clean["status"] == "CONSENSUS_COMMITTED"
    assert res_clean["quorum_achieved"] is True

    # 1 compromised rogue node attempting to force execution
    votes_poisoned = [
        {"agent_id": "ROGUE_WORKER", "vote": "APPROVE", "taint_detected": True},
        {"agent_id": "SENTINEL_GUARD", "vote": "REJECT", "taint_detected": False},
        {"agent_id": "COMPLIANCE_AGENT", "vote": "REJECT", "taint_detected": False},
    ]
    res_poisoned = engine.evaluate_swarm_action("TASK-02", "delete_database", {}, votes_poisoned)
    assert res_poisoned["status"] == "CONSENSUS_VETOED"
    assert "ROGUE_WORKER" in res_poisoned["compromised_nodes_isolated"]

    # Test via API
    api_res = client.post("/api/v1/byzantine/vote", json={"simulate_poisoned_node": True})
    assert api_res.status_code == 200
    assert api_res.json()["status"] == "CONSENSUS_VETOED"


# 4. Test Zero-Knowledge Agentic Attestation
def test_zk_attestation_proof_generation_and_verification():
    engine = ZkAgenticAttestationEngine()
    proof = engine.generate_attestation_proof(
        event_id="EVT-TEST-8812",
        shannon_entropy=3.12,
        pii_tokens_count=0,
        dual_signatures_valid=True,
        raw_secret_payload="super_confidential_vendor_payment_token"
    )
    assert proof["proof_valid"] is True
    # Verify raw secret is NOT leaked in the public proof
    assert "super_confidential" not in str(proof)
    assert len(proof["blinded_payload_commitment"]) == 128  # SHA3-512 hex length
    
    # Verify proof offline
    assert engine.verify_proof_offline(proof) is True

    # Test via API
    api_res = client.post("/api/v1/zk/attest", json={
        "event_id": "EVT-SENTINEL-API",
        "shannon_entropy": 2.8,
        "pii_count": 0,
        "dual_signatures_valid": True,
        "raw_payload_secret": "my_secret_token"
    })
    assert api_res.status_code == 200
    assert api_res.json()["verified_offline"] is True


# 5. Test Statutory Regulatory Compliance Engine
def test_statutory_compliance_dossier():
    engine = StatutoryRegulatoryEngine()
    dossier = engine.generate_compliance_dossier({"workflow_id": "TEST-WF-001"})
    assert dossier["statutory_violations_detected"] == 0
    assert len(dossier["statutory_matrix"]) == 5
    assert "DPDP Act" in dossier["jurisdictions_certified"][0]
    
    # Test via API
    res = client.get("/api/v1/compliance/dossier")
    assert res.status_code == 200
    data = res.json()
    assert data["overall_legal_rating"] == "FULL_STATUTORY_COMPLIANCE (100%)"
