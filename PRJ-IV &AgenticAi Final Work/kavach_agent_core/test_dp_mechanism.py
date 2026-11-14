"""
Comprehensive Unit Tests for KAVACH Stage 5:
Differential Privacy & Laplace Epsilon-Delta Noise Mechanism.
Course: CSE3101 Agentic AI - Capstone Project (BML Munjal University)
Student: Dhruv Jain (230532)
"""

import math
import pytest
from kavach_agent_core.differential_privacy import (
    sample_laplace,
    PrivacyBudgetAccountant,
    DifferentialPrivacyEngine,
    GLOBAL_DP_ENGINE,
)


def test_laplace_sampling_properties():
    """
    Verify Laplace random variable generation matches theoretical moments:
    Mean E[Y] = 0, Variance Var(Y) = 2*b^2.
    """
    b = 2.0
    samples = [sample_laplace(mu=0.0, b=b) for _ in range(3000)]
    mean = sum(samples) / len(samples)
    variance = sum((x - mean) ** 2 for x in samples) / len(samples)

    # Statistical bounds (p < 0.01 tolerance)
    assert abs(mean) < 0.25, f"Laplace mean {mean} deviates significantly from 0.0"
    expected_variance = 2.0 * (b ** 2)  # 8.0
    assert 6.0 < variance < 10.5, f"Laplace variance {variance} deviates from expected {expected_variance}"


def test_differential_privacy_aggregate_queries():
    """Verify COUNT, SUM, and AVG queries with calibrated sensitivity Delta f."""
    engine = DifferentialPrivacyEngine()
    engine.accountant.reset(new_budget=10.0)

    # 1. COUNT query (Delta f = 1.0)
    res_count = engine.query_dp_aggregate(query_type="COUNT", epsilon=0.5)
    assert res_count["success"] is True
    assert res_count["sensitivity"] == 1.0
    assert res_count["laplace_scale_b"] == 2.0  # 1.0 / 0.5
    assert res_count["mathematical_invariant"]["satisfied"] is True

    # 2. SUM query with clipping bound (Delta f = clipping_bound)
    clipping_bound = 50000.0
    res_sum = engine.query_dp_aggregate(query_type="SUM", epsilon=0.2, clipping_bound=clipping_bound)
    assert res_sum["success"] is True
    assert res_sum["sensitivity"] == clipping_bound
    assert res_sum["laplace_scale_b"] == clipping_bound / 0.2

    # 3. AVG query
    res_avg = engine.query_dp_aggregate(query_type="AVG", epsilon=1.0, clipping_bound=10000.0)
    assert res_avg["success"] is True
    assert res_avg["sensitivity"] > 0


def test_privacy_budget_sequential_composition():
    """Verify sequential composition theorem and budget exhaustion halt."""
    accountant = PrivacyBudgetAccountant(total_budget=1.0)
    assert accountant.remaining_budget == 1.0

    # Query 1: spend 0.4
    ok1 = accountant.consume_budget(0.4, "Query_1")
    assert ok1 is True
    assert accountant.remaining_budget == 0.6

    # Query 2: spend 0.5
    ok2 = accountant.consume_budget(0.5, "Query_2")
    assert ok2 is True
    assert accountant.remaining_budget == 0.1

    # Query 3: attempt to spend 0.3 (exceeds 0.1 remaining)
    ok3 = accountant.consume_budget(0.3, "Query_3")
    assert ok3 is False, "Accountant must reject query exceeding remaining budget"
    assert accountant.remaining_budget == 0.1


def test_dp_reconstruction_resistance_simulation():
    """Verify simulation of reconstruction attack resistance and variance."""
    engine = DifferentialPrivacyEngine()
    engine.accountant.reset(new_budget=5.0)

    sim = engine.simulate_reconstruction_resistance()
    assert sim["success"] is True
    assert len(sim["trials"]) == 3
    assert "privacy_guarantee" in sim
    assert engine.accountant.spent_budget > 0
