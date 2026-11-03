"""
Unit tests for KAVACH Registered Tools Engine (app/agent/tools.py).
Verifies real tool operations, workspace containment, permissions, and security.
"""

import os
import pytest
from app.agent.tools import (
    repo_list_tree,
    repo_read_file,
    repo_search_code,
    security_scan_code,
    ast_analyze_impact,
    run_allowlisted_tests,
    propose_code_patch,
    apply_approved_patch,
    TOOLS_REGISTRY,
    TOOL_SCHEMAS,
)


def test_tools_registry_contains_all_schemas():
    """Verify registry maps match defined schemas."""
    schema_names = {s["name"] for s in TOOL_SCHEMAS}
    registry_names = set(TOOLS_REGISTRY.keys())
    assert schema_names == registry_names
    assert len(registry_names) >= 9
    assert "multimodal_inspect_image" in registry_names


def test_repo_list_tree_valid():
    """Verify repo_list_tree returns real files under permitted path."""
    res = repo_list_tree("01_KAVACH_Platform/backend/app/agent", max_depth=1)
    assert res["success"] is True
    assert res["total_items"] > 0
    paths = [item["path"] for item in res["items"]]
    assert any("tools.py" in p for p in paths)


def test_repo_read_file_slicing():
    """Verify repo_read_file reads specific line slices."""
    res = repo_read_file("01_KAVACH_Platform/backend/app/agent/tools.py", start_line=1, end_line=10)
    assert res["success"] is True
    assert res["start_line"] == 1
    assert res["end_line"] == 10
    assert "Registered Tools Engine" in res["raw_text"]


def test_repo_read_file_path_traversal_blocked():
    """Verify path traversal outside workspace is blocked."""
    with pytest.raises(PermissionError):
        repo_read_file("../../windows/system32/cmd.exe")


def test_repo_search_code_literal():
    """Verify searching code locates real occurrences."""
    res = repo_search_code("run_allowlisted_tests", "01_KAVACH_Platform/backend/app/agent")
    assert res["success"] is True
    assert res["match_count"] >= 1
    files = [m["file"] for m in res["matches"]]
    assert any("tools.py" in f for f in files)


def test_security_scan_code_detects_credentials():
    """Verify security scan detects PII and high-entropy credentials."""
    sample = "Aadhaar: 9876 5432 1098 and AWS_KEY = AKIAIOSFODNN7EXAMPLE"
    res = security_scan_code(sample)
    assert res["success"] is True
    assert res["findings_count"] == 2
    assert res["is_safe"] is False
    assert res["has_critical_findings"] is True


def test_ast_analyze_impact_computes_blast_radius():
    """Verify AST analysis computes dependency blast radius."""
    res = ast_analyze_impact("app/security/detector.py")
    assert res["success"] is True
    assert res["total_affected_files"] >= 1
    assert 0.0 <= res["blast_radius_score"] <= 1.0


def test_run_allowlisted_tests_executes_real_pytest():
    """Verify real pytest execution on allowlisted path."""
    res = run_allowlisted_tests(
        "01_KAVACH_Platform/tests/test_api_endpoints.py",
        filter_keyword="test_health",
        timeout_seconds=20,
    )
    assert res["success"] is True
    assert res["exit_code"] == 0
    assert res["passed"] is True
    assert res["duration_ms"] > 0
    assert "test_health" in res["stdout"] or "passed" in res["stdout"]


def test_run_allowlisted_tests_blocks_disallowed_paths():
    """Verify attempts to run unapproved paths are rejected."""
    res = run_allowlisted_tests("/etc/passwd")
    assert res["success"] is False
    assert "outside allowlisted" in res["error"]


def test_propose_and_apply_patch_requires_approval():
    """Verify patch generation and human approval gate."""
    target_file = "01_KAVACH_Platform/backend/app/agent/planner.py"
    res = repo_read_file(target_file)
    original_text = res["raw_text"]

    modified_text = original_text + "\n# Verified Patch Line\n"
    patch_res = propose_code_patch(target_file, modified_text, change_rationale="Adding audit comment")
    assert patch_res["success"] is True
    assert patch_res["status"] == "AWAITING_APPROVAL"
    assert "+# Verified Patch Line" in patch_res["diff"]

    # Blocked without approval token
    blocked_apply = apply_approved_patch(target_file, modified_text, approval_token="")
    assert blocked_apply["success"] is False
    assert "Human approval required" in blocked_apply["error"]
