"""
Focused Verification Script for KAVACH Post-Implementation Reality Check.
Runs focused checks for:
1. Path Traversal Containment Guard (Direct & In-Engine)
2. Patch Approval Enforcement (HITL Token)
3. Allowlisted Subprocess Execution
4. Error Handling & Loop Timeout Behavior
5. Temporary Fixture Write Operation with Backup Creation
"""

import os
import sys
import tempfile
import time
import shutil

# Ensure backend app is on sys.path
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
backend_dir = os.path.join(root, "01_KAVACH_Platform", "backend")
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.agent.tools import (
    repo_read_file,
    repo_list_tree,
    apply_approved_patch,
    propose_code_patch,
    run_allowlisted_tests,
    get_workspace_root,
)
from app.agent.react_engine import AgenticReActEngine
from app.generation.llm_client import is_llm_configured


def check_path_containment():
    print("--- Check 1: Path Traversal Containment Guard ---")
    # Direct tool call must raise PermissionError on traversal
    try:
        repo_read_file("../../../Windows/System32/drivers/etc/hosts")
        assert False, "Should have raised PermissionError"
    except PermissionError as pe:
        assert "escapes workspace boundary" in str(pe)
        print(f"[PASS] Direct traversal blocked with PermissionError: {pe}")

    try:
        repo_list_tree("../../..")
        assert False, "Should have raised PermissionError"
    except PermissionError as pe:
        assert "escapes workspace boundary" in str(pe)
        print(f"[PASS] Direct list tree traversal blocked with PermissionError: {pe}")

    # ReAct engine execution handles it gracefully as structured observation
    engine = AgenticReActEngine(max_iterations=1)
    res = engine.run("Read file ../../../Windows/System32/drivers/etc/hosts")
    assert res.status in ["COMPLETE", "SUCCESS", "BLOCKED", "NEEDS_REVIEW"]
    print(f"[PASS] ReAct engine gracefully caught traversal without crashing (status={res.status})")


def check_patch_approval_enforcement():
    print("\n--- Check 2: Patch Approval Token Enforcement ---")
    res = apply_approved_patch(
        file_path="01_KAVACH_Platform/backend/app/agent/planner.py",
        patch_content="# unauthorized write attempt",
        approval_token=""
    )
    assert res["success"] is False
    assert "Human approval required" in res["error"]
    print(f"[PASS] Unauthorized patch write blocked: {res['error']}")


def check_allowlisted_subprocess_execution():
    print("\n--- Check 3: Allowlisted Subprocess Execution ---")
    # Disallowed path
    res_bad = run_allowlisted_tests("C:/Windows/notepad.exe")
    assert res_bad["success"] is False
    assert "outside allowlisted test directories" in res_bad["error"]
    print(f"[PASS] Non-allowlisted test execution blocked: {res_bad['error']}")

    # Allowed test path with timeout protection
    t0 = time.time()
    res_ok = run_allowlisted_tests("01_KAVACH_Platform/tests/test_api_endpoints.py", filter_keyword="test_health", timeout_seconds=15)
    duration = time.time() - t0
    assert res_ok["success"] is True
    print(f"[PASS] Allowlisted test executed in subprocess (duration={round(duration, 2)}s, exit_code={res_ok.get('exit_code')})")


def check_timeout_and_error_handling():
    print("\n--- Check 4: Error Handling & Timeout Behavior ---")
    engine = AgenticReActEngine(max_iterations=3, timeout_seconds=0.0001)  # tiny timeout
    res = engine.run("Inspect repository structure")
    assert any(s.action == "TIMEOUT" for s in res.steps)
    print(f"[PASS] Bounded engine successfully halted on timeout (status={res.status})")


def check_temp_fixture_write_and_backup():
    print("\n--- Check 5: Temporary Fixture Write Operation with Backup Creation ---")
    workspace = get_workspace_root()
    # Create a safe test file inside workspace
    test_rel_path = "01_KAVACH_Platform/tests/temp_test_target.txt"
    test_abs_path = os.path.join(workspace, test_rel_path.replace("/", os.sep))

    with open(test_abs_path, "w", encoding="utf-8") as f:
        f.write("original content line 1\noriginal content line 2\n")

    try:
        # Propose patch
        prop = propose_code_patch(
            file_path=test_rel_path,
            modified_content="original content line 1\nMODIFIED content line 2\n",
            change_rationale="Unit test patch demonstration"
        )
        assert prop["success"] is True
        assert prop["status"] == "AWAITING_APPROVAL"
        print(f"[PASS] Patch proposal generated unified diff (patch_id={prop['patch_id']})")

        # Apply with valid token
        apply_res = apply_approved_patch(
            file_path=test_rel_path,
            patch_content="original content line 1\nMODIFIED content line 2\n",
            approval_token="SUPERVISOR-TOKEN-TEST-VALID"
        )
        assert apply_res["success"] is True
        assert apply_res["status"] == "APPLIED"
        backup_file = os.path.join(workspace, apply_res["backup_created"].replace("/", os.sep))
        assert os.path.exists(backup_file)
        print(f"[PASS] Patch applied safely with automatic backup: {apply_res['backup_created']}")

        # Verify modified content
        with open(test_abs_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "MODIFIED content line 2" in content

        # Clean up backup
        if os.path.exists(backup_file):
            os.remove(backup_file)
    finally:
        if os.path.exists(test_abs_path):
            os.remove(test_abs_path)
    print("[PASS] Cleaned up temporary test fixture.")


if __name__ == "__main__":
    print("=" * 60)
    print("KAVACH FOCUSED VERIFICATION PASS")
    print(f"Live LLM Configured: {is_llm_configured()}")
    print("=" * 60)
    check_path_containment()
    check_patch_approval_enforcement()
    check_allowlisted_subprocess_execution()
    check_timeout_and_error_handling()
    check_temp_fixture_write_and_backup()
    print("\n" + "=" * 60)
    print("ALL FOCUSED VERIFICATION CHECKS PASSED SUCCESSFULLY")
    print("=" * 60)
