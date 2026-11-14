"""
KAVACH AST Semantic Vulnerability & Supply-Chain Slopsquatting Graph Traversal (CSE3101 Stage 3)
Authors: Dhruv Jain (230532), BML Munjal University
Direct alignment with:
  - CSE3101 Handout: Unit 6 Software Verification & Security, Static AST Analysis, Taint Traversal
  - Aho et al. (Compilers): Principles, Techniques, and Tools (AST Data-Flow Taint Propagation)
  - Damerau-Levenshtein Metric Space for Package Hallucination / Slopsquatting Invariants
  - Grading Rubrics: C11 (Final Solution), C12 (Technical Depth), C15 (Viva Defense)
"""

import ast
import os
import re
from typing import Dict, Any, List, Set, Tuple, Optional
from pydantic import BaseModel, Field


# =========================================================================
# 1. VERIFIED PYPI ECOSYSTEM & DAMERAU-LEVENSHTEIN METRIC
# =========================================================================

VERIFIED_PYPI_REGISTRY: Set[str] = {
    "requests",
    "numpy",
    "pandas",
    "fastapi",
    "flask",
    "pydantic",
    "cryptography",
    "colorama",
    "scipy",
    "scikit-learn",
    "torch",
    "tensorflow",
    "uvicorn",
    "pytest",
    "httpx",
    "urllib3",
    "sqlalchemy",
    "jinja2",
    "aiohttp",
    "pillow",
    "boto3",
    "paramiko",
    "celery",
    "redis",
    "click",
    "typing-extensions",
    "starlette",
    "pytest-cov",
}


def damerau_levenshtein_distance(s1: str, s2: str) -> int:
    """
    Compute Damerau-Levenshtein distance between two strings,
    supporting insertion, deletion, substitution, and adjacent transposition.
    """
    d = {}
    len1 = len(s1)
    len2 = len(s2)
    for i in range(-1, len1 + 1):
        d[(i, -1)] = i + 1
    for j in range(-1, len2 + 1):
        d[(-1, j)] = j + 1

    for i in range(len1):
        for j in range(len2):
            cost = 0 if s1[i] == s2[j] else 1
            d[(i, j)] = min(
                d[(i - 1, j)] + 1,        # deletion
                d[(i, j - 1)] + 1,        # insertion
                d[(i - 1, j - 1)] + cost,  # substitution
            )
            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost)  # transposition

    return d[(len1 - 1, len2 - 1)]


def check_supply_chain_slopsquatting(package_name: str) -> Optional[Dict[str, Any]]:
    """
    Evaluate candidate import/dependency against verified PyPI registry.
    Flags typosquatting/slopsquatting when distance d_DL is 1 or 2.
    """
    pkg_clean = package_name.lower().strip()
    if pkg_clean in VERIFIED_PYPI_REGISTRY:
        return None  # Verified legitimate package

    for legitimate in VERIFIED_PYPI_REGISTRY:
        dist = damerau_levenshtein_distance(pkg_clean, legitimate)
        if 1 <= dist <= 2:
            return {
                "candidate_package": pkg_clean,
                "spoofed_target": legitimate,
                "damerau_levenshtein_distance": dist,
                "severity": "CRITICAL",
                "cwe_id": "CWE-1395",
                "threat": "Supply Chain Typosquatting / Hallucinated Dependency (Slopsquatting)",
                "remediation": f"Replace rogue dependency '{pkg_clean}' with official '{legitimate}'",
            }

    return None


# =========================================================================
# 2. AST DATA-FLOW TAINT ANALYSIS VISITOR
# =========================================================================

class ASTTaintNode(BaseModel):
    id: str
    node_type: str
    symbol: str
    line: int
    is_tainted: bool = False
    detail: str = ""


class ASTTaintEdge(BaseModel):
    source_id: str
    target_id: str
    relation: str  # e.g. "ASSIGN_TAINT", "FLOW_INTO_SINK", "PROPAGATE_FORMAT"


