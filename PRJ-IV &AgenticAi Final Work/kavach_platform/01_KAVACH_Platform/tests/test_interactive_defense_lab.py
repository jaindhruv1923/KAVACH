"""
Unit & Integration Tests for KAVACH Academic Defense Lab Suite.
Verifies the 5 standout empirical viva capabilities:
1. Break & Heal Autonomous Self-Healing
2. Interactive ReAct Step Debugger
3. Live Red-Team Zero-Day Attack Simulation
4. 45-Sample Held-Out Benchmark & Scorecard
5. Multilingual Hinglish DevOps Intent Parser
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.agent.interactive_suite import (
    run_break_and_heal_demo,
    get_self_heal_scenarios,
    get_react_step,
    get_react_debugger_presets,
    simulate_red_team_attack,
    get_red_team_presets,
    run_held_out_evaluation,
    parse_multilingual_prompt
)


@pytest.fixture
def client():
    return TestClient(app)


def test_self_heal_break_and_heal():
    """Verify autonomous self-healing loop repairs uninitialized bug in 2 iterations."""
    res = run_break_and_heal_demo("rate_limiter_none_type")
    assert res["status"] == "HEALED"
    assert res["iterations_required"] == 2
    assert len(res["trajectory"]) == 4
    assert res["trajectory"][0]["status"] == "FAILED"
    assert res["trajectory"][3]["status"] == "PASSED"
    assert "patch_diff" in res["trajectory"][2]


def test_react_step_debugger():
    """Verify ReAct step debugger returns step metadata, thoughts, actions, and observations."""
    step0 = get_react_step("sql_injection_audit", 0)
    assert step0["step_index"] == 0
    assert step0["step"]["phase"] == "THOUGHT_1"
    assert "thought" in step0["step"]
    assert "action" in step0["step"]

    step4 = get_react_step("sql_injection_audit", 4)
    assert step4["is_final"] is True
    assert step4["step"]["phase"] == "FINAL_ANSWER"


def test_red_team_attack_interception():
    """Verify multi-tier defense intercepts slopsquatting, injection, and PII leaks."""
    # 1. Slopsquatting
    r_slop = simulate_red_team_attack("slopsquatting")
    assert r_slop["intercepted"] is True
    assert "AST Package Firewall" in r_slop["defense_layer"]

    # 2. Prompt Injection
    r_inj = simulate_red_team_attack("prompt_injection")
    assert r_inj["intercepted"] is True
    assert "Prompt Injection Shield" in r_inj["defense_layer"]

    # 3. DPDP PII Leak
    r_pii = simulate_red_team_attack("pii_leak")
    assert r_pii["intercepted"] is True
    assert "Sentinel Token Vault" in r_pii["defense_layer"]


def test_held_out_benchmark_eval():
    """Verify held-out evaluation processes all 45 cases and computes valid F1 score and Merkle root."""
    res = run_held_out_evaluation()
    assert res["total_test_cases"] == 45
    assert res["metrics"]["f1_score"] >= 0.90
    assert res["metrics"]["accuracy"] >= 0.90
    assert "merkle_root" in res["merkle_provenance"]
    assert len(res["cases"]) == 45


def test_multilingual_hinglish_parse():
    """Verify Hinglish engineering prompt normalizes to canonical technical task."""
    p1 = parse_multilingual_prompt("Bhai ek FastAPI rate limiter bana do jo Redis token bucket use kare")
    assert p1["detected_language"] == "Hinglish (Hindi-English Code-Mix)"
    assert p1["intent_category"] == "FASTAPI_RATE_LIMITER"
    assert "explanation_hindi" in p1
    assert "explanation_english" in p1


def test_api_endpoints_interactive_defense_lab(client):
    """Verify all 5 interactive HTTP endpoints return 200 with on-demand results."""
    # 1. Self heal
    r1 = client.post("/api/interactive/self-heal/run", json={"scenario_id": "rate_limiter_none_type"})
    assert r1.status_code == 200
    assert r1.json()["status"] == "HEALED"

    # 2. Step debugger
    r2 = client.get("/api/interactive/react/step?preset_id=sql_injection_audit&step_index=1")
    assert r2.status_code == 200
    assert "step" in r2.json()

    # 3. Attack playground
    r3 = client.post("/api/interactive/attack/simulate", json={"attack_type": "prompt_injection"})
    assert r3.status_code == 200
    assert r3.json()["intercepted"] is True

    # 4. Held out benchmark
    r4 = client.get("/api/interactive/benchmark/held-out")
    assert r4.status_code == 200
    assert r4.json()["total_test_cases"] == 45

    # 5. Multilingual
    r5 = client.post("/api/interactive/multilingual/parse", json={"prompt": "bhai database me aadhaar leak check karo"})
    assert r5.status_code == 200
    assert r5.json()["intent_category"] == "PII_TOKENIZATION_GUARD"
