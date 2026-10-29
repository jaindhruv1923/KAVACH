"""
Test Suite: Frontier Agentic AI Paradigms Verification.
Validates:
1. Language Agent Tree Search (LATS / MCTS) with UCT argmax, rollouts, and value backpropagation.
2. Dual-Tier Reflexion Memory (Episodic-to-Semantic Cognitive Consolidation) and Plan Veto Gate.
"""

import os
import sys
import pytest

# Ensure backend app is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "backend")))

from app.agent.lats_planner import LATSPlanner, LATSNode
from app.agent.reflexion_memory import ReflexionMemoryEngine, SemanticInvariant, global_reflexion_memory


def test_lats_planner_search_and_pruning():
    """Verify that LATS explores multiple candidate branches, prunes insecure ones, and converges."""
    planner = LATSPlanner(exploration_constant=1.414, max_depth=2)

    result = planner.search(
        problem="Securely disburse vendor payment and audit third-party AST imports",
        iterations=10,
        domain="banking"
    )

    assert result["algorithm"] == "Language Agent Tree Search (LATS / MCTS)"
    assert result["academic_reference"] == "Zhou et al., ICML 2024"
    assert result["status"] == "CONVERGED_OPTIMAL_PATH"
    assert result["total_nodes_explored"] >= 4
    assert result["branches_pruned"] >= 1  # Verify that bypass/hazardous actions were pruned
    assert len(result["optimal_trajectory"]) > 0
    assert result["winning_q_value"] > 0.0


def test_reflexion_memory_verbal_reinforcement_and_veto():
    """Verify that failed episodes synthesize permanent verbal semantic rules and veto bad plans."""
    engine = ReflexionMemoryEngine()

    # Record a failed episode (simulated slopsquatting import attempt)
    ep_res = engine.record_episode(
        task_id="TASK-992",
        goal="Install fast_jwt_vault_security for authentication",
        trajectory=[{"step": "pip install", "action": "install unverified package"}],
        outcome="FAILURE",
        error_context="404 on PyPI: Package 'fast_jwt_vault_security' is unregistered slopsquat",
        domain="devops"
    )

    assert ep_res["outcome"] == "FAILURE"
    assert ep_res["consolidated_lesson"] is not None
    assert "Supply-chain warning" in ep_res["consolidated_lesson"]["verbal_reflection"]

    # Test pre-execution plan evaluation against learned invariants
    bad_plan = ["pip install fast_jwt_vault_security without verify", "run test"]
    veto_res = engine.evaluate_plan_against_invariants(bad_plan, domain="devops")

    assert veto_res["cognitive_veto_approved"] is False
    assert veto_res["total_violations_found"] >= 1
    assert veto_res["status"] == "COGNITIVELY_BLOCKED_FOR_CORRECTION"

    # Test clean plan passes veto
    clean_plan = ["verify package on pypi registry", "tokenize sensitive data", "run ephemeral pytest"]
    clean_veto = engine.evaluate_plan_against_invariants(clean_plan, domain="devops")
    assert clean_veto["cognitive_veto_approved"] is True

