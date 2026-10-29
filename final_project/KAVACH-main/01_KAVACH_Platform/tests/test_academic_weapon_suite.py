"""
Comprehensive Test Suite: 10 Elite Academic Weapon Features for KAVACH
1. Differential Privacy Prompt Distillation (Dwork 2006)
2. Graph of Thoughts (GoT) Non-Linear Reasoning (Besta 2024)
3. Cryptographic Agent Watermarking (Kirchenbauer 2023)
4. Information Flow Security Lattice (Denning 1976)
5. Post-Quantum Cryptography State Sealing (NIST FIPS 204 ML-DSA)
6. Denial-of-Wallet & DoS Token Throttling (OWASP LLM04)
7. Semantic Factuality & NLI Cross-Entailment (Wang 2023)
8. Autonomous SAGA Inverse Compensation Stack (Garcia-Molina)
9. Causal Counterfactual XAI Explainer (Pearl 2009)
10. Scientific Ablation Study Matrix & Empirical Benchmarks
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

from app.security.differential_privacy import DifferentialPrivacyEngine
from app.agent.graph_of_thoughts_engine import GraphOfThoughtsEngine
from app.security.agent_watermarking import AgentWatermarkingEngine
from app.security.information_flow_lattice import InformationFlowLattice, SecurityClass
from app.security.pqc_quantum_shield import PostQuantumShieldEngine
from app.security.denial_of_wallet_guard import DenialOfWalletGuard
from app.security.factuality_entailment import FactualityEntailmentEngine
from app.security.saga_compensation_stack import SagaCompensationOrchestrator
from app.security.causal_xai_explainer import CausalXaiExplainer
from app.security.scientific_ablation import ScientificAblationEngine

client = TestClient(app)


# 1. Differential Privacy
def test_differential_privacy_noise_bounds():
    engine = DifferentialPrivacyEngine(epsilon=0.5)
    raw_vals = [100.0, 200.0, 300.0]
    privatized = engine.privatize_numeric_features(raw_vals)
    assert len(privatized) == 3
    # Check bounded perturbation
    res = engine.privatize_prompt_representation("def process_payment(account_id): return True")
    assert res["privacy_guaranteed"] is True
    assert res["max_divergence_bound"] > 1.0

    # Test via API
    api_res = client.post("/api/v1/privacy/distill", json={"raw_prompt": "secret internal vendor query", "epsilon": 0.5})
    assert api_res.status_code == 200
    assert api_res.json()["privacy_guaranteed"] is True


# 2. Graph of Thoughts (GoT)
def test_graph_of_thoughts_reasoning_and_cycle_prevention():
    engine = GraphOfThoughtsEngine()
    flow = engine.execute_reasoning_flow("Audit vendor package and authorize dual-custody escrow")
    assert flow["status"] == "CONVERGED_OPTIMAL"
    assert flow["cyclic_recursion_detected"] is False
    assert flow["total_nodes_generated"] >= 4

    # Test via API
    api_res = client.post("/api/v1/got/reason", json={"problem": "Verify AST and Escrow"})
    assert api_res.status_code == 200
    assert api_res.json()["status"] == "CONVERGED_OPTIMAL"


# 3. Cryptographic Agent Watermarking
def test_agent_watermarking_kirchenbauer_z_score():
    engine = AgentWatermarkingEngine()
    test_text = "The autonomous security agent verified the cryptographic signature and committed the transaction safely."
    res = engine.watermark_text(test_text)
    assert res["watermark_algorithm"].startswith("Kirchenbauer")
    assert "z_score" in res
    assert res["total_tokens_evaluated"] > 5

    # Test via API
    api_res = client.post("/api/v1/watermark/verify", json={"text": test_text})
    assert api_res.status_code == 200
    assert "z_score" in api_res.json()


# 4. Information Flow Security Lattice
def test_information_flow_lattice_denning_model():
    lattice = InformationFlowLattice()
    
    # Allowed flow: Internal -> Confidential
    flow_ok = lattice.audit_flow("vendor_invoice", "audit_log", SecurityClass.CONFIDENTIAL)
    assert flow_ok["flow_permitted"] is True

    # Blocked declassification: Top Secret -> Public
    flow_bad = lattice.audit_flow("api_key", "public_readme", SecurityClass.PUBLIC)
    assert flow_bad["flow_permitted"] is False
    assert "ILLEGAL_INFORMATION_DECLASSIFICATION_BLOCKED" in flow_bad["verdict"]

    # Test via API
    api_res = client.post("/api/v1/lattice/audit", json={
        "source_var": "api_key",
        "sink_channel": "public_readme",
        "sink_level": 1
    })
    assert api_res.status_code == 200
    assert api_res.json()["flow_permitted"] is False


# 5. Post-Quantum Cryptography State Sealing
def test_post_quantum_cryptographic_dilithium_seal():
    pqc = PostQuantumShieldEngine(security_level=5)
    seal = pqc.generate_quantum_sealed_digest("KAVACH-IMMUTABLE-LEDGER-BLOCK-001")
    assert seal["shor_algorithm_resilient"] is True
    assert len(seal["polynomial_vectors"]) == 8
    assert seal["pqc_signature_seal"].startswith("ML-DSA-5-")

    # Test via API
    api_res = client.post("/api/v1/pqc/seal", json={"payload": "Test payload"})
    assert api_res.status_code == 200
    assert api_res.json()["shor_algorithm_resilient"] is True


# 6. Denial-of-Wallet (DoW) Protection
def test_denial_of_wallet_token_bucket_circuit_breaker():
    dow = DenialOfWalletGuard(max_tokens_per_minute=20000, max_cost_budget_usd=1.0)
    
    # Normal request
    r1 = dow.audit_token_consumption(estimated_tokens=5000, estimated_cost_usd=0.10)
    assert r1["allowed"] is True
    assert r1["verdict"] == "BUDGET_APPROVED"

    # Velocity spike breach
    r2 = dow.audit_token_consumption(estimated_tokens=25000, estimated_cost_usd=0.20)
    assert r2["allowed"] is False
    assert r2["verdict"] == "TOKEN_VELOCITY_BREACH"

    # Test via API
    api_res = client.post("/api/v1/dow/audit", json={"estimated_tokens": 5000, "estimated_cost_usd": 0.05})
    assert api_res.status_code == 200
    assert api_res.json()["allowed"] is True


# 7. Semantic Factuality & Entailment
def test_factuality_entailment_grounding():
    engine = FactualityEntailmentEngine()
    
    # Entailed claim
    c1 = engine.verify_action_entailment("The transfer is subject to RBI 50000 INR dual custody mandates.", "rbi_ceiling")
    assert c1["entailment_relationship"] == "ENTAILMENT"

    # Contradictory claim
    c2 = engine.verify_action_entailment("Executing 100000 INR transfer without dual custody approval.", "rbi_ceiling")
    assert c2["entailment_relationship"] == "CONTRADICTION"
    assert c2["verdict"] == "FACTUALITY_VETO"

    # Test via API
    api_res = client.post("/api/v1/factuality/verify", json={"claim": "Pre-execution Sentinel enforces Shannon entropy threshold of 4.50 bits per character.", "domain": "shannon_threshold"})
    assert api_res.status_code == 200
    assert api_res.json()["entailment_relationship"] == "ENTAILMENT"


# 8. SAGA Autonomous Inverse Compensation Stack
def test_saga_compensation_stack_atomic_unwind():
    orchestrator = SagaCompensationOrchestrator()
    unwound_actions = []

    orchestrator.register_step(
        "Step 1: Escrow Lock",
        lambda: True,
        lambda: unwound_actions.append("ESCROW_RELEASED") or True
    )
    orchestrator.register_step(
        "Step 2: Ephemeral Sandbox",
        lambda: True,
        lambda: unwound_actions.append("SANDBOX_CLEANED") or True
    )
    orchestrator.register_step(
        "Step 3: External API Call",
        lambda: False,  # Simulates network failure
        lambda: unwound_actions.append("API_SESSION_KILLED") or True
    )

    res = orchestrator.execute_saga()
    assert res["status"] == "SAGA_COMPENSATED_ROLLBACK"
    assert res["failure_step"] == "Step 3: External API Call"
    assert res["steps_compensated"] == 2
    # Verify inverse unwinding
    assert "SANDBOX_CLEANED" in unwound_actions
    assert "ESCROW_RELEASED" in unwound_actions

    # Test via API
    api_res = client.post("/api/v1/saga/unwind", json={"simulate_fail_at_step_3": True})
    assert api_res.status_code == 200
    assert api_res.json()["status"] == "SAGA_COMPENSATED_ROLLBACK"


# 9. Causal Counterfactual XAI Explainer
def test_causal_counterfactual_xai_explainer():
    explainer = CausalXaiExplainer()
    code_with_secret = "def transfer():\n    api_key = 'sk-live-93820194829019283019'\n    return True"
    res = explainer.compute_counterfactual_explanation(code_with_secret, "QUARANTINED")
    
    assert res["xai_framework"].startswith("Structural Causal Counterfactuals")
    assert res["counterfactual_target_verdict"] == "APPROVED"
    assert "Replace credential" in res["minimal_counterfactual_intervention"]

    # Test via API
    api_res = client.post("/api/v1/xai/counterfactual", json={"code": code_with_secret, "verdict": "QUARANTINED"})
    assert api_res.status_code == 200
    assert api_res.json()["counterfactual_target_verdict"] == "APPROVED"


# 10. Scientific Ablation Study Matrix
def test_scientific_ablation_study_matrix():
    ablation = ScientificAblationEngine()
    res = ablation.run_ablation_comparison()
    
    assert res["configurations_evaluated"] == 4
    assert "Full KAVACH Sovereign Engine" in res["configurations"]
    full_kavach = res["configurations"]["Full KAVACH Sovereign Engine"]
    assert full_kavach["f1_score"] > 0.99
    assert full_kavach["latency_ms"] < 1.0

    # Test via API
    api_res = client.get("/api/v1/ablation/matrix")
    assert api_res.status_code == 200
    assert api_res.json()["configurations_evaluated"] == 4
