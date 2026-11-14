"""
Comprehensive Unit Tests for KAVACH Stage 3:
AST Semantic Vulnerability & Supply-Chain Slopsquatting Graph Traversal.
Course: CSE3101 Agentic AI - Capstone Project (BML Munjal University)
Student: Dhruv Jain (230532)
"""

import pytest
from kavach_agent_core.ast_analyzer import (
    damerau_levenshtein_distance,
    check_supply_chain_slopsquatting,
    AdvancedASTTaintVisitor,
    analyze_ast_and_supply_chain,
    VERIFIED_PYPI_REGISTRY,
)


def test_damerau_levenshtein_distance_metric_properties():
    """Verify Damerau-Levenshtein distance satisfies metric axioms and adjacent transposition."""
    # Identity
    assert damerau_levenshtein_distance("requests", "requests") == 0
    assert damerau_levenshtein_distance("numpy", "numpy") == 0

    # Substitution (cost = 1)
    assert damerau_levenshtein_distance("fastapi", "fastapiX") == 1
    assert damerau_levenshtein_distance("flask", "flakk") == 1

    # Deletion (cost = 1)
    assert damerau_levenshtein_distance("colorama", "colorma") == 1

    # Adjacent Transposition (cost = 1 in Damerau-Levenshtein, vs 2 in standard Levenshtein)
    assert damerau_levenshtein_distance("requests", "reqeusts") == 1
    assert damerau_levenshtein_distance("pydantic", "pydnatio") == 2


def test_supply_chain_slopsquatting_audit():
    """Verify CWE-1395 detection on typosquatted / slopsquatted dependencies."""
    # Legitimate packages pass without alert
    assert check_supply_chain_slopsquatting("requests") is None
    assert check_supply_chain_slopsquatting("numpy") is None
    assert check_supply_chain_slopsquatting("fastapi") is None

    # Typosquatted / Slopsquatted packages get flagged
    alert_colorma = check_supply_chain_slopsquatting("colorma")
    assert alert_colorma is not None
    assert alert_colorma["cwe_id"] == "CWE-1395"
    assert alert_colorma["spoofed_target"] == "colorama"
    assert alert_colorma["damerau_levenshtein_distance"] == 1

    alert_reqeusts = check_supply_chain_slopsquatting("reqeusts")
    assert alert_reqeusts is not None
    assert alert_reqeusts["spoofed_target"] == "requests"
    assert alert_reqeusts["damerau_levenshtein_distance"] == 1


def test_ast_taint_reachability_dag():
    """Verify AST data-flow lattice tracks untrusted source to critical sinks."""
    vulnerable_snippet = """
import os
import pickle

def process_webhook(user_input):
    payload = user_input
    eval(payload)
    os.system("cat " + payload)
    pickle.loads(payload)
"""
    result = analyze_ast_and_supply_chain(vulnerable_snippet)
    assert result["success"] is True
    assert result["is_safe"] is False
    assert result["sinks_found_count"] >= 3

    sink_types = {s["type"] for s in result["sinks"]}
    assert "CWE-94_ARBITRARY_CODE_EXECUTION" in sink_types
    assert "CWE-78_COMMAND_INJECTION" in sink_types
    assert "CWE-502_INSECURE_DESERIALIZATION" in sink_types

    # Verify graph lattice structure
    lattice = result["graph_lattice"]
    assert lattice["nodes_count"] > 0
    assert lattice["edges_count"] > 0


def test_ast_safe_code_certified():
    """Verify benign, safe Python code passes with invariant certification."""
    safe_snippet = """
import math
import numpy as np

def calculate_hypotenuse(a, b):
    # Pure deterministic computation with zero dynamic sinks
    return math.sqrt(a**2 + b**2)
"""
    result = analyze_ast_and_supply_chain(safe_snippet)
    assert result["success"] is True
    assert result["is_safe"] is True
    assert result["total_vulnerabilities_count"] == 0
    assert result["mathematical_invariant"]["satisfied"] is True
