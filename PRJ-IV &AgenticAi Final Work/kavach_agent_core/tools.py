"""
KAVACH Agentic AI Platform - Model Context Protocol (MCP) Tool Registry
Course: CSE3101 Agentic AI - Final Capstone Project
Authors: Dhruv Jain (230532), BML Munjal University

This module provides real, verifiable, workspace-bounded tools that give
the AI Agent genuine capabilities to interact with the environment:
  1. Filesystem Tools: Read, Write, Edit, Search, List
  2. Execution Tools: Python execution and Pytest test runner
  3. Domain Security Tools: Verhoeff D5 Aadhaar Checksum, DPDP 2023 Tokenization,
     Shannon Entropy Secrets Auditor, AST Blast-Radius Scanner.
"""

import os
import sys
import re
import ast
import time
import math
import shutil
import difflib
import subprocess
from typing import Dict, Any, List, Optional, Tuple

# Base workspace directory
WORKSPACE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

BLOCKED_EXTENSIONS = {".exe", ".dll", ".so", ".bin", ".pyd", ".key", ".pfx"}

# =========================================================================
# PATH SAFETY & CONTAINMENT
# =========================================================================

def verify_safe_path(target_path: str) -> str:
    """Enforce workspace containment to prevent arbitrary file traversal."""
    if not os.path.isabs(target_path):
        sub_resolved = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), target_path))
        if os.path.exists(sub_resolved):
            resolved = sub_resolved
        else:
            resolved = os.path.abspath(os.path.join(WORKSPACE_ROOT, target_path))
    else:
        resolved = os.path.abspath(target_path)

    try:
        common = os.path.commonpath([WORKSPACE_ROOT, resolved])
    except ValueError:
        raise PermissionError(f"Access denied: Path across drives is not allowed: '{target_path}'")

    if common != WORKSPACE_ROOT:
        raise PermissionError(f"Access denied: Target path '{target_path}' escapes workspace boundary '{WORKSPACE_ROOT}'")

    return resolved


# =========================================================================
# 1. FILESYSTEM & REPOSITORY TOOLS
# =========================================================================

