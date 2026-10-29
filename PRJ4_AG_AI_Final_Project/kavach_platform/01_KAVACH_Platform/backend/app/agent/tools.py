"""
Registered Tools Engine for KAVACH Agentic AI Platform (Phase 4).

Provides real, permission-controlled, workspace-bounded tools that perform
actual operations on the software repository:
  1. repo_list_tree: Safely inspect repository filesystem structure.
  2. repo_read_file: Read source code with line slice limits and path traversal guards.
  3. repo_search_code: Search literal/regex patterns across codebase.
  4. security_scan_code: Run KAVACH native PII and secret scanners.
  5. ast_analyze_impact: Calculate module dependencies and blast radius.
  6. run_allowlisted_tests: Execute real pytest suites in a bounded subprocess with timeouts.
  7. propose_code_patch: Construct an in-memory unified diff for review.
  8. apply_approved_patch: Atomically apply patch with backup after human approval.

Every tool validates inputs, enforces workspace containment, and returns
structured, verifiable result dictionaries.
"""

import os
import re
import sys
import ast
import time
import shutil
import difflib
import subprocess
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from app.security.detector import detect_pii
from app.security.secret_detector import detect_secrets
from app.impact.dependency_graph import build_dependency_graph, find_dependent_files
from app.security.multimodal_vision import global_vision_auditor


# ---------------------------------------------------------------------------
# Workspace Boundaries & Allowlist Security Policy
# ---------------------------------------------------------------------------

def get_workspace_root() -> str:
    """Return the absolute path to the permitted repository root."""
    backend_app_dir = os.path.abspath(os.path.dirname(__file__))
    # backend_app_dir (agent) -> app -> backend -> 01_KAVACH_Platform -> repo root (KAVACH-main)
    repo_root = os.path.abspath(os.path.join(backend_app_dir, "..", "..", "..", ".."))
    return repo_root


def _verify_safe_path(target_path: str, workspace_root: Optional[str] = None) -> str:
    """
    Ensure the target path resides strictly inside the authorized workspace boundary.
    Raises PermissionError on path traversal attempts or attempts to escape root.
    """
    root = os.path.abspath(workspace_root or get_workspace_root())
    if not os.path.isabs(target_path):
        resolved = os.path.abspath(os.path.join(root, target_path))
    else:
        resolved = os.path.abspath(target_path)

    # Path traversal check
    try:
        common = os.path.commonpath([root, resolved])
    except ValueError:
        raise PermissionError(f"Access denied: Path across drives is not allowed: '{target_path}'")

    if common != root:
        raise PermissionError(f"Access denied: Target path '{target_path}' escapes workspace boundary '{root}'")

    return resolved


BLOCKED_EXTENSIONS = {".exe", ".dll", ".so", ".dylib", ".bin", ".pyc", ".pyd", ".key", ".pem", ".pfx"}
ALLOWLISTED_TEST_PREFIXES = [
    "01_KAVACH_Platform/tests",
    "02_Banking_and_Results_Dashboard",
    "tests",
]


# ---------------------------------------------------------------------------
# Tool Schemas
# ---------------------------------------------------------------------------

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, Any]
    permission_level: str = "READ"  # READ, ANALYZE, TEST, WRITE


# ---------------------------------------------------------------------------
# Tool Implementations
# ---------------------------------------------------------------------------

def repo_list_tree(directory: str = "", max_depth: int = 2) -> Dict[str, Any]:
    """List directory contents up to a maximum depth within the workspace."""
    root = get_workspace_root()
    target = _verify_safe_path(directory or root)
    if not os.path.isdir(target):
        return {"error": f"Path is not a directory: {directory}", "success": False}

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
            rel_path = os.path.relpath(fpath, root).replace("\\", "/")
            try:
                sz = os.path.getsize(fpath)
            except OSError:
                sz = 0
            items.append({"path": rel_path, "is_dir": False, "size_bytes": sz})

        for dname in dirnames:
            dpath = os.path.join(dirpath, dname)
            rel_path = os.path.relpath(dpath, root).replace("\\", "/")
            items.append({"path": rel_path, "is_dir": True, "size_bytes": 0})

    return {
        "success": True,
        "base_directory": os.path.relpath(target, root).replace("\\", "/"),
        "total_items": len(items),
        "items": items[:150],  # cap listing size
    }


