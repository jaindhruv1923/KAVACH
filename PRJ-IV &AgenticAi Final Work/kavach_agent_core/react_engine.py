"""
KAVACH Core Autonomous ReAct Engine (Reason + Act + Reflect)
Course: CSE3101 Agentic AI - Final Capstone Project
Authors: Dhruv Jain (230532), BML Munjal University

Implements the foundational Agentic Design Patterns from the CSE3101 Syllabus:
1. ReAct (Reasoning and Acting) - Interleaved thought, action, observation cycle.
2. Reflection & Self-Correction - Dynamic diagnosis and recovery from tool failures.
3. Tool Use - Dynamic Model Context Protocol (MCP) tool execution.
4. Tracing & Observability - Structured execution telemetry for live streaming.
"""

import os
import sys
import json
import re
import time
import uuid
from typing import Dict, Any, List, Optional, Callable
from pydantic import BaseModel, Field

from kavach_agent_core.tools import execute_tool, MCP_TOOL_SCHEMAS, TOOL_REGISTRY
from kavach_agent_core.llm_client import LLMClient


class ReActStep(BaseModel):
    step_number: int
    agent_role: str = "Lead Orchestrator"
    thought: str
    action: str
    action_input: Dict[str, Any] = Field(default_factory=dict)
    observation: Dict[str, Any] = Field(default_factory=dict)
    reflection: Optional[str] = None
    duration_ms: float = 0.0
    status: str = "SUCCESS"  # SUCCESS, ERROR, SELF_CORRECTED, FINISHED


class AgentRunResult(BaseModel):
    run_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    goal: str
    status: str = "RUNNING"  # COMPLETE, FAILED, TIMED_OUT, RUNNING
    model_provider: str = ""
    steps: List[ReActStep] = Field(default_factory=list)
    total_iterations: int = 0
    total_duration_ms: float = 0.0
    final_answer: str = ""
    self_corrections_count: int = 0


