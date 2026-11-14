"""
Unit test suite for KAVACH MCP Tool Registry.
Verifies all 11 tools execute against real files, real math, and real subprocesses.
"""

import os
import sys
import pytest

# Add parent path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kavach_agent_core.tools import (
    tool_list_files,
    tool_read_file,
    tool_write_file,
    tool_edit_file,
    tool_search_code,
    tool_run_python,
    tool_validate_aadhaar_verhoeff,
    tool_dpdp_tokenize,
    tool_entropy_secret_audit,
    tool_ast_security_scan,
    execute_tool,
    TOOL_REGISTRY,
    MCP_TOOL_SCHEMAS,
)


def test_tool_registry_schemas_consistency():
    """Verify that every registered tool has an MCP schema."""
    registered = set(TOOL_REGISTRY.keys())
    schema_names = set(s["name"] for s in MCP_TOOL_SCHEMAS)
    assert registered == schema_names, f"Mismatch: {registered ^ schema_names}"


def test_filesystem_tools(tmp_path):
    """Test file creation, reading, editing, and listing."""
    test_rel_file = "kavach_agent_core/temp_test_artifact.txt"
    
    # 1. Write file
    res_w = tool_write_file(test_rel_file, "Line 1: Hello Kavach\nLine 2: Sensitive Value\nLine 3: End")
    assert res_w["success"] is True
    assert res_w["bytes_written"] > 0

    # 2. Read file
    res_r = tool_read_file(test_rel_file, start_line=1, end_line=2)
    assert res_r["success"] is True
    assert "Hello Kavach" in res_r["content"]

    # 3. Edit file
    res_e = tool_edit_file(test_rel_file, "Sensitive Value", "Masked Value")
    assert res_e["success"] is True
    assert res_e["occurrences_replaced"] == 1

    # Verify edit
    res_r2 = tool_read_file(test_rel_file)
    assert "Masked Value" in res_r2["content"]

    # 4. Search file
    res_s = tool_search_code("Masked Value", search_path="kavach_agent_core")
    assert res_s["success"] is True
    assert res_s["total_matches"] >= 1

    # Cleanup temp artifact
    try:
        from kavach_agent_core.tools import verify_safe_path
        p = verify_safe_path(test_rel_file)
        if os.path.exists(p):
            os.remove(p)
        # remove backup if created
        if res_e.get("backup_created"):
            bak = verify_safe_path(res_e["backup_created"])
            if os.path.exists(bak):
                os.remove(bak)
    except Exception:
        pass


def test_verhoeff_aadhaar_validation():
    """Test Dihedral D5 Verhoeff checksum algorithm with valid and invalid Aadhaar numbers."""
    # Valid Aadhaar numbers generated via Verhoeff checksum
    valid_aadhaar = "999999990019" # valid Verhoeff D5
    # Invalid (corrupted single digit)
    invalid_aadhaar = "999999990018"

    res_valid = tool_validate_aadhaar_verhoeff(valid_aadhaar)
    assert res_valid["success"] is True
    assert res_valid["is_valid"] is True

    res_invalid = tool_validate_aadhaar_verhoeff(invalid_aadhaar)
    assert res_invalid["success"] is True
    assert res_invalid["is_valid"] is False


def test_dpdp_tokenization():
    """Verify Indian DPDP Act 2023 tokenization masks sensitive PII."""
    raw_prompt = "Customer Dhruv with Aadhaar 9999 9999 0019 and PAN ABCDE1234F called from 9876543210."
    res = tool_dpdp_tokenize(raw_prompt)
    assert res["success"] is True
    assert res["tokens_created_count"] >= 3
    assert "ABCDE1234F" not in res["tokenized_text"]
    assert "[[KAVACH_DPDP_PAN_" in res["tokenized_text"]


def test_entropy_and_ast_security_scanners():
    """Verify Shannon entropy detector and AST syntax auditor."""
    # High entropy API key
    sample_text = "AWS_SECRET_KEY = 'h8fH29xLk92PqZ49vLm018Zc92K10982'"
    res_entropy = tool_entropy_secret_audit(sample_text)
    assert res_entropy["success"] is True
    assert res_entropy["high_entropy_findings_count"] >= 1

    # Insecure python code with eval
    insecure_code = """
import os
def handle_input(user_str):
    eval(user_str)
    os.system("ls -la")
"""
    res_ast = tool_ast_security_scan(insecure_code)
    assert res_ast["success"] is True
    assert res_ast["is_safe"] is False
    assert res_ast["vulnerabilities_found"] == 2


