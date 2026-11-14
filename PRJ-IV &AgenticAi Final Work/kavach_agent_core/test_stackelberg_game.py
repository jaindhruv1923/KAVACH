"""
Unit tests for Stackelberg Security Game & Dynamic Token Bucket Ingress Velocity Control.
Course: CSE3101 Agentic AI - Final Capstone Project
"""

import time
import pytest
from kavach_agent_core.stackelberg_game import (
    StackelbergSecurityGame,
    DynamicTokenBucket
)


def test_stackelberg_equilibrium_solution():
    """Verify Strong Stackelberg Equilibrium satisfies probability simplex and minimax bounds."""
    game = StackelbergSecurityGame()
    solution = game.solve_stackelberg_equilibrium()

    assert solution["status"] == "EQUILIBRIUM_SOLVED"
    strategy = solution["defense_allocation_s_star"]
    
    # 1. Invariant: Probability simplex sum(p_i) == 1.0
    total_prob = sum(strategy.values())
    assert abs(total_prob - 1.0) < 1e-3

    # 2. All probabilities non-negative
    for target, prob in strategy.items():
        assert prob >= 0.0

    # 3. PII Exfiltration has highest risk weight, so p(PII) should be highest
    assert strategy["PII_EXFILTRATION"] >= strategy["VELOCITY_RESOURCE_DOS"]

    # 4. Attacker best response exists in target vectors
    assert solution["attacker_best_response"] in game.TARGET_VECTORS
    assert "expected_defender_utility" in solution
    assert "expected_attacker_utility" in solution


def test_stackelberg_game_comparison_advantage():
    """Verify Stackelberg defense allocation reduces attacker payout relative to uniform defense."""
    game = StackelbergSecurityGame()
    comp = game.simulate_game_comparison()

    assert comp["success"] is True
    comparison = comp["comparison"]
    
    # Stackelberg allocation should provide a defender utility gain over uniform allocation
    assert comparison["defender_utility_gain"] >= 0.0
    assert comparison["attacker_utility_reduction"] >= 0.0


def test_token_bucket_consumption_and_burst():
    """Verify Token Bucket admits bursts up to capacity and rejects when exhausted."""
    bucket = DynamicTokenBucket(capacity=10.0, base_replenish_rate=2.0)
    
    # Consume within capacity
    admitted, meta = bucket.consume(tokens=5.0)
    assert admitted is True
    assert meta["remaining_tokens"] <= 5.1
    assert meta["total_admitted"] == 1

    # Consume another 5
    admitted2, meta2 = bucket.consume(tokens=5.0)
    assert admitted2 is True
    assert meta2["remaining_tokens"] <= 0.2

    # Now bucket is virtually empty, 3 tokens should be rejected
    admitted3, meta3 = bucket.consume(tokens=3.0)
    assert admitted3 is False
    assert meta3["total_rejected"] >= 1
    assert meta3["retry_after_sec"] > 0.0


def test_token_bucket_threat_modulation_and_replenish():
    """Verify rate modulation under adversarial threat level theta."""
    bucket = DynamicTokenBucket(capacity=15.0, base_replenish_rate=10.0, throttle_decay=0.8)
    
    # At threat level 0.0, effective rate = 10.0
    bucket.set_threat_level(0.0)
    assert bucket.effective_rate == 10.0

    # At threat level 1.0, effective rate = 10.0 * (1 - 0.8) = 2.0
    bucket.set_threat_level(1.0)
    assert bucket.effective_rate == 2.0

    status = bucket.get_status()
    assert status["status"] == "ACTIVE"
    assert status["threat_level_theta"] == 1.0
    assert status["effective_rate_per_sec"] == 2.0