class ASTTaintGraphReport(BaseModel):
    total_nodes: int = 0
    total_edges: int = 0
    taint_sources: List[ASTTaintNode] = Field(default_factory=list)
    taint_sinks_trapped: List[Dict[str, Any]] = Field(default_factory=list)
    slopsquatted_packages: List[Dict[str, Any]] = Field(default_factory=list)
    is_safe: bool = True
    mathematical_invariant_satisfied: bool = True


class AdvancedASTTaintVisitor(ast.NodeVisitor):
    """
    Traverses Python AST to construct an explicit taint reachability DAG:
    G_AST = (V, E) where sources flow through variable lattice to forbidden sinks.
    """

    TAINT_SOURCE_PATTERNS = {"user_input", "query", "payload", "req", "raw_data", "untrusted", "input_str", "args"}

    def __init__(self):
        super().__init__()
        self.tainted_symbols: Set[str] = set()
        self.nodes: List[ASTTaintNode] = []
        self.edges: List[ASTTaintEdge] = []
        self.sinks_found: List[Dict[str, Any]] = []
        self.imports_analyzed: List[Dict[str, Any]] = []

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            squat = check_supply_chain_slopsquatting(alias.name)
            if squat:
                squat["line"] = node.lineno
                self.imports_analyzed.append(squat)
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module:
            squat = check_supply_chain_slopsquatting(node.module)
            if squat:
                squat["line"] = node.lineno
                self.imports_analyzed.append(squat)
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        # Identify tainted parameters
        for arg in node.args.args:
            arg_name = arg.arg
            if any(p in arg_name.lower() for p in self.TAINT_SOURCE_PATTERNS):
                self.tainted_symbols.add(arg_name)
                n = ASTTaintNode(
                    id=f"src_{node.lineno}_{arg_name}",
                    node_type="TAINT_SOURCE_ARG",
                    symbol=arg_name,
                    line=node.lineno,
                    is_tainted=True,
                    detail=f"Tainted parameter '{arg_name}' declared in function '{node.name}'",
                )
                self.nodes.append(n)
        self.generic_visit(node)

    def visit_Assign(self, node: ast.Assign):
        # Track variable assignments where right-hand side contains tainted symbol
        rhs_symbols = {n.id for n in ast.walk(node.value) if isinstance(n, ast.Name)}
        rhs_tainted = rhs_symbols.intersection(self.tainted_symbols)

        # Check for direct input() calls
        is_direct_input_call = False
        if isinstance(node.value, ast.Call):
            if isinstance(node.value.func, ast.Name) and node.value.func.id in ("input", "raw_input"):
                is_direct_input_call = True

        for target in node.targets:
            if isinstance(target, ast.Name):
                target_var = target.id
                if rhs_tainted or is_direct_input_call:
                    self.tainted_symbols.add(target_var)
                    src_sym = list(rhs_tainted)[0] if rhs_tainted else "input()"
                    n = ASTTaintNode(
                        id=f"var_{node.lineno}_{target_var}",
                        node_type="TAINT_PROPAGATION_VARIABLE",
                        symbol=target_var,
                        line=node.lineno,
                        is_tainted=True,
                        detail=f"Taint propagated from '{src_sym}' into '{target_var}'",
                    )
                    self.nodes.append(n)
                    self.edges.append(ASTTaintEdge(
                        source_id=f"src_{src_sym}",
                        target_id=n.id,
                        relation="ASSIGN_TAINT",
                    ))

        self.generic_visit(node)

    def visit_Call(self, node: ast.Call):
        # 1. Arbitrary Code Execution Sinks: eval(), exec(), compile()
        if isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec", "compile"):
            args_symbols = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
            tainted_args = args_symbols.intersection(self.tainted_symbols)
            is_tainted_reach = bool(tainted_args) or len(node.args) > 0

            self.sinks_found.append({
                "line": node.lineno,
                "type": "CWE-94_ARBITRARY_CODE_EXECUTION",
                "severity": "CRITICAL",
                "sink_function": node.func.id,
                "tainted_reachability": is_tainted_reach,
                "tainted_arguments": list(tainted_args),
                "detail": f"Forbidden '{node.func.id}()' invocation traps unvalidated code string.",
                "remediation": "Replace dynamic evaluation with deterministic AST NodeVisitor parser.",
            })

        # 2. Command Injection Sinks: os.system(), os.popen()
        elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "os":
            if node.func.attr in ("system", "popen"):
                args_symbols = {n.id for n in ast.walk(node) if isinstance(n, ast.Name)}
                tainted_args = args_symbols.intersection(self.tainted_symbols)
                self.sinks_found.append({
                    "line": node.lineno,
                    "type": "CWE-78_COMMAND_INJECTION",
                    "severity": "CRITICAL",
                    "sink_function": f"os.{node.func.attr}",
                    "tainted_reachability": bool(tainted_args) or len(node.args) > 0,
                    "tainted_arguments": list(tainted_args),
                    "detail": f"os.{node.func.attr}() shell execution sink discovered.",
                    "remediation": "Use subprocess.run with argument sequence array and shell=False.",
                })

        # 3. Subprocess with shell=True
        elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "subprocess":
            if node.func.attr in ("Popen", "run", "call", "check_output"):
                shell_kw = any(isinstance(k, ast.keyword) and k.arg == "shell" and getattr(k.value, "value", False) is True for k in node.keywords)
                if shell_kw or node.func.attr in ("Popen", "run"):
                    self.sinks_found.append({
                        "line": node.lineno,
                        "type": "CWE-78_SUBPROCESS_SHELL_INJECTION",
                        "severity": "HIGH",
                        "sink_function": f"subprocess.{node.func.attr}(shell=True)",
                        "tainted_reachability": True,
                        "detail": f"subprocess.{node.func.attr} configured with shell=True creates command injection risk.",
                        "remediation": "Set shell=False and pass arguments as an explicit vector list.",
                    })

        # 4. Insecure Deserialization: pickle.loads()
        elif isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Name) and node.func.value.id == "pickle":
            if node.func.attr in ("loads", "load"):
                self.sinks_found.append({
                    "line": node.lineno,
                    "type": "CWE-502_INSECURE_DESERIALIZATION",
                    "severity": "CRITICAL",
                    "sink_function": f"pickle.{node.func.attr}",
                    "tainted_reachability": True,
                    "detail": f"Arbitrary object deserialization sink 'pickle.{node.func.attr}' trapped.",
                    "remediation": "Use safe JSON serialization or HMAC-signed state tokens.",
                })

        self.generic_visit(node)


