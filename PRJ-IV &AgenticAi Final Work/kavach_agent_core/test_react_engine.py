"""
Comprehensive unit test suite for KAVACH ReAct Engine & Self-Correction Loop.
Course: CSE3101 Agentic AI - Final Capstone Project
"""

import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kavach_agent_core.react_engine import AutonomousReActEngine, ReActStep, AgentRunResult
from kavach_agent_core.llm_client import LLMClient


def test_react_engine_initialization():
    """Verify ReAct engine initializes with active model provider."""
    engine = AutonomousReActEngine()
    assert engine.max_iterations == 8
    assert engine.llm is not None
    provider = engine.llm.get_active_provider_name()
    assert len(provider) > 0


def test_react_engine_execution_on_dpdp_task():
    """Verify autonomous ReAct loop runs, calls tools, and terminates with FINISH."""
    engine = AutonomousReActEngine(max_iterations=5)
    captured_steps = []

    def on_step(step: ReActStep):
        captured_steps.append(step)

    goal = "Perform DPDP tokenization audit for user with Aadhaar 9999 9999 0019 and PAN ABCDE1234F"
    result: AgentRunResult = engine.run(goal=goal, on_step_callback=on_step)

    assert result.status == "COMPLETE"
    assert len(result.steps) >= 2
    assert len(captured_steps) == len(result.steps)

    # First step should have executed tool_dpdp_tokenize
    step1 = result.steps[0]
    assert step1.action == "tool_dpdp_tokenize"
    assert step1.observation.get("success") is True
    assert step1.observation.get("tokens_created_count") >= 2

    # Final step should be FINISH
    last_step = result.steps[-1]
    assert last_step.action == "FINISH"
    assert "DPDP" in result.final_answer or "token" in result.final_answer.lower()


def test_react_engine_execution_on_test_verification_task():
    """Verify autonomous ReAct loop runs pytest tool and verifies results."""
    engine = AutonomousReActEngine(max_iterations=5)
    goal = "Run pytest verification suite on test_tools.py to confirm all tools pass."
    result = engine.run(goal=goal)

    assert result.status == "COMPLETE"
    assert any(s.action == "tool_run_pytest" for s in result.steps)
    test_step = next(s for s in result.steps if s.action == "tool_run_pytest")
    assert test_step.observation.get("passed") is True


def test_react_engine_self_correction_behavior():
    """
    Test that when an action encounters an error, the engine marks the step,
    generates a Self-Reflection note, and increments self_corrections_count.
    """
    # Create an engine with a mock LLM that deliberately makes an error on step 1,
    # then observes the reflection and finishes on step 2.
    class MockSelfCorrectingLLM(LLMClient):
        def __init__(self):
            super().__init__()
            self.turn = 0

        def generate(self, prompt: str, system_instruction: str = "") -> str:
            self.turn += 1
            if self.turn == 1:
                # Intentionally call tool with invalid parameter to trigger error
                import json
                return json.dumps({
                    "thought": "I will attempt to read a non-existent file.",
                    "action": "tool_read_file",
                    "action_input": {"file_path": "non_existent_file_12345.py"}
                })
            else:
                # Second turn: observe error and finish
                import json
                return json.dumps({
                    "thought": "I see that the file was missing. I will self-correct and complete the task.",
                    "action": "FINISH",
                    "final_answer": "Successfully recovered from missing file through autonomous reflection."
                })

    mock_engine = AutonomousReActEngine(llm_client=MockSelfCorrectingLLM(), max_iterations=4)
    result = mock_engine.run(goal="Demonstrate self-correction after tool failure.")

    assert result.status == "COMPLETE"
    assert result.self_corrections_count >= 1
    assert result.steps[0].status == "ERROR"
    assert result.steps[0].reflection is not None
    assert "Reflexion" in result.steps[0].reflection or "Self-Reflection" in result.steps[0].reflection
    assert result.steps[1].action == "FINISH"