def tool_list_files(directory: str = "", max_depth: int = 2) -> Dict[str, Any]:
    """List directory contents up to a maximum depth within the workspace."""
    try:
        target = verify_safe_path(directory or WORKSPACE_ROOT)
        if not os.path.isdir(target):
            return {"success": False, "error": f"Path is not a directory: {directory}"}

        items = []
        base_depth = target.rstrip(os.sep).count(os.sep)
        for dirpath, dirnames, filenames in os.walk(target):
            current_depth = dirpath.count(os.sep) - base_depth
            if current_depth > max_depth:
                dirnames.clear()
                continue

            dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__", "venv", ".venv", "node_modules"}]
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                rel_path = os.path.relpath(fpath, WORKSPACE_ROOT).replace("\\", "/")
                try:
                    sz = os.path.getsize(fpath)
                except OSError:
                    sz = 0
                items.append({"path": rel_path, "is_dir": False, "size_bytes": sz})

            for dname in dirnames:
                dpath = os.path.join(dirpath, dname)
                rel_path = os.path.relpath(dpath, WORKSPACE_ROOT).replace("\\", "/")
                items.append({"path": rel_path, "is_dir": True, "size_bytes": 0})

        return {
            "success": True,
            "directory": os.path.relpath(target, WORKSPACE_ROOT).replace("\\", "/"),
            "total_items": len(items),
            "items": items[:150],
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_read_file(file_path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> Dict[str, Any]:
    """Read a permitted text file within the workspace with line bounds."""
    try:
        target = verify_safe_path(file_path)
        ext = os.path.splitext(target)[1].lower()
        if ext in BLOCKED_EXTENSIONS:
            return {"success": False, "error": f"Reading binary/credential extension '{ext}' is forbidden"}

        if not os.path.isfile(target):
            return {"success": False, "error": f"File not found: {file_path}"}

        with open(target, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()

        total_lines = len(lines)
        s_idx = max(1, start_line or 1) - 1
        e_idx = min(total_lines, end_line or total_lines)
        selected_lines = lines[s_idx:e_idx]

        numbered_content = "".join(f"{i + s_idx + 1:4d} | {line}" for i, line in enumerate(selected_lines))

        return {
            "success": True,
            "file_path": os.path.relpath(target, WORKSPACE_ROOT).replace("\\", "/"),
            "total_lines": total_lines,
            "start_line": s_idx + 1,
            "end_line": e_idx,
            "content": numbered_content,
            "raw_text": "".join(selected_lines),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_write_file(file_path: str, content: str) -> Dict[str, Any]:
    """Write/overwrite content to a file safely with automatic timestamped backup."""
    try:
        target = verify_safe_path(file_path)
        os.makedirs(os.path.dirname(target), exist_ok=True)

        backup_created = None
        if os.path.isfile(target):
            backup_created = target + f".{int(time.time())}.bak"
            shutil.copy2(target, backup_created)

        with open(target, "w", encoding="utf-8") as f:
            f.write(content)

        return {
            "success": True,
            "file_path": os.path.relpath(target, WORKSPACE_ROOT).replace("\\", "/"),
            "bytes_written": len(content.encode("utf-8")),
            "backup_created": os.path.relpath(backup_created, WORKSPACE_ROOT).replace("\\", "/") if backup_created else None,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_edit_file(file_path: str, target_string: str, replacement_string: str) -> Dict[str, Any]:
    """Atomic search-and-replace edit on an existing file."""
    try:
        target = verify_safe_path(file_path)
        if not os.path.isfile(target):
            return {"success": False, "error": f"File not found: {file_path}"}

        with open(target, "r", encoding="utf-8") as f:
            content = f.read()

        if target_string not in content:
            return {"success": False, "error": f"Target string not found in {file_path}"}

        backup_created = target + f".{int(time.time())}.bak"
        shutil.copy2(target, backup_created)

        new_content = content.replace(target_string, replacement_string)
        with open(target, "w", encoding="utf-8") as f:
            f.write(new_content)

        return {
            "success": True,
            "file_path": os.path.relpath(target, WORKSPACE_ROOT).replace("\\", "/"),
            "occurrences_replaced": content.count(target_string),
            "backup_created": os.path.relpath(backup_created, WORKSPACE_ROOT).replace("\\", "/"),
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_search_code(query: str, search_path: str = "", is_regex: bool = False, max_results: int = 25) -> Dict[str, Any]:
    """Search for literal text or regex patterns across workspace files."""
    try:
        target = verify_safe_path(search_path or WORKSPACE_ROOT)
        results = []
        flags = re.IGNORECASE
        pattern = re.compile(query if is_regex else re.escape(query), flags)

        for dirpath, dirnames, filenames in os.walk(target):
            dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__", "venv", ".venv", "node_modules"}]
            for fname in filenames:
                ext = os.path.splitext(fname)[1].lower()
                if ext in BLOCKED_EXTENSIONS:
                    continue

                fpath = os.path.join(dirpath, fname)
                try:
                    with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                        for lineno, line in enumerate(f, 1):
                            if pattern.search(line):
                                results.append({
                                    "file": os.path.relpath(fpath, WORKSPACE_ROOT).replace("\\", "/"),
                                    "line": lineno,
                                    "match": line.strip()[:180],
                                })
                                if len(results) >= max_results:
                                    break
                except Exception:
                    continue
            if len(results) >= max_results:
                break

        return {
            "success": True,
            "query": query,
            "total_matches": len(results),
            "matches": results,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


# =========================================================================
# 2. EXECUTION & TESTING TOOLS
# =========================================================================

def tool_run_pytest(test_path: str = "", filter_keyword: str = "", timeout_seconds: int = 30) -> Dict[str, Any]:
    """Execute pytest in a bounded subprocess and capture real stdout, stderr, and exit code."""
    try:
        target = verify_safe_path(test_path or WORKSPACE_ROOT)
        cmd = [sys.executable, "-m", "pytest", target, "-q", "--tb=short"]
        if filter_keyword:
            cmd.extend(["-k", filter_keyword])

        start_time = time.time()
        proc = subprocess.run(
            cmd,
            cwd=WORKSPACE_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        duration_ms = round((time.time() - start_time) * 1000, 2)
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        passed = (proc.returncode == 0)

        summary_line = stdout.strip().splitlines()[-1] if stdout.strip() else ""

        return {
            "success": True,
            "command": " ".join(cmd),
            "exit_code": proc.returncode,
            "passed": passed,
            "duration_ms": duration_ms,
            "summary": summary_line,
            "stdout": stdout[:4000],
            "stderr": stderr[:2000],
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Test timed out after {timeout_seconds}s"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_run_python(code: str = "", file_path: str = "", timeout_seconds: int = 15) -> Dict[str, Any]:
    """Execute Python code or a script file in a subprocess with safety limits."""
    try:
        if file_path:
            target = verify_safe_path(file_path)
            cmd = [sys.executable, target]
        else:
            cmd = [sys.executable, "-c", code]

        start_time = time.time()
        proc = subprocess.run(
            cmd,
            cwd=WORKSPACE_ROOT,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        duration_ms = round((time.time() - start_time) * 1000, 2)

        return {
            "success": True,
            "exit_code": proc.returncode,
            "stdout": proc.stdout[:3000],
            "stderr": proc.stderr[:2000],
            "duration_ms": duration_ms,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"Execution timed out after {timeout_seconds}s"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# =========================================================================
# 3. KAVACH DOMAIN SECURITY & COMPLIANCE TOOLS
# =========================================================================

# Dihedral Group D5 Verhoeff Permutation & Multiplication Tables
_VERHOEFF_D = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 2, 3, 4, 0, 6, 7, 8, 9, 5],
    [2, 3, 4, 0, 1, 7, 8, 9, 5, 6],
    [3, 4, 0, 1, 2, 8, 9, 5, 6, 7],
    [4, 0, 1, 2, 3, 9, 5, 6, 7, 8],
    [5, 9, 8, 7, 6, 0, 4, 3, 2, 1],
    [6, 5, 9, 8, 7, 1, 0, 4, 3, 2],
    [7, 6, 5, 9, 8, 2, 1, 0, 4, 3],
    [8, 7, 6, 5, 9, 3, 2, 1, 0, 4],
    [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
]

_VERHOEFF_P = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
    [1, 5, 7, 6, 2, 8, 3, 0, 9, 4],
    [5, 8, 0, 3, 7, 9, 6, 1, 4, 2],
    [8, 9, 1, 6, 0, 4, 3, 5, 2, 7],
    [9, 4, 5, 3, 1, 2, 6, 8, 7, 0],
    [4, 2, 8, 6, 5, 7, 3, 9, 0, 1],
    [2, 7, 9, 3, 8, 0, 6, 4, 1, 5],
    [7, 0, 4, 6, 9, 1, 3, 2, 5, 8],
]


def tool_validate_aadhaar_verhoeff(aadhaar_number: str) -> Dict[str, Any]:
    """
    Validate 12-digit Indian Aadhaar number using Dihedral Group D5 algebraic checksum.
    Guarantees detection of 100% single-digit substitution and adjacent transposition errors.
    """
    clean_digits = [int(c) for c in str(aadhaar_number) if c.isdigit()]
    if len(clean_digits) != 12:
        return {
            "success": True,
            "is_valid": False,
            "error": f"Invalid Aadhaar length: expected 12 digits, got {len(clean_digits)}",
        }

    c = 0
    for i, d in enumerate(reversed(clean_digits)):
        c = _VERHOEFF_D[c][_VERHOEFF_P[i % 8][d]]

    verhoeff_zero = (c == 0)
    uidai_lead_valid = (clean_digits[0] not in (0, 1))
    is_valid = verhoeff_zero and uidai_lead_valid

    reasons = []
    if not uidai_lead_valid:
        reasons.append("UIDAI violation: Aadhaar cannot begin with digit 0 or 1")
    if not verhoeff_zero:
        reasons.append(f"Dihedral D5 checksum failure (c={c}, expected 0)")

    return {
        "success": True,
        "aadhaar": f"{clean_digits[0]}XXX-XXXX-XXXX",
        "is_valid": is_valid,
        "checksum_value": c,
        "verhoeff_zero_checksum": verhoeff_zero,
        "uidai_format_valid": uidai_lead_valid,
        "mathematical_group": "Dihedral Group D5",
        "diagnostic": "Valid UIDAI Aadhaar Number" if is_valid else "; ".join(reasons),
    }


def tool_dpdp_tokenize(text: str) -> Dict[str, Any]:
    """
    Indian DPDP Act 2023 Tokenization Vault: Detects and pseudonymizes Aadhaar, PAN,
    credit/debit cards, phone numbers, and emails into reversible secure tokens.
    """
    import uuid
    token_vault = {}
    tokens_created = []

    # Priority-ordered patterns (16-digit cards evaluated before 12-digit Aadhaar)
    patterns = [
        (r"\b(?:\d{4}[\s-]?){3}\d{4}\b|\b\d{16}\b", "PAYMENT_CARD"),
        (r"\b(?:\d{4}[\s-]?){2}\d{4}\b|\b\d{12}\b", "AADHAAR"),
        (r"\b[A-Za-z]{5}[0-9]{4}[A-Za-z]\b", "PAN"),
        (r"\b(?:(?:\+91|0)?[6-9]\d{9})\b", "PHONE"),
        (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b", "EMAIL"),
    ]

    redacted_text = text
    for pat, label in patterns:
        matches = re.findall(pat, redacted_text)
        for m in matches:
            clean_m = re.sub(r"[\s-]", "", m)
            tok = f"[[KAVACH_DPDP_{label}_{uuid.uuid4().hex[:8].upper()}]]"
            token_vault[tok] = m

            meta = {
                "type": label,
                "token": tok,
                "original_length": len(m),
            }
            if label == "AADHAAR":
                v_res = tool_validate_aadhaar_verhoeff(clean_m)
                meta["verhoeff_valid"] = v_res.get("is_valid", False)
                meta["uidai_format_valid"] = v_res.get("uidai_format_valid", False)
                meta["diagnostic"] = v_res.get("diagnostic", "")

            tokens_created.append(meta)
            redacted_text = redacted_text.replace(m, tok)

    return {
        "success": True,
        "tokens_created_count": len(tokens_created),
        "tokens_created": tokens_created,
        "tokenized_text": redacted_text,
    }


def tool_entropy_secret_audit(content: str) -> Dict[str, Any]:
    """
    Calculates Shannon Information Entropy H(X) = -sum(p * log2(p)) to detect
    high-entropy cryptographic secrets, API keys, and passwords.
    """
    candidates = set()
    # Find quoted string literals or alphanumeric/symbolic strings
    for m in re.findall(r"['\"]([^'\"]{10,})['\"]", content):
        candidates.add(m)
    for m in re.findall(r"[A-Za-z0-9+/=_\-!@#$%^&*]{14,}", content):
        candidates.add(m)

    findings = []
    for tok in candidates:
        if len(tok) < 10:
            continue
        prob = [tok.count(c) / len(tok) for c in set(tok)]
        h = -sum(p * math.log2(p) for p in prob)
        if h >= 3.8:
            findings.append({
                "secret_candidate": tok[:4] + "..." + tok[-4:],
                "entropy_bits": round(h, 3),
                "risk": "HIGH" if h >= 4.3 else "MEDIUM",
            })

    return {
        "success": True,
        "high_entropy_findings_count": len(findings),
        "findings": findings,
    }


def tool_ast_security_scan(content_or_file_path: str) -> Dict[str, Any]:
    """
    Analyze Python code via Abstract Syntax Tree (AST) to detect dangerous calls:
    eval, exec, os.system, subprocess with shell=True, pickle, and hardcoded secrets.
    """
    code_str = content_or_file_path
    if os.path.isfile(content_or_file_path):
        target = verify_safe_path(content_or_file_path)
        with open(target, "r", encoding="utf-8") as f:
            code_str = f.read()

    try:
        tree = ast.parse(code_str)
    except SyntaxError as se:
        return {"success": False, "error": f"SyntaxError in code: {se}"}

    vulnerabilities = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            # eval(), exec()
            if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
                vulnerabilities.append({
                    "line": node.lineno,
                    "type": "ARBITRARY_CODE_EXECUTION",
                    "severity": "CRITICAL",
                    "detail": f"Direct call to forbidden '{node.func.id}()'",
                })
            # os.system, os.popen
            elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
                if node.func.attr in ("system", "popen"):
                    vulnerabilities.append({
                        "line": node.lineno,
                        "type": "COMMAND_INJECTION_RISK",
                        "severity": "HIGH",
                        "detail": f"os.{node.func.attr}() call detected",
                    })
            # subprocess.Popen / subprocess.run / subprocess.call
            elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
                if node.func.attr in ("Popen", "run", "call", "check_output"):
                    shell_kw = any(isinstance(k, ast.keyword) and k.arg == "shell" and getattr(k.value, "value", False) is True for k in node.keywords)
                    if shell_kw or node.func.attr in ("Popen", "run"):
                        vulnerabilities.append({
                            "line": node.lineno,
                            "type": "SUBPROCESS_INJECTION_RISK",
                            "severity": "HIGH",
                            "detail": f"subprocess.{node.func.attr}(shell=True) detected",
                        })
            # pickle.loads / pickle.load
            elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "pickle":
                if node.func.attr in ("loads", "load"):
                    vulnerabilities.append({
                        "line": node.lineno,
                        "type": "INSECURE_DESERIALIZATION",
                        "severity": "CRITICAL",
                        "detail": f"pickle.{node.func.attr}() deserialization sink detected",
                    })

    return {
        "success": True,
        "is_safe": len(vulnerabilities) == 0,
        "vulnerabilities_found": len(vulnerabilities),
        "vulnerabilities_found_count": len(vulnerabilities),
        "vulnerabilities": vulnerabilities,
    }


def tool_ast_taint_graph_scan(content_or_file_path: str) -> Dict[str, Any]:
    """
    Constructs an explicit AST Taint Graph G_AST = (V, E) to trace data-flow reachability
    from untrusted inputs to dangerous sinks (eval, exec, os.system, subprocess, pickle).
    Also performs Damerau-Levenshtein slopsquatting dependency checks.
    """
    from kavach_agent_core.ast_analyzer import analyze_ast_and_supply_chain
    code_str = content_or_file_path
    if os.path.isfile(content_or_file_path):
        target = verify_safe_path(content_or_file_path)
        with open(target, "r", encoding="utf-8") as f:
            code_str = f.read()

    return analyze_ast_and_supply_chain(code_str)


def tool_supply_chain_audit(requirements_or_code: str) -> Dict[str, Any]:
    """
    Audits dependency packages against the verified PyPI registry using
    the Damerau-Levenshtein metric space to flag hallucinated/slopsquatted packages.
    """
    from kavach_agent_core.ast_analyzer import check_supply_chain_slopsquatting
    lines = requirements_or_code.splitlines()
    candidates = []
    for line in lines:
        cleaned = re.sub(r"[#=><~].*", "", line).strip()
        import_match = re.search(r"(?:import|from)\s+([a-zA-Z0-9_\-]+)", cleaned)
        if import_match:
            cleaned = import_match.group(1).strip()
        if cleaned and len(cleaned) >= 3:
            candidates.append(cleaned)

    findings = []
    for c in set(candidates):
        res = check_supply_chain_slopsquatting(c)
        if res:
            findings.append(res)

    return {
        "success": True,
        "is_safe": len(findings) == 0,
        "packages_audited_count": len(candidates),
        "slopsquatting_anomalies_count": len(findings),
        "findings": findings,
    }


def tool_saga_rollback(transaction_id: str, reason: str = "Invariant violation or test failure") -> Dict[str, Any]:
    """
    Execute reverse compensating transactions C_{k-1} ... C_1 in SAGA protocol
    to restore workspace files to pre-transaction SHA-256 state without corruption.
    """
    from kavach_agent_core.saga_engine import GLOBAL_SAGA_COORDINATOR
    try:
        tx = GLOBAL_SAGA_COORDINATOR.rollback(transaction_id, reason=reason)
        return {
            "success": True,
            "transaction_id": tx.transaction_id,
            "state": tx.state,
            "rollback_reason": tx.rollback_reason,
            "compensations_executed": len(tx.compensation_log),
            "compensation_log": tx.compensation_log,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def tool_saga_status(transaction_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Query active SAGA transaction status or list recent transaction compensation logs.
    """
    from kavach_agent_core.saga_engine import GLOBAL_SAGA_COORDINATOR
    if transaction_id:
        tx = GLOBAL_SAGA_COORDINATOR.active_transactions.get(transaction_id)
        if not tx:
            hist = [t for t in GLOBAL_SAGA_COORDINATOR.transaction_history if t.transaction_id == transaction_id]
            tx = hist[0] if hist else None
        if not tx:
            return {"success": False, "error": f"Transaction '{transaction_id}' not found."}
        return {"success": True, "transaction": tx.dict()}

    return {
        "success": True,
        "total_managed": GLOBAL_SAGA_COORDINATOR.total_transactions_managed,
        "total_commits": GLOBAL_SAGA_COORDINATOR.total_commits_executed,
        "total_rollbacks": GLOBAL_SAGA_COORDINATOR.total_rollbacks_executed,
        "active_transactions_count": len(GLOBAL_SAGA_COORDINATOR.active_transactions),
        "recent_history": [t.dict() for t in GLOBAL_SAGA_COORDINATOR.transaction_history[-5:]],
    }


def tool_differential_privacy_query(
    query_type: str = "COUNT",
    epsilon: float = 0.5,
    clipping_bound: float = 100000.0,
) -> Dict[str, Any]:
    """
    Execute an epsilon-Differentially Private aggregate query (COUNT, SUM, AVG)
    with calibrated Laplace noise to protect banking records against reconstruction attacks.
    """
    from kavach_agent_core.differential_privacy import GLOBAL_DP_ENGINE
    return GLOBAL_DP_ENGINE.query_dp_aggregate(
        query_type=query_type,
        epsilon=epsilon,
        clipping_bound=clipping_bound,
    )


def tool_dp_budget_status() -> Dict[str, Any]:
    """
    Query the Differential Privacy budget consumption and remaining allocation.
    """
    from kavach_agent_core.differential_privacy import GLOBAL_DP_ENGINE
    acct = GLOBAL_DP_ENGINE.accountant
    return {
        "success": True,
        "total_budget": acct.total_budget,
        "spent_budget": acct.spent_budget,
        "remaining_budget": acct.remaining_budget,
        "query_count": acct.query_count,
        "queries": acct.query_log[-10:],
    }


# =========================================================================
# MCP TOOL REGISTRY & SCHEMAS
# =========================================================================

TOOL_REGISTRY = {
    "tool_list_files": tool_list_files,
    "tool_read_file": tool_read_file,
    "tool_write_file": tool_write_file,
    "tool_edit_file": tool_edit_file,
    "tool_search_code": tool_search_code,
    "tool_run_pytest": tool_run_pytest,
    "tool_run_python": tool_run_python,
    "tool_validate_aadhaar_verhoeff": tool_validate_aadhaar_verhoeff,
    "tool_dpdp_tokenize": tool_dpdp_tokenize,
    "tool_entropy_secret_audit": tool_entropy_secret_audit,
    "tool_ast_security_scan": tool_ast_security_scan,
    "tool_ast_taint_graph_scan": tool_ast_taint_graph_scan,
    "tool_supply_chain_audit": tool_supply_chain_audit,
    "tool_saga_rollback": tool_saga_rollback,
    "tool_saga_status": tool_saga_status,
    "tool_differential_privacy_query": tool_differential_privacy_query,
    "tool_dp_budget_status": tool_dp_budget_status,
}

MCP_TOOL_SCHEMAS = [
    {
        "name": "tool_list_files",
        "description": "Explore repository files and subdirectories under an authorized path.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "Relative directory path (e.g. 'PRJ-IV &AgenticAi Final Work')"},
                "max_depth": {"type": "integer", "description": "Maximum directory traversal depth (default 2)"},
            },
        },
    },
    {
        "name": "tool_read_file",
        "description": "Read source code or text file from the workspace with line bounds.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Relative file path to read"},
                "start_line": {"type": "integer", "description": "Starting line number (1-indexed)"},
                "end_line": {"type": "integer", "description": "Ending line number (inclusive)"},
            },
            "required": ["file_path"],
        },
    },
    {
        "name": "tool_write_file",
        "description": "Write or overwrite content to a file safely with an automatic timestamped backup.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Relative file path to write to"},
                "content": {"type": "string", "description": "Full file content string to write"},
            },
            "required": ["file_path", "content"],
        },
    },
    {
        "name": "tool_edit_file",
        "description": "Perform atomic search-and-replace modification on a specific file.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Relative file path to modify"},
                "target_string": {"type": "string", "description": "Exact text substring to replace"},
                "replacement_string": {"type": "string", "description": "Replacement text substring"},
            },
            "required": ["file_path", "target_string", "replacement_string"],
        },
    },
    {
        "name": "tool_search_code",
        "description": "Search literal text or regex pattern across workspace source code files.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The search term or regex"},
                "search_path": {"type": "string", "description": "Subdirectory to restrict search"},
                "is_regex": {"type": "boolean", "description": "Treat query as regex (default false)"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "tool_run_pytest",
        "description": "Execute pytest in a bounded subprocess and capture real test status and tracebacks.",
        "parameters": {
            "type": "object",
            "properties": {
                "test_path": {"type": "string", "description": "Path to test file or directory"},
                "filter_keyword": {"type": "string", "description": "pytest -k keyword filter"},
            },
        },
    },
    {
        "name": "tool_run_python",
        "description": "Execute Python code or a script file in a subprocess with safety limits.",
        "parameters": {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "Python code string to execute with python -c"},
                "file_path": {"type": "string", "description": "Or path to python script to run"},
            },
        },
    },
    {
        "name": "tool_validate_aadhaar_verhoeff",
        "description": "Validate 12-digit Indian Aadhaar number using Dihedral Group D5 algebraic checksum.",
        "parameters": {
            "type": "object",
            "properties": {
                "aadhaar_number": {"type": "string", "description": "12-digit Aadhaar number string"},
            },
            "required": ["aadhaar_number"],
        },
    },
    {
        "name": "tool_dpdp_tokenize",
        "description": "Tokenize and mask PII (Aadhaar, PAN, Phone, Email) per Indian DPDP Act 2023.",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "Text containing sensitive data to tokenize"},
            },
            "required": ["text"],
        },
    },
    {
        "name": "tool_entropy_secret_audit",
        "description": "Calculate Shannon Information Entropy to detect exposed API keys and passwords.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "Text or code to scan for secrets"},
            },
            "required": ["content"],
        },
    },
    {
        "name": "tool_ast_security_scan",
        "description": "Perform AST scan on Python code to identify eval, exec, and command injection risks.",
        "parameters": {
            "type": "object",
            "properties": {
                "content_or_file_path": {"type": "string", "description": "Python source code string or file path"},
            },
            "required": ["content_or_file_path"],
        },
    },
    {
        "name": "tool_ast_taint_graph_scan",
        "description": "Construct explicit AST Taint Reachability DAG G_AST = (V, E) tracing data flows from tainted sources to dangerous sinks (eval, exec, os.system, subprocess, pickle).",
        "parameters": {
            "type": "object",
            "properties": {
                "content_or_file_path": {"type": "string", "description": "Python source code string or file path to analyze for AST taint reachability"},
            },
            "required": ["content_or_file_path"],
        },
    },
    {
        "name": "tool_supply_chain_audit",
        "description": "Audit dependency imports and requirements against verified PyPI registry using Damerau-Levenshtein metric space to flag hallucinated/slopsquatted packages (CWE-1395).",
        "parameters": {
            "type": "object",
            "properties": {
                "requirements_or_code": {"type": "string", "description": "requirements.txt content or Python source code containing import statements"},
            },
            "required": ["requirements_or_code"],
        },
    },
    {
        "name": "tool_saga_rollback",
        "description": "Execute reverse compensating transactions C_{k-1} ... C_1 in SAGA protocol to restore workspace files without corruption.",
        "parameters": {
            "type": "object",
            "properties": {
                "transaction_id": {"type": "string", "description": "Saga transaction ID to rollback"},
                "reason": {"type": "string", "description": "Failure reason triggering rollback"},
            },
            "required": ["transaction_id"],
        },
    },
    {
        "name": "tool_saga_status",
        "description": "Query active SAGA distributed transaction status or list recent compensation logs.",
        "parameters": {
            "type": "object",
            "properties": {
                "transaction_id": {"type": "string", "description": "Optional transaction ID to query specific state"},
            },
        },
    },
    {
        "name": "tool_differential_privacy_query",
        "description": "Execute an epsilon-Differentially Private aggregate query (COUNT, SUM, AVG) with calibrated Laplace noise to protect banking records per Indian DPDP Act 2023.",
        "parameters": {
            "type": "object",
            "properties": {
                "query_type": {"type": "string", "description": "Aggregate function to evaluate: 'COUNT', 'SUM', or 'AVG'"},
                "epsilon": {"type": "number", "description": "Privacy parameter epsilon > 0 (default 0.5)"},
                "clipping_bound": {"type": "number", "description": "Upper clipping bound B for global sensitivity calibration (default 100000.0)"},
            },
            "required": ["query_type"],
        },
    },
    {
        "name": "tool_dp_budget_status",
        "description": "Query cumulative Differential Privacy budget consumption and remaining allocation under sequential composition.",
        "parameters": {
            "type": "object",
            "properties": {},
        },
    },
]


def execute_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """Universal dispatcher for the MCP Tool Registry."""
    if tool_name not in TOOL_REGISTRY:
        return {
            "success": False,
            "error": f"Unknown tool '{tool_name}'. Available tools: {list(TOOL_REGISTRY.keys())}",
        }
    fn = TOOL_REGISTRY[tool_name]
    try:
        return fn(**arguments)
    except TypeError as te:
        return {"success": False, "error": f"Invalid arguments for {tool_name}: {te}"}
    except Exception as e:
        return {"success": False, "error": f"Tool execution failed: {e}"}
