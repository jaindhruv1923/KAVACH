"""
Unit Tests for Adaptive Self-Correction & Reflexion Engine (CSE3101 Stage 2)
Course: CSE3101 Agentic AI - Final Capstone Project
Authors: Dhruv Jain (230532), BML Munjal University
"""

import pytest
from kavach_agent_core.reflexion_engine import SelfCorrectionEngine, ReflexionEpisode, ReflexionMemory


def test_reflexion_engine_pytest_diagnosis():
    engine = SelfCorrectionEngine(max_reflection_budget=3)
    episode = engine.diagnose_and_reflect(
        agent_name="VerifierCritic",
        action="tool_run_pytest",
        action_input={"test_path": "kavach_agent_core/test_tools.py"},
        observation={"passed": False, "summary": "1 failed, 20 passed", "stderr": "AssertionError: 5 != 0"},
        cycle_number=1,
    )

    assert episode.trigger_event == "PYTEST_ASSERTION_FAILED"
    assert "assertion failure" in episode.root_cause_diagnosis.lower()
    assert episode.loss_before == 1.0
    assert episode.loss_after == 0.0
    assert episode.status == "RESOLVED"
    assert episode.corrective_action == "tool_edit_file"


def test_reflexion_engine_ast_vulnerability_diagnosis():
    engine = SelfCorrectionEngine(max_reflection_budget=3)
    episode = engine.diagnose_and_reflect(
        agent_name="SecurityAuditor",
        action="tool_ast_security_scan",
        action_input={"content_or_file_path": "def run(x): eval(x)"},
        observation={"vulnerabilities_found": 1, "error": "Direct call to forbidden 'eval()'"},
        cycle_number=1,
    )

    assert episode.trigger_event == "AST_VULNERABILITY_DETECTED"
    assert "ast nodevisitor" in episode.root_cause_diagnosis.lower()
    assert "safe_eval_ast" in episode.corrective_input["replacement_string"]


def test_reflexion_memory_verbal_context():
    mem = ReflexionMemory()
    assert mem.get_verbal_refinement_context() == ""

    ep = ReflexionEpisode(
        agent_name="DevOpsCoder",
        cycle_number=1,
        trigger_event="AST_VULNERABILITY_DETECTED",
        failed_action="tool_write_file",
        observation_summary="Dangerous sink eval() introduced",
        root_cause_diagnosis="AST NodeVisitor trapped eval()",
        counterfactual_heuristic="Use parameterized literal_eval instead",
        corrective_action="tool_edit_file",
    )
    mem.add_episode(ep)
    assert mem.total_corrections_attempted == 1
    assert mem.total_corrections_resolved == 1

    context = mem.get_verbal_refinement_context()
    assert "[ADAPTIVE REFLEXION MEMORY" in context
    assert "Cycle #1" in context
    assert "DevOpsCoder" in context


def test_reflexion_budget_capping():
    engine = SelfCorrectionEngine(max_reflection_budget=3)
    episode = engine.diagnose_and_reflect(
        agent_name="DevOpsCoder",
        action="tool_list_files",
        action_input={},
        observation={"error": "Disk failure"},
        cycle_number=5,  # Exceeds budget of 3
    )
    assert episode.cycle_number == 3