def test_python_execution_tool():
    """Verify live Python execution in subprocess."""
    res = tool_run_python(code="print(2 + 2 * 10)")
    assert res["success"] is True
    assert res["stdout"].strip() == "22"


def test_universal_execute_tool_dispatcher():
    """Verify universal execute_tool function dispatch and error handling."""
    # Test valid dispatch
    res = execute_tool("tool_validate_aadhaar_verhoeff", {"aadhaar_number": "999999990019"})
    assert res["success"] is True
    assert res["is_valid"] is True

    # Test unknown tool
    res_err = execute_tool("non_existent_tool", {})
    assert res_err["success"] is False
    assert "Unknown tool" in res_err["error"]

    # Test invalid arguments
    res_arg_err = execute_tool("tool_read_file", {})
    assert res_arg_err["success"] is False


def test_ast_taint_graph_and_supply_chain_tools():
    """Verify AST Taint Reachability DAG scan and Damerau-Levenshtein slopsquatting check."""
    # 1. AST Taint Scan on vulnerable sink reachability
    code_with_taint = """
import colorma
def handle_request(user_input):
    sanitized = user_input
    eval(sanitized)
    os.system("echo " + user_input)
"""
    res_taint = execute_tool("tool_ast_taint_graph_scan", {"content_or_file_path": code_with_taint})
    assert res_taint["success"] is True
    assert res_taint["is_safe"] is False
    assert res_taint["sinks_found_count"] >= 2
    assert res_taint["slopsquats_found_count"] >= 1
    assert "colorma" in [s["candidate_package"] for s in res_taint["slopsquatting_findings"]]

    # 2. Supply Chain Audit on requirements with typosquatting
    reqs_text = """
fastapi==0.110.0
numpy>=1.24.0
reqeusts==2.31.0
colorma>=0.4.6
"""
    res_sc = execute_tool("tool_supply_chain_audit", {"requirements_or_code": reqs_text})
    assert res_sc["success"] is True
    assert res_sc["is_safe"] is False
    assert res_sc["slopsquatting_anomalies_count"] == 2
    spoofed = {f["spoofed_target"] for f in res_sc["findings"]}
    assert "requests" in spoofed
    assert "colorama" in spoofed


def test_saga_tools():
    """Verify SAGA transaction status and rollback tools."""
    from kavach_agent_core.saga_engine import GLOBAL_SAGA_COORDINATOR
    tx = GLOBAL_SAGA_COORDINATOR.begin_transaction(goal="Test tool-level SAGA dispatch")
    
    # Query status
    res_status = execute_tool("tool_saga_status", {"transaction_id": tx.transaction_id})
    assert res_status["success"] is True
    assert res_status["transaction"]["state"] == "ACTIVE"

    # Rollback tool
    res_rb = execute_tool("tool_saga_rollback", {"transaction_id": tx.transaction_id, "reason": "Test unit rollback"})
    assert res_rb["success"] is True
    assert res_rb["state"] == "ROLLED_BACK"


def test_differential_privacy_tools():
    """Verify tool_differential_privacy_query and tool_dp_budget_status."""
    from kavach_agent_core.differential_privacy import GLOBAL_DP_ENGINE
    GLOBAL_DP_ENGINE.accountant.reset(new_budget=10.0)

    # 1. DP Query Tool
    res_query = execute_tool("tool_differential_privacy_query", {"query_type": "COUNT", "epsilon": 0.5})
    assert res_query["success"] is True
    assert "privatized_value" in res_query
    assert res_query["sensitivity"] == 1.0

    # 2. Budget Status Tool
    res_budget = execute_tool("tool_dp_budget_status", {})
    assert res_budget["success"] is True
    assert res_budget["spent_budget"] >= 0.5
    assert res_budget["remaining_budget"] <= 9.5




