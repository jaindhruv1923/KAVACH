"""
Specialized Multi-Agent Roles & Delegation Architecture for KAVACH (Phase 4).

Complies with CSE3101 Module 4 & 5:
- Specialized agent personas with distinct responsibilities and bounded tools
- Coordinator-Worker delegation pattern
- Explicit observable handoffs between agents with structured message passing
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class AgentPersona(BaseModel):
    name: str
    role: str
    goal: str
    backstory: str
    allowed_tools: List[str]
    max_steps: int = 4


COORDINATOR_PERSONA = AgentPersona(
    name="Coordinator",
    role="Lead Systems Architect & Dispatcher",
    goal="Decompose the user's software engineering goal, delegate subtasks to specialists, and synthesize final verified results.",
    backstory="Senior engineering lead with deep knowledge of the KAVACH platform architecture, responsible for directing specialized agents without performing low-level operations directly.",
    allowed_tools=["repo_list_tree", "ast_analyze_impact"],
    max_steps=3,
)

INSPECTOR_PERSONA = AgentPersona(
    name="RepositoryInspector",
    role="Source Code & File Navigator",
    goal="Inspect repository structure, locate relevant code files, search patterns, and retrieve source context.",
    backstory="Specialist in Python static analysis and filesystem navigation, capable of pinpointing exact functions, imports, and variables across repositories.",
    allowed_tools=["repo_list_tree", "repo_read_file", "repo_search_code"],
    max_steps=4,
)

SECURITY_AUDITOR_PERSONA = AgentPersona(
    name="SecurityAuditor",
    role="Zero-Trust Policy & Guardrail Enforcer",
    goal="Inspect inputs, code diffs, and tool observations for Indian PII, high-entropy secrets, and indirect prompt injections.",
    backstory="Cybersecurity specialist enforcing DPDP Act 2023, RBI compliance, and OWASP LLM Top 10 defenses before any code is modified or executed.",
    allowed_tools=["security_scan_code", "ast_analyze_impact"],
    max_steps=3,
)

VERIFIER_PERSONA = AgentPersona(
    name="CodeVerifier",
    role="Test Execution & Quality Engineer",
    goal="Execute allowlisted pytest suites, inspect syntax, parse test tracebacks, and verify patches.",
    backstory="Meticulous test automation engineer who insists on empirical evidence from real test runs before declaring any task successful.",
    allowed_tools=["run_allowlisted_tests", "propose_code_patch", "apply_approved_patch"],
    max_steps=4,
)

ALL_PERSONAS = {
    "Coordinator": COORDINATOR_PERSONA,
    "RepositoryInspector": INSPECTOR_PERSONA,
    "SecurityAuditor": SECURITY_AUDITOR_PERSONA,
    "CodeVerifier": VERIFIER_PERSONA,
}


class AgentHandoff(BaseModel):
    from_agent: str
    to_agent: str
    reason: str
    context_keys: List[str]
    timestamp: float


def select_agent_for_action(tool_name: str) -> AgentPersona:
    """Determine the responsible agent persona based on the requested tool."""
    for persona in [SECURITY_AUDITOR_PERSONA, VERIFIER_PERSONA, INSPECTOR_PERSONA, COORDINATOR_PERSONA]:
        if tool_name in persona.allowed_tools:
            return persona
    return COORDINATOR_PERSONA