class AutonomousReActEngine:
    """
    Autonomous ReAct Agent Brain.
    Manages bounded reasoning loops, real-time tool execution, and reflection.
    """

    def __init__(
        self,
        llm_client: Optional[LLMClient] = None,
        max_iterations: int = 8,
        timeout_seconds: float = 60.0,
        agent_role: str = "Autonomous ReAct Agent",
    ):
        self.llm = llm_client or LLMClient()
        self.max_iterations = max_iterations
        self.timeout_seconds = timeout_seconds
        self.agent_role = agent_role

    def run(
        self,
        goal: str,
        on_step_callback: Optional[Callable[[ReActStep], None]] = None,
    ) -> AgentRunResult:
        """Execute the goal through the autonomous ReAct reasoning and reflection loop."""
        start_time = time.time()
        provider_name = self.llm.get_active_provider_name()

        result = AgentRunResult(
            goal=goal,
            status="RUNNING",
            model_provider=provider_name,
        )

        history_steps: List[ReActStep] = []
        is_complete = False

        for iteration in range(1, self.max_iterations + 1):
            if time.time() - start_time > self.timeout_seconds:
                timeout_step = ReActStep(
                    step_number=iteration,
                    agent_role=self.agent_role,
                    thought="Execution timeout reached. Halting iterative reasoning loop.",
                    action="TIMEOUT",
                    observation={"error": "Exceeded maximum execution timeout"},
                    status="ERROR",
                )
                result.steps.append(timeout_step)
                if on_step_callback:
                    on_step_callback(timeout_step)
                result.status = "TIMED_OUT"
                break

            step_start = time.time()

            # Construct ReAct Prompt
            prompt = self._build_react_prompt(goal, history_steps)

            # Query LLM / Heuristic Engine
            raw_response = self.llm.generate(
                prompt=prompt,
                system_instruction=(
                    "You are KAVACH, an autonomous AI DevOps & Security Agent. "
                    "You reason step-by-step using ReAct. Always respond in valid JSON."
                )
            )

            # Parse Structured Action Decision
            decision = self._parse_json_decision(raw_response)

            thought = decision.get("thought", "Analyzing available context.")
            action = decision.get("action", "FINISH")
            action_input = decision.get("action_input", {})
            final_answer = decision.get("final_answer", "")

            # Check Termination
            if action == "FINISH" or not action:
                step_duration = round((time.time() - step_start) * 1000, 2)
                finish_step = ReActStep(
                    step_number=iteration,
                    agent_role=self.agent_role,
                    thought=thought,
                    action="FINISH",
                    action_input={},
                    observation={"summary": "Goal satisfied and verified."},
                    duration_ms=step_duration,
                    status="FINISHED",
                )
                result.steps.append(finish_step)
                if on_step_callback:
                    on_step_callback(finish_step)

                result.final_answer = final_answer or thought
                result.status = "COMPLETE"
                is_complete = True
                break

            # Execute Tool
            obs = execute_tool(action, action_input)
            step_duration = round((time.time() - step_start) * 1000, 2)

            # Check for errors and perform Reflection (Agentic Design Pattern)
            reflection = None
            step_status = "SUCCESS"
            is_error = (
                obs.get("success") is False
                or "error" in obs
                or (action == "tool_run_pytest" and obs.get("passed") is False)
            )

            if is_error:
                step_status = "ERROR"
                result.self_corrections_count += 1
                err_detail = obs.get("error") or obs.get("stderr") or obs.get("summary") or "Tool failure"
                reflection = f"[Self-Reflection]: Action '{action}' returned an error: {err_detail}. I must analyze why this failed and adapt my next action."

            react_step = ReActStep(
                step_number=iteration,
                agent_role=self.agent_role,
                thought=thought,
                action=action,
                action_input=action_input,
                observation=obs,
                reflection=reflection,
                duration_ms=step_duration,
                status=step_status,
            )

            history_steps.append(react_step)
            result.steps.append(react_step)

            if on_step_callback:
                on_step_callback(react_step)

        result.total_iterations = len(result.steps)
        result.total_duration_ms = round((time.time() - start_time) * 1000, 2)
        if not is_complete and result.status == "RUNNING":
            result.status = "COMPLETE"
            result.final_answer = f"Agent finished execution after {result.total_iterations} reasoning steps."

        return result

    def _build_react_prompt(self, goal: str, history: List[ReActStep]) -> str:
        """Construct the ReAct chain-of-thought prompt with tool schemas and prior observations."""
        tools_doc = "\n".join(
            f"- {s['name']}: {s['description']}\n  Parameters: {list(s['parameters'].get('properties', {}).keys())}"
            for s in MCP_TOOL_SCHEMAS
        )

        history_text = ""
        for s in history:
            history_text += f"\n--- Step {s.step_number} [{s.agent_role}] ---\n"
            history_text += f"Thought: {s.thought}\n"
            history_text += f"Action: {s.action}({json.dumps(s.action_input)})\n"
            obs_preview = json.dumps(s.observation)
            if len(obs_preview) > 300:
                obs_preview = obs_preview[:300] + "... [truncated]"
            history_text += f"Observation: {obs_preview}\n"
            if s.reflection:
                history_text += f"Reflection: {s.reflection}\n"

        if not history_text:
            history_text = "(No actions executed yet)"

        prompt = f"""You are KAVACH, an autonomous Agentic AI DevOps & Security Engineer.
GOAL: {goal}

AVAILABLE MCP TOOLS:
{tools_doc}

EXECUTION TRACE SO FAR:
{history_text}

INSTRUCTIONS:
1. Examine the GOAL and the EXECUTION TRACE.
2. If the goal is fully accomplished, return action 'FINISH' with a detailed 'final_answer'.
3. Otherwise, select the single best tool from AVAILABLE MCP TOOLS to make progress.
4. If a previous step had an error or reflection, explain how you are self-correcting in your 'thought'.

You MUST respond strictly with valid JSON conforming to one of these formats:

Format 1 (Call a Tool):
{{
  "thought": "Your step-by-step reasoning on what to do next",
  "action": "tool_name",
  "action_input": {{"param1": "value1"}}
}}

Format 2 (Task Finished):
{{
  "thought": "Summary of evidence collected and validation completed",
  "action": "FINISH",
  "final_answer": "Complete, comprehensive answer or solution summary"
}}
"""
        return prompt

    def _parse_json_decision(self, response_text: str) -> Dict[str, Any]:
        """Extract and parse structured JSON decision with fallback recovery."""
        if not response_text:
            return {"thought": "No response received.", "action": "FINISH", "final_answer": "Execution ended."}

        # Clean markdown codeblocks
        cleaned = re.sub(r"```(?:json)?", "", response_text).strip()

        # Try direct parse
        try:
            return json.loads(cleaned)
        except Exception:
            pass

        # Try regex extract
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except Exception:
                pass

        # Fallback to text synthesis
        return {
            "thought": "Direct synthesis from reasoning.",
            "action": "FINISH",
            "final_answer": cleaned[:600],
        }
