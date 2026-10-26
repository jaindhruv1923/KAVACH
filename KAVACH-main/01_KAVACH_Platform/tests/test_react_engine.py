"""
Unit tests for KAVACH Bounded ReAct Execution Engine (app/agent/react_engine.py).
Verifies iterative reasoning-acting loops, tool execution, multi-agent handoffs,
security gates, and empirical results.
"""

import pytest
from app.agent.react_engine import AgenticReActEngine, AgentExecutionResult


def test_react_engine_halts_on_sensitive_input():
    """Verify pre-execution security gate immediately halts prompt with leaked credentials."""
    engine = AgenticReActEngine(max_iterations=4)
    res = engine.run("Deploy worker with Aadhaar 9876 5432 1098 and AWS_KEY AKIAIOSFODNN7EXAMPLE")
    assert res.status == "BLOCKED"
    assert len(res.security_findings) >= 2
    assert len(res.steps) == 0  # Zero tool calls allowed
    assert "halted by Kavach Security Policy" in res.final_output


def test_react_engine_executes_real_tests():
    """Verify engine runs real allowlisted tests and incorporates observation."""
    engine = AgenticReActEngine(max_iterations=4)
    res = engine.run("Run health check test verification")
    assert res.status == "COMPLETE"
    assert res.total_iterations >= 2
    tool_steps = [s for s in res.steps if s.action == "run_allowlisted_tests"]
    assert len(tool_steps) == 1
    step = tool_steps[0]
    assert step.agent_role == "CodeVerifier"
    assert step.observation["passed"] is True
    assert "artifacts" in res.model_dump()
    assert "test_run" in res.artifacts


def test_react_engine_code_search_and_read():
    """Verify multi-step search and read workflow."""
    engine = AgenticReActEngine(max_iterations=4)
    res = engine.run("Search for run_workflow in codebase and inspect its definition")
    assert res.status == "COMPLETE"
    actions = [s.action for s in res.steps]
    assert "repo_search_code" in actions
    assert "repo_read_file" in actions
    inspector_steps = [s for s in res.steps if s.agent_role == "RepositoryInspector"]
    assert len(inspector_steps) >= 2


def test_react_engine_blast_radius_analysis():
    """Verify AST dependency analysis invocation and artifact generation."""
    engine = AgenticReActEngine(max_iterations=4)
    res = engine.run("Calculate change impact and blast radius for detector.py")
    assert res.status == "COMPLETE"
    impact_steps = [s for s in res.steps if s.action == "ast_analyze_impact"]
    assert len(impact_steps) == 1
    assert "blast_radius" in res.artifacts
    assert res.artifacts["blast_radius"]["score"] >= 0.0


def test_react_engine_patch_proposal():
    """Verify patch generation and Human-in-the-Loop approval gate."""
    engine = AgenticReActEngine(max_iterations=4)
    res = engine.run("Propose a patch for planner.py")
    assert res.status == "COMPLETE"
    patch_steps = [s for s in res.steps if s.action == "propose_code_patch"]
    assert len(patch_steps) == 1
    assert "proposed_patch" in res.artifacts
    assert res.artifacts["proposed_patch"]["diff"] is not None


def test_react_engine_trace_structure_and_timings():
    """Verify structured trace contains all observability fields."""
    engine = AgenticReActEngine(max_iterations=3)
    res = engine.run("Inspect repository structure")
    assert res.total_duration_ms > 0
    assert len(res.steps) >= 2
    for s in res.steps:
        assert s.step_number > 0
        assert s.agent_role in ["Coordinator", "RepositoryInspector", "SecurityAuditor", "CodeVerifier"]
        assert s.thought != ""
        assert s.action != ""
        assert isinstance(s.duration_ms, float)
