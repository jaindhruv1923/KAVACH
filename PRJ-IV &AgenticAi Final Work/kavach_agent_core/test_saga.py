"""
Comprehensive Unit Tests for KAVACH Stage 4:
Autonomous SAGA Distributed Transaction Rollback & Git Patch Escrow Protocol.
Course: CSE3101 Agentic AI - Capstone Project (BML Munjal University)
Student: Dhruv Jain (230532)
"""

import os
import pytest
from kavach_agent_core.saga_engine import (
    SagaCoordinator,
    compute_sha256,
    compute_file_sha256,
    GLOBAL_SAGA_COORDINATOR,
)


def test_saga_begin_and_commit(tmp_path):
    """Verify standard forward execution and atomic commit when invariants pass."""
    coordinator = SagaCoordinator(workspace_root=str(tmp_path))
    tx = coordinator.begin_transaction(goal="Apply verified security patch to auth.py")
    assert tx.state == "ACTIVE"

    test_file = tmp_path / "auth.py"
    test_file.write_text("def authenticate(): return True\n", encoding="utf-8")

    # Record step
    step = coordinator.record_step(
        transaction_id=tx.transaction_id,
        name="Update auth logic",
        agent="DevOpsCoder",
        action_type="FILE_EDIT",
        target_path="auth.py",
        forward_action={"content": "def authenticate(): return True\n"},
        compensating_action={"type": "RESTORE_CONTENT", "previous_content": "def authenticate(): return False\n"},
    )
    assert step.status == "EXECUTED"

    committed_tx = coordinator.commit(tx.transaction_id)
    assert committed_tx.state == "COMMITTED"
    assert committed_tx.completed_at is not None
    assert committed_tx.steps[0].status == "COMMITTED"


def test_saga_reverse_compensating_rollback(tmp_path):
    """
    Verify that upon failure, compensating transactions execute in exact reverse order
    (C_2 then C_1) and restore file state bit-for-bit to pre-transaction SHA-256 hash.
    """
    coordinator = SagaCoordinator(workspace_root=str(tmp_path))
    test_file = tmp_path / "banking_ledger.py"
    initial_code = "# Initial Clean Ledger\nBALANCE = 1000\n"
    test_file.write_text(initial_code, encoding="utf-8")
    initial_sha = compute_sha256(initial_code)

    tx = coordinator.begin_transaction(goal="Modify banking transaction limits")

    # Step 1: Change balance
    step1_code = "# Step 1 Modified Ledger\nBALANCE = 5000\n"
    test_file.write_text(step1_code, encoding="utf-8")
    coordinator.record_step(
        transaction_id=tx.transaction_id,
        name="Step 1: Increase balance limit",
        agent="DevOpsCoder",
        action_type="FILE_EDIT",
        target_path="banking_ledger.py",
        forward_action={"content": step1_code},
        compensating_action={"type": "RESTORE_CONTENT", "previous_content": initial_code},
    )

    # Step 2: Inject faulty code
    step2_code = step1_code + "\neval('exploit()')\n"
    test_file.write_text(step2_code, encoding="utf-8")
    coordinator.record_step(
        transaction_id=tx.transaction_id,
        name="Step 2: Add dynamic routing hook",
        agent="DevOpsCoder",
        action_type="FILE_EDIT",
        target_path="banking_ledger.py",
        forward_action={"content": step2_code},
        compensating_action={"type": "RESTORE_CONTENT", "previous_content": initial_code},
    )

    assert len(tx.steps) == 2

    # VerifierCritic rejects step 2 -> Trigger SAGA Rollback
    rb_tx = coordinator.rollback(tx.transaction_id, reason="VerifierCritic rejected build: AST eval() detected")
    assert rb_tx.state == "ROLLED_BACK"
    assert len(rb_tx.compensation_log) == 2

    # Verify reverse compensation order: Step 2 compensated first, then Step 1
    assert rb_tx.compensation_log[0]["step_number"] == 2
    assert rb_tx.compensation_log[1]["step_number"] == 1

    # Verify bit-for-bit restoration
    restored_code = test_file.read_text(encoding="utf-8")
    restored_sha = compute_sha256(restored_code)
    assert restored_sha == initial_sha
    assert restored_code == initial_code


def test_saga_delete_file_compensation(tmp_path):
    """Verify that a speculative file created during a transaction is cleanly deleted on rollback."""
    coordinator = SagaCoordinator(workspace_root=str(tmp_path))
    tx = coordinator.begin_transaction(goal="Create speculative temporary microservice")

    speculative_file = tmp_path / "temp_speculative_service.py"
    speculative_file.write_text("print('rogue worker')\n", encoding="utf-8")
    assert speculative_file.exists()

    coordinator.record_step(
        transaction_id=tx.transaction_id,
        name="Create temp service",
        agent="DevOpsCoder",
        action_type="FILE_WRITE",
        target_path="temp_speculative_service.py",
        forward_action={"action": "created"},
        compensating_action={"type": "DELETE_CREATED_FILE"},
    )

    coordinator.rollback(tx.transaction_id, reason="Speculative build rejected")
    assert not speculative_file.exists(), "Speculative file must be cleanly deleted on rollback"


def test_saga_simulation_engine():
    """Verify the end-to-end SAGA simulation method."""
    res = GLOBAL_SAGA_COORDINATOR.simulate_saga_failure_and_rollback()
    assert res["success"] is True
    assert res["state"] == "ROLLED_BACK"
    assert res["is_clean_restored"] is True
    assert res["mathematical_invariant"]["satisfied"] is True
    assert res["compensations_executed_count"] >= 1