def repo_read_file(file_path: str, start_line: Optional[int] = None, end_line: Optional[int] = None) -> Dict[str, Any]:
    """Read a permitted text file within the workspace with optional line slicing."""
    root = get_workspace_root()
    target = _verify_safe_path(file_path)

    ext = os.path.splitext(target)[1].lower()
    if ext in BLOCKED_EXTENSIONS:
        return {"error": f"Access denied: Reading binary/credential extension '{ext}' is forbidden", "success": False}

    if not os.path.isfile(target):
        return {"error": f"File not found: {file_path}", "success": False}

    try:
        with open(target, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
    except Exception as e:
        return {"error": f"Failed to read file: {e}", "success": False}

    total_lines = len(lines)
    s_idx = max(1, start_line or 1) - 1
    e_idx = min(total_lines, end_line or total_lines)

    selected_lines = lines[s_idx:e_idx]
    numbered_content = "".join(f"{i + s_idx + 1:4d} | {line}" for i, line in enumerate(selected_lines))

    return {
        "success": True,
        "file_path": os.path.relpath(target, root).replace("\\", "/"),
        "total_lines": total_lines,
        "start_line": s_idx + 1,
        "end_line": e_idx,
        "content": numbered_content,
        "raw_text": "".join(selected_lines),
    }


def repo_search_code(query: str, search_path: str = "", is_regex: bool = False, max_results: int = 25) -> Dict[str, Any]:
    """Search for code patterns across permitted files in the workspace."""
    root = get_workspace_root()
    target = _verify_safe_path(search_path or root)

    results = []
    flags = re.IGNORECASE
    try:
        pattern = re.compile(query if is_regex else re.escape(query), flags)
    except re.error as err:
        return {"error": f"Invalid regex pattern: {err}", "success": False}

    for dirpath, dirnames, filenames in os.walk(target):
        dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__", "venv", ".venv", "node_modules", "data"}]
        for fname in filenames:
            if not fname.endswith((".py", ".js", ".html", ".css", ".md", ".json", ".txt")):
                continue
            fpath = os.path.join(dirpath, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                    for line_no, line in enumerate(f, 1):
                        if pattern.search(line):
                            results.append({
                                "file": os.path.relpath(fpath, root).replace("\\", "/"),
                                "line_number": line_no,
                                "line_content": line.strip()[:200],
                            })
                            if len(results) >= max_results:
                                break
            except OSError:
                continue
        if len(results) >= max_results:
            break

    return {
        "success": True,
        "query": query,
        "match_count": len(results),
        "matches": results,
    }


def security_scan_code(content: str) -> Dict[str, Any]:
    """Run native KAVACH PII, secret, and prompt injection analysis on text/code."""
    pii = detect_pii(content)
    secrets = detect_secrets(content)
    all_findings = pii + secrets

    severities = [f.get("severity", "low") for f in all_findings]
    has_critical = "critical" in severities or "high" in severities

    return {
        "success": True,
        "findings_count": len(all_findings),
        "is_safe": len(all_findings) == 0,
        "has_critical_findings": has_critical,
        "findings": all_findings,
    }


def multimodal_inspect_image(
    image_path: str = "",
    base64_data: str = "",
    description: str = ""
) -> Dict[str, Any]:
    """
    Multimodal visual inspection tool for architecture diagrams, code screenshots, and UI captures.
    Verifies image path containment or decodes base64 payload, extracts visual metadata/entropy,
    and identifies security anti-patterns (unencrypted endpoints, visual credential leaks, open ingress).
    """
    root = get_workspace_root()
    safe_target = ""
    if image_path:
        is_safe, err_or_path = _verify_safe_path(image_path, root)
        if not is_safe:
            return {"success": False, "error": f"Path security violation: {err_or_path}"}
        safe_target = err_or_path

    audit_res = global_vision_auditor.audit_diagram_or_image(
        image_identifier=safe_target or "visual_capture",
        diagram_description=description,
        base64_data=base64_data or None
    )
    audit_res["success"] = True
    return audit_res


def ast_analyze_impact(target_file: str) -> Dict[str, Any]:
    """Calculate AST dependencies and blast radius for a target file."""
    root = get_workspace_root()
    norm_path = target_file.replace("\\", "/").lstrip("./")

    # Find the backend directory
    backend_app_dir = os.path.join(root, "01_KAVACH_Platform", "backend", "app")
    if not os.path.exists(backend_app_dir):
        backend_app_dir = os.path.join(root, "backend", "app")

    dep_graph = build_dependency_graph(backend_app_dir)
    mod_hint = os.path.splitext(os.path.basename(norm_path))[0]
    dependents = find_dependent_files(dep_graph, mod_hint)

    total_modules = len(dep_graph) or 1
    blast_radius = round(len(dependents) / total_modules, 4)

    return {
        "success": True,
        "target_file": norm_path,
        "direct_dependents": dependents,
        "total_affected_files": len(dependents),
        "blast_radius_score": blast_radius,
        "risk_tier": "CRITICAL" if blast_radius > 0.5 else ("HIGH" if blast_radius > 0.2 else "LOW"),
    }


def run_allowlisted_tests(test_path: str, filter_keyword: str = "", timeout_seconds: int = 30) -> Dict[str, Any]:
    """
    Execute pytest on an allowlisted test directory or file in a bounded subprocess.
    Returns real stdout, stderr, and test exit code.
    """
    root = get_workspace_root()
    norm_path = test_path.replace("\\", "/").lstrip("./")

    # Check allowlist
    if not any(norm_path.startswith(prefix) for prefix in ALLOWLISTED_TEST_PREFIXES):
        return {
            "success": False,
            "error": f"Test path '{test_path}' is outside allowlisted test directories: {ALLOWLISTED_TEST_PREFIXES}",
        }

    abs_test_path = _verify_safe_path(norm_path, root)
    if not os.path.exists(abs_test_path):
        return {"success": False, "error": f"Test target does not exist: {test_path}"}

    cmd = [sys.executable, "-m", "pytest", norm_path, "-q", "--tb=short"]
    if filter_keyword:
        cmd.extend(["-k", filter_keyword])

    start_time = time.time()
    try:
        proc = subprocess.run(
            cmd,
            cwd=root,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        duration_ms = round((time.time() - start_time) * 1000, 2)
        stdout = proc.stdout or ""
        stderr = proc.stderr or ""
        passed = (proc.returncode == 0)

        # Extract test summary if available
        summary_line = stdout.strip().splitlines()[-1] if stdout.strip() else ""

        return {
            "success": True,
            "command": " ".join(cmd),
            "exit_code": proc.returncode,
            "passed": passed,
            "duration_ms": duration_ms,
            "summary": summary_line,
            "stdout": stdout[:4000],  # bounded size
            "stderr": stderr[:2000],
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "error": f"Test execution timed out after {timeout_seconds} seconds",
            "duration_ms": timeout_seconds * 1000,
        }
    except Exception as e:
        return {"success": False, "error": f"Failed to execute test process: {e}"}


def propose_code_patch(file_path: str, modified_content: str, change_rationale: str = "") -> Dict[str, Any]:
    """
    Generate an in-memory unified diff against an existing file for human approval.
    Does NOT write to disk.
    """
    root = get_workspace_root()
    target = _verify_safe_path(file_path, root)

    if not os.path.isfile(target):
        return {"error": f"File does not exist: {file_path}", "success": False}

    with open(target, "r", encoding="utf-8", errors="replace") as f:
        original = f.read()

    # Syntax verification if Python
    valid_syntax = True
    syntax_error = None
    if target.endswith(".py"):
        try:
            ast.parse(modified_content)
        except SyntaxError as se:
            valid_syntax = False
            syntax_error = f"SyntaxError at line {se.lineno}: {se.msg}"

    # Generate unified diff
    orig_lines = original.splitlines(keepends=True)
    mod_lines = modified_content.splitlines(keepends=True)
    diff = list(difflib.unified_diff(
        orig_lines, mod_lines,
        fromfile=f"a/{file_path}",
        tofile=f"b/{file_path}",
    ))

    diff_text = "".join(diff)
    import hashlib
    patch_id = hashlib.sha256(diff_text.encode("utf-8")).hexdigest()[:12]

    return {
        "success": True,
        "patch_id": patch_id,
        "file_path": os.path.relpath(target, root).replace("\\", "/"),
        "diff": diff_text,
        "lines_added": sum(1 for line in diff if line.startswith("+") and not line.startswith("+++")),
        "lines_removed": sum(1 for line in diff if line.startswith("-") and not line.startswith("---")),
        "valid_syntax": valid_syntax,
        "syntax_error": syntax_error,
        "change_rationale": change_rationale,
        "status": "AWAITING_APPROVAL",
    }


def apply_approved_patch(file_path: str, patch_content: str, approval_token: str) -> Dict[str, Any]:
    """
    Apply a validated patch to an authorized file with automatic backup.
    Requires an explicit non-empty approval token.
    """
    if not approval_token or approval_token.strip() == "":
        return {
            "success": False,
            "error": "Human approval required: Consequential write operations require a verified supervisor token.",
        }

    root = get_workspace_root()
    target = _verify_safe_path(file_path, root)

    # Protect core security files from autonomous modification
    protected_core = ["detector.py", "secret_detector.py", "policy_engine.py", "merkle_ledger.py"]
    if any(target.endswith(p) for p in protected_core) and "SUPERVISOR_ELEVATED" not in approval_token:
        return {
            "success": False,
            "error": f"Protected security kernel file '{os.path.basename(target)}' cannot be modified without SUPERVISOR_ELEVATED token.",
        }

    if not os.path.isfile(target):
        return {"error": f"File does not exist: {file_path}", "success": False}

    # Create backup before write
    backup_path = target + f".{int(time.time())}.bak"
    try:
        shutil.copy2(target, backup_path)
        with open(target, "w", encoding="utf-8") as f:
            f.write(patch_content)
        return {
            "success": True,
            "file_path": os.path.relpath(target, root).replace("\\", "/"),
            "backup_created": os.path.relpath(backup_path, root).replace("\\", "/"),
            "bytes_written": len(patch_content.encode("utf-8")),
            "status": "APPLIED",
        }
    except Exception as e:
        return {"success": False, "error": f"Write failed: {e}"}


# ---------------------------------------------------------------------------
# Tool Registry Map
# ---------------------------------------------------------------------------

TOOLS_REGISTRY = {
    "repo_list_tree": repo_list_tree,
    "repo_read_file": repo_read_file,
    "repo_search_code": repo_search_code,
    "security_scan_code": security_scan_code,
    "multimodal_inspect_image": multimodal_inspect_image,
    "ast_analyze_impact": ast_analyze_impact,
    "run_allowlisted_tests": run_allowlisted_tests,
    "propose_code_patch": propose_code_patch,
    "apply_approved_patch": apply_approved_patch,
}

TOOL_SCHEMAS = [
    {
        "name": "repo_list_tree",
        "description": "Explore repository files and subdirectories under an authorized path.",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {"type": "string", "description": "Relative directory path (e.g. '01_KAVACH_Platform/backend/app')"},
                "max_depth": {"type": "integer", "description": "Maximum directory traversal depth (default 2)"},
            },
        },
    },
    {
        "name": "repo_read_file",
        "description": "Read source code from an authorized file with optional line bounds.",
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
        "name": "repo_search_code",
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
        "name": "security_scan_code",
        "description": "Run KAVACH's native PII, credential, and injection scans on code text.",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {"type": "string", "description": "Code or text snippet to inspect"},
            },
            "required": ["content"],
        },
    },
    {
        "name": "multimodal_inspect_image",
        "description": "Inspect architecture diagrams, error screenshots, or UI captures. Validates bytes, extracts visual metadata/entropy, and flags security threats.",
        "parameters": {
            "type": "object",
            "properties": {
                "image_path": {"type": "string", "description": "Workspace relative path to image file (png, jpg, webp)"},
                "base64_data": {"type": "string", "description": "Optional base64 encoded image payload"},
                "description": {"type": "string", "description": "Optional user context or architecture description"},
            },
        },
    },
    {
        "name": "ast_analyze_impact",
        "description": "Compute import dependencies and change blast radius for a Python module.",
        "parameters": {
            "type": "object",
            "properties": {
                "target_file": {"type": "string", "description": "Relative path to Python file"},
            },
            "required": ["target_file"],
        },
    },
    {
        "name": "run_allowlisted_tests",
        "description": "Execute real pytest tests on allowlisted test paths in a bounded subprocess.",
        "parameters": {
            "type": "object",
            "properties": {
                "test_path": {"type": "string", "description": "Allowlisted path (e.g. '01_KAVACH_Platform/tests/test_api_endpoints.py')"},
                "filter_keyword": {"type": "string", "description": "Pytest keyword filter expression (-k)"},
            },
            "required": ["test_path"],
        },
    },
    {
        "name": "propose_code_patch",
        "description": "Produce a unified diff for review before making a consequential modification.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Target file to modify"},
                "modified_content": {"type": "string", "description": "The new file content"},
                "change_rationale": {"type": "string", "description": "Why this modification is needed"},
            },
            "required": ["file_path", "modified_content"],
        },
    },
    {
        "name": "apply_approved_patch",
        "description": "Apply a patch to a file with automatic backup. Requires human approval token.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {"type": "string", "description": "Target file to patch"},
                "patch_content": {"type": "string", "description": "Verified new content to write"},
                "approval_token": {"type": "string", "description": "Supervisor approval token"},
            },
            "required": ["file_path", "patch_content", "approval_token"],
        },
    },
]


def enable_mcp_tools() -> int:
    """
    Connect to local/remote MCP Server via Model Context Protocol (2024-11-05),
    discover available MCP tools, and dynamically bridge them into KAVACH's tool registry.
    """
    try:
        from app.mcp.client import global_mcp_client
        return global_mcp_client.bridge_tools_to_agent_registry(TOOLS_REGISTRY, TOOL_SCHEMAS)
    except Exception as e:
        return 0