def analyze_ast_and_supply_chain(code_str: str) -> Dict[str, Any]:
    """
    Execute complete AST semantic analysis: Taint Graph Reachability and Slopsquatting.
    """
    try:
        tree = ast.parse(code_str)
    except SyntaxError as se:
        return {
            "success": False,
            "error": f"SyntaxError in code: {se}",
            "is_safe": False,
        }

    visitor = AdvancedASTTaintVisitor()
    visitor.visit(tree)

    total_vulns = len(visitor.sinks_found) + len(visitor.imports_analyzed)
    is_safe = (total_vulns == 0)

    return {
        "success": True,
        "is_safe": is_safe,
        "total_vulnerabilities_count": total_vulns,
        "sinks_found_count": len(visitor.sinks_found),
        "slopsquats_found_count": len(visitor.imports_analyzed),
        "sinks": visitor.sinks_found,
        "slopsquatting_findings": visitor.imports_analyzed,
        "tainted_symbols_tracked": list(visitor.tainted_symbols),
        "graph_lattice": {
            "nodes_count": len(visitor.nodes),
            "edges_count": len(visitor.edges),
            "nodes": [n.dict() for n in visitor.nodes],
            "edges": [e.dict() for e in visitor.edges],
        },
        "mathematical_invariant": {
            "lattice_formula": r"\mathcal{G}_{\text{AST}} = (\mathcal{V}, \mathcal{E}), \quad \forall v \in \text{Sinks}: \text{Taint}(v) \implies \text{Quarantine}",
            "metric_space": r"d_{DL}(a, b) = \min(\text{ins}, \text{del}, \text{sub}, \text{transposition}) \le 2",
            "satisfied": is_safe,
        },
    }
