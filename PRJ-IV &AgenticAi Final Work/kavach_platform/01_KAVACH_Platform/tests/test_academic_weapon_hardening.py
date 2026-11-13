"""
Test Suite: Academic Weapon Hardening & Defense Verifications.
Validates:
1. Dynamic AST Import Interception (__import__, importlib.import_module).
2. Finite-State Cyclic Regression Loop Termination in ReAct Self-Healer.
3. Multi-Agent Dual-Custody Multi-Sig Transfer (Segregation of Duties).
4. Dual-Custody REST Endpoint with Cryptographic Attestation Stamps.
"""

import pytest
import os
import sys

# Ensure app is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))
banking_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "02_Banking_and_Results_Dashboard", "implementation_banks"))
sys.path.insert(0, banking_dir)

from app.security.package_firewall import extract_imported_packages
from app.agent.self_healer import autonomous_self_heal
from core_banking import CoreBankingEngine
from fastapi.testclient import TestClient
from server import app


def test_dynamic_ast_import_interception():
    """Verify that AST package firewall intercepts dynamic imports alongside static ones."""
    code_with_dynamic_imports = '''
import math
from fastapi import FastAPI

def load_payload():
    mod1 = __import__("slopsquatted_dynamic_pkg")
    import importlib
    mod2 = importlib.import_module("adversarial_supply_chain_pkg")
    return mod1, mod2
'''
    pkgs = extract_imported_packages(code_with_dynamic_imports)
    assert "math" in pkgs
    assert "fastapi" in pkgs
    assert "importlib" in pkgs
    assert "slopsquatted_dynamic_pkg" in pkgs
    assert "adversarial_supply_chain_pkg" in pkgs


def test_cyclic_regression_detection_terminates_loop():
    """Verify that ReAct self-healer aborts immediately when oscillating into a cyclic patch."""
    broken_code = "def solve(x):\n    return x + 1\n"
    test_suite = "import unittest\nclass T(unittest.TestCase):\n    def test_one(self):\n        self.assertEqual(solve(2), 5)\n"

    # Mock an LLM that repeatedly returns the exact same non-convergent code
    def oscillating_mock_llm(prompt: str) -> str:
        return "```python\ndef solve(x):\n    return x + 2\n```"

    result = autonomous_self_heal(
        code=broken_code,
        test_code=test_suite,
        max_iterations=5,
        custom_llm_fn=oscillating_mock_llm
    )

    assert result["success"] is False
    assert result["status"] == "CYCLIC_REGRESSION_BLOCKED"
    assert "cyclic regression" in result["verdict"].lower()


def test_dual_custody_transfer_missing_signatures():
    """Verify that high-value dual custody transfers fail or hold if either signature is missing."""
    engine = CoreBankingEngine()
    
    # 1. Missing initiator signature
    res1 = engine.execute_dual_custody_transfer(
        sender_acc="SBIN00012345678",
        receiver_acc="ICIC00045678901",
        amount=5000.0,
        initiator_agent_sig="",
        cosigner_auditor_sig="A2A-SIG-CREWAI-12345"
    )
    assert res1["status"] == "FAILED_DUAL_CUSTODY"

    # 2. Missing cosigner signature
    res2 = engine.execute_dual_custody_transfer(
        sender_acc="SBIN00012345678",
        receiver_acc="ICIC00045678901",
        amount=5000.0,
        initiator_agent_sig="A2A-SIG-ADK-98765",
        cosigner_auditor_sig=""
    )
    assert res2["status"] == "DUAL_CUSTODY_PENDING_APPROVAL"


def test_dual_custody_transfer_both_signatures_approved():
    """Verify that transfer succeeds and attaches attestation when both signatures are valid."""
    engine = CoreBankingEngine()
    res = engine.execute_dual_custody_transfer(
        sender_acc="SBIN00012345678",
        receiver_acc="ICIC00045678901",
        amount=100.0,
        initiator_agent_sig="A2A-SIG-ADK-7F9B1C2D",
        cosigner_auditor_sig="A2A-SIG-CREWAI-83A4E21F",
        memo="Settlement of vendor invoice"
    )
    assert res["status"] == "SUCCESS"
    assert "dual_custody_attestation" in res
    assert res["dual_custody_attestation"]["consensus"] == "DUAL_AGENT_CONSENSUS_ACHIEVED"
    assert res["dual_custody_attestation"]["sod_compliance"] == "RBI-CYBER-FRAMEWORK-ANNEX-1"


def test_dual_custody_api_endpoint():
    """Verify the /api/dual-custody/transfer endpoint via FastAPI TestClient."""
    client = TestClient(app)
    payload = {
        "sender_acc": "SBIN00012345678",
        "receiver_acc": "ICIC00045678901",
        "amount": 200.0,
        "initiator_agent_sig": "A2A-SIG-ADK-GATEWAY",
        "cosigner_auditor_sig": "A2A-SIG-CREWAI-AUDITOR",
        "memo": "Authorized vendor payment",
        "transfer_type": "NEFT"
    }
    resp = client.post("/api/dual-custody/transfer", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "SUCCESS"
    assert "dual_custody_attestation" in data
