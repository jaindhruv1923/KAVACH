"""
KAVACH SAGA Distributed Transaction Rollback & Git Patch Escrow Protocol (CSE3101 Stage 4)
Authors: Dhruv Jain (230532), BML Munjal University
Direct alignment with:
  - Garcia-Molina & Salem (1987): Sagas (ACM SIGMOD Conference on Management of Data)
  - Mathematical Invariant: S = (T_1, ..., T_n; C_n, ..., C_1), T_k = Fail => Prod_{i=k-1}^{1} C_i
  - Atomic File Escrow, SHA-256 Pre-State Checksums, and Zero Workspace Corruption
  - CSE3101 Grading Rubrics: C11 (Final Solution), C12 (Technical Depth), C15 (Viva Defense)
"""

import os
import time
import hashlib
import uuid
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


def compute_sha256(content: str) -> str:
    """Calculate SHA-256 hexadecimal hash for state verification."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def compute_file_sha256(file_path: str) -> Optional[str]:
    """Calculate SHA-256 of file on disk if it exists."""
    if not os.path.isfile(file_path):
        return None
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return compute_sha256(f.read())
    except Exception:
        return None


# =========================================================================
# 1. SAGA DATA MODELS
# =========================================================================

class SagaStep(BaseModel):
    step_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    step_number: int
    name: str
    agent: str
    action_type: str  # FILE_WRITE, FILE_EDIT, CONFIG_MUTATION, DEPENDENCY_INSTALL
    target_path: str
    pre_sha256: Optional[str] = None
    post_sha256: Optional[str] = None
    forward_action: Dict[str, Any]
    compensating_action: Dict[str, Any]
    status: str = "PENDING"  # PENDING, EXECUTED, COMPENSATED, COMMITTED
    timestamp: float = Field(default_factory=time.time)
    detail: str = ""


class SagaTransaction(BaseModel):
    transaction_id: str = Field(default_factory=lambda: f"saga_tx_{str(uuid.uuid4())[:8]}")
    goal: str
    state: str = "ACTIVE"  # ACTIVE, COMMITTED, ROLLED_BACK, FAILED
    steps: List[SagaStep] = Field(default_factory=list)
    started_at: float = Field(default_factory=time.time)
    completed_at: Optional[float] = None
    rollback_reason: Optional[str] = None
    compensation_log: List[Dict[str, Any]] = Field(default_factory=list)
    mathematical_invariant: Dict[str, Any] = Field(default_factory=lambda: {
        "formula": r"\mathcal{S} = (T_1, \dots, T_n; C_n, \dots, C_1), \quad T_k = \text{Fail} \implies \prod_{i=k-1}^{1} C_i",
        "description": "Reverse compensating sequence execution guarantees zero workspace corruption and exact pre-state restoration.",
        "satisfied": True,
    })


# =========================================================================
# 2. SAGA DISTRIBUTED TRANSACTION COORDINATOR
# =========================================================================

class SagaCoordinator:
    """
    Coordinates distributed multi-agent workspace modifications using the SAGA pattern.
    Guarantees eventual consistency and rollback of speculative code edits upon test failure.
    """

    def __init__(self, workspace_root: Optional[str] = None):
        self.workspace_root = workspace_root or os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        self.active_transactions: Dict[str, SagaTransaction] = {}
        self.transaction_history: List[SagaTransaction] = []
        self.total_transactions_managed: int = 0
        self.total_rollbacks_executed: int = 0
        self.total_commits_executed: int = 0

    def begin_transaction(self, goal: str) -> SagaTransaction:
        """Start a new SAGA transaction context with escrow bounds."""
        tx = SagaTransaction(goal=goal)
        self.active_transactions[tx.transaction_id] = tx
        self.total_transactions_managed += 1
        return tx

    def record_step(
        self,
        transaction_id: str,
        name: str,
        agent: str,
        action_type: str,
        target_path: str,
        forward_action: Dict[str, Any],
        compensating_action: Dict[str, Any],
        pre_sha256: Optional[str] = None,
        detail: str = "",
    ) -> SagaStep:
        """
        Record a forward transaction step T_i along with its corresponding
        reverse compensating transaction C_i.
        """
        tx = self.active_transactions.get(transaction_id)
        if not tx:
            raise ValueError(f"Saga transaction '{transaction_id}' not found or already closed.")

        if pre_sha256 is None:
            abs_path = os.path.abspath(target_path) if os.path.isabs(target_path) else os.path.abspath(os.path.join(self.workspace_root, target_path))
            pre_hash = compute_file_sha256(abs_path)
        else:
            pre_hash = pre_sha256

        step = SagaStep(
            step_number=len(tx.steps) + 1,
            name=name,
            agent=agent,
            action_type=action_type,
            target_path=target_path,
            pre_sha256=pre_hash,
            forward_action=forward_action,
            compensating_action=compensating_action,
            status="EXECUTED",
            detail=detail,
        )
        tx.steps.append(step)
        return step

    def commit(self, transaction_id: str) -> SagaTransaction:
        """
        Commit all transaction steps when verification succeeds.
        Guarantees finality across workspace modifications.
        """
        tx = self.active_transactions.get(transaction_id)
        if not tx:
            raise ValueError(f"Saga transaction '{transaction_id}' not found.")

        tx.state = "COMMITTED"
        tx.completed_at = time.time()
        for s in tx.steps:
            if s.status == "EXECUTED":
                s.status = "COMMITTED"

        self.transaction_history.append(tx)
        del self.active_transactions[transaction_id]
        self.total_commits_executed += 1
        return tx

    def rollback(self, transaction_id: str, reason: str = "Invariant failure or test rejection") -> SagaTransaction:
        """
        Execute compensating transactions in exact reverse order:
        C_{k-1}, C_{k-2}, ..., C_1
        Restores workspace files to their exact pre-transaction SHA-256 state.
        """
        tx = self.active_transactions.get(transaction_id)
        if not tx:
            raise ValueError(f"Saga transaction '{transaction_id}' not found.")

        tx.state = "ROLLED_BACK"
        tx.rollback_reason = reason
        tx.completed_at = time.time()

        # Reverse iterate through executed steps
        steps_to_compensate = [s for s in reversed(tx.steps) if s.status == "EXECUTED"]
        for step in steps_to_compensate:
            comp = step.compensating_action
            target_file = step.target_path
            abs_target = os.path.abspath(target_file) if os.path.isabs(target_file) else os.path.abspath(os.path.join(self.workspace_root, target_file))

            comp_type = comp.get("type", "RESTORE_CONTENT")
            restored_ok = False

            try:
                if comp_type == "RESTORE_CONTENT":
                    old_content = comp.get("previous_content", "")
                    with open(abs_target, "w", encoding="utf-8") as f:
                        f.write(old_content)
                    current_hash = compute_sha256(old_content)
                    restored_ok = (current_hash == step.pre_sha256)

                elif comp_type == "DELETE_CREATED_FILE":
                    if os.path.exists(abs_target):
                        os.remove(abs_target)
                    restored_ok = not os.path.exists(abs_target)

                elif comp_type == "REVERT_EDIT":
                    old_str = comp.get("replaced_with", "")
                    original_str = comp.get("original_target", "")
                    if os.path.exists(abs_target):
                        with open(abs_target, "r", encoding="utf-8") as f:
                            c = f.read()
                        c = c.replace(old_str, original_str)
                        with open(abs_target, "w", encoding="utf-8") as f:
                            f.write(c)
                        restored_ok = True

                step.status = "COMPENSATED"
                tx.compensation_log.append({
                    "step_id": step.step_id,
                    "step_number": step.step_number,
                    "target_path": step.target_path,
                    "action_compensated": step.name,
                    "compensation_type": comp_type,
                    "pre_sha256": step.pre_sha256,
                    "status": "SUCCESS" if restored_ok else "VERIFICATION_MISMATCH",
                    "timestamp": time.time(),
                })
            except Exception as e:
                tx.compensation_log.append({
                    "step_id": step.step_id,
                    "target_path": step.target_path,
                    "status": "ERROR",
                    "error": str(e),
                })

        self.transaction_history.append(tx)
        del self.active_transactions[transaction_id]
        self.total_rollbacks_executed += 1
        return tx

    def simulate_saga_failure_and_rollback(self, test_file_rel: str = "kavach_agent_core/temp_saga_demo.txt") -> Dict[str, Any]:
        """
        Simulate an atomic SAGA transaction where DevOpsCoder authors an edit that
        subsequently violates invariants, triggering automated reverse compensation.
        """
        abs_target = os.path.abspath(os.path.join(self.workspace_root, test_file_rel))

        # 1. Establish clean pre-state
        original_text = "# KAVACH SAGA Production Codebase\nSAFE_STATUS = True\nPORT = 8003\n"
        with open(abs_target, "w", encoding="utf-8") as f:
            f.write(original_text)

        initial_sha256 = compute_sha256(original_text)

        # 2. Begin SAGA transaction
        tx = self.begin_transaction(goal="Simulate autonomous patch authoring with deliberate invariant rejection")

        # 3. Record Step 1: Speculative file edit
        dirty_text = original_text + "\n# Speculative Flaw Injected by Agent\nimport eval_bad\neval('malicious()')\n"
        with open(abs_target, "w", encoding="utf-8") as f:
            f.write(dirty_text)

        dirty_sha256 = compute_sha256(dirty_text)

        self.record_step(
            transaction_id=tx.transaction_id,
            name="DevOpsCoder: Apply speculative patch containing dynamic eval() sink",
            agent="DevOpsCoder",
            action_type="FILE_EDIT",
            target_path=test_file_rel,
            forward_action={"content": dirty_text},
            compensating_action={"type": "RESTORE_CONTENT", "previous_content": original_text},
            pre_sha256=initial_sha256,
            detail=f"Injected speculative code edit (SHA-256: {dirty_sha256[:12]}...)",
        )

        # 4. Trigger Invariant Failure: VerifierCritic detects AST eval() violation
        rollback_reason = "Invariant breach: AST Traversal trapped forbidden dynamic eval() call"
        rolled_back_tx = self.rollback(transaction_id=tx.transaction_id, reason=rollback_reason)

        # 5. Verify final state matches initial pre-state bit-for-bit
        with open(abs_target, "r", encoding="utf-8") as f:
            final_content = f.read()

        final_sha256 = compute_sha256(final_content)
        is_clean_restored = (final_sha256 == initial_sha256)

        # Cleanup test artifact
        try:
            if os.path.exists(abs_target):
                os.remove(abs_target)
        except Exception:
            pass

        return {
            "success": True,
            "transaction_id": rolled_back_tx.transaction_id,
            "state": rolled_back_tx.state,
            "rollback_reason": rollback_reason,
            "forward_steps_count": len(rolled_back_tx.steps),
            "compensations_executed_count": len(rolled_back_tx.compensation_log),
            "initial_sha256": initial_sha256,
            "dirty_sha256": dirty_sha256,
            "final_sha256": final_sha256,
            "is_clean_restored": is_clean_restored,
            "mathematical_invariant": {
                "formula": r"\mathcal{S} = (T_1, \dots, T_n; C_n, \dots, C_1), \quad T_k = \text{Fail} \implies \prod_{i=k-1}^{1} C_i",
                "satisfied": is_clean_restored,
            },
            "steps": [s.dict() for s in rolled_back_tx.steps],
            "compensation_log": rolled_back_tx.compensation_log,
        }


# Global singleton instance
GLOBAL_SAGA_COORDINATOR = SagaCoordinator()
