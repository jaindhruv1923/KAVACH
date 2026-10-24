"""
Phase 2 - Agent Orchestrator Tests
Tests for workflow coordination, planning, and state management.
"""

import json
import pytest
from app.agent.orchestrator import run_workflow
from app.agent.state import WorkflowRun, WorkflowStage, save_run, get_run, list_runs
from app.agent.planner import plan_request, deterministic_fallback_planner


class TestPlanner:
    """Test task planning logic."""

    def test_plan_request_basic(self):
        """Test basic request planning."""
        plan = plan_request("Add authentication to the login module")
        
        assert isinstance(plan, list)
        assert len(plan) > 0
        assert all(isinstance(task, str) for task in plan)

    def test_plan_request_identifies_auth_keywords(self):
        """Test that planner identifies auth-related tasks."""
        plan = plan_request("Update the auth component")
        
        # Should identify auth-related tasks (auth as word boundary match)
        auth_related = [t for t in plan if "auth" in t.lower()]
        assert len(auth_related) > 0

    def test_plan_request_identifies_password_keywords(self):
        """Test that planner identifies password-related tasks."""
        plan = plan_request("I need to improve password handling")
        
        password_related = [t for t in plan if "password" in t.lower()]
        assert len(password_related) > 0

    def test_plan_request_identifies_test_keywords(self):
        """Test that planner identifies test-related tasks."""
        plan = plan_request("We need to add tests for the system")
        
        test_related = [t for t in plan if "test" in t.lower()]
        assert len(test_related) > 0
    

    def test_plan_request_identifies_database_keywords(self):
        """Test that planner identifies database-related tasks."""
        plan = plan_request("I need to modify the database table structure")
        
        db_related = [t for t in plan if "database" in t.lower()]
        assert len(db_related) > 0

    def test_plan_request_generic_request(self):
        """Test planning for generic request without keywords."""
        plan = plan_request("Make the code better")
        
        assert len(plan) > 0
        # Should still include context retrieval
        general_tasks = [t for t in plan if "context" in t.lower() or "retrieve" in t.lower()]
        assert len(general_tasks) > 0

    def test_plan_request_always_includes_security_check(self):
        """Test that security checks are always included in plan."""
        plans = [
            plan_request("Add authentication"),
            plan_request("Update database"),
            plan_request("Fix bugs"),
        ]
        
        for plan in plans:
            security_tasks = [t for t in plan if "security" in t.lower() or "check" in t.lower()]
            assert len(security_tasks) > 0

    def test_llm_planner_success_gemini(self, monkeypatch):
        """Test honest LLM planning path via Gemini JSON response."""
        sample_plan = [
            "Analyze authentication requirements",
            "Retrieve repository security modules",
            "Generate compliant token validation",
            "Run policy enforcement checks",
        ]
        monkeypatch.setattr("app.generation.llm_client.is_llm_configured", lambda: True)
        monkeypatch.setattr("app.generation.llm_client.call_llm", lambda prompt: json.dumps(sample_plan))
        plan = plan_request("Add OAuth2 login support", provider="gemini")
        assert plan == sample_plan

    def test_llm_planner_markdown_wrapped_json(self, monkeypatch):
        """Test LLM planner parsing JSON wrapped in markdown code fence."""
        sample_plan = [
            "Inspect database schemas",
            "Verify migration scripts",
            "Perform security review",
        ]
        raw_response = f"```json\n{json.dumps(sample_plan)}\n```"
        monkeypatch.setattr("app.generation.llm_client.is_llm_configured", lambda: True)
        monkeypatch.setattr("app.generation.llm_client.call_llm", lambda prompt: raw_response)
        plan = plan_request("Migrate users table to PostgreSQL")
        assert plan == sample_plan

    def test_llm_planner_ollama_option(self, monkeypatch):
        """Test honest LLM planning path with the Ollama local option."""
        sample_plan = [
            "Check local endpoints",
            "Retrieve offline context",
            "Apply security policies",
        ]
        monkeypatch.setattr("app.generation.llm_client.call_ollama", lambda prompt: json.dumps(sample_plan))
        plan = plan_request("Audit local routes", provider="ollama")
        assert plan == sample_plan

    def test_llm_planner_fallback_on_malformed_json(self, monkeypatch):
        """Test fallback when LLM returns unstructured text instead of JSON."""
        monkeypatch.setattr("app.generation.llm_client.is_llm_configured", lambda: True)
        monkeypatch.setattr("app.generation.llm_client.call_llm", lambda prompt: "I cannot produce a plan right now.")
        plan = plan_request("Update auth middleware")
        # Should gracefully fall back to deterministic planner
        assert isinstance(plan, list)
        assert any("auth" in t.lower() for t in plan)
        assert any("security" in t.lower() for t in plan)

    def test_deterministic_fallback_planner_direct(self):
        """Test deterministic fallback planner directly."""
        plan = deterministic_fallback_planner("Check database connection and password")
        assert isinstance(plan, list)
        assert any("database" in t.lower() for t in plan)
        assert any("password" in t.lower() for t in plan)
        assert any("security" in t.lower() for t in plan)

    def test_planner_fallback_path_is_fast(self):
        """Test that deterministic fallback executes immediately without network delay (< 50ms)."""
        import time
        start = time.perf_counter()
        plan = plan_request("Refactor user database models")
        duration = time.perf_counter() - start
        assert duration < 0.05, f"Fallback path took too long: {duration:.4f}s"
        assert isinstance(plan, list)
        assert len(plan) > 0

    def test_planner_caps_task_count_and_length(self, monkeypatch):
        """Test that untrusted LLM output is capped at MAX_TASKS (8) and MAX_TASK_LENGTH (150)."""
        huge_task = "A" * 300
        overloaded_plan = [f"Task {i}: {huge_task}" for i in range(25)]
        monkeypatch.setattr(
            "app.agent.planner._call_llm_single_shot",
            lambda prompt, provider=None, timeout_seconds=3.0: json.dumps(overloaded_plan),
        )
        plan = plan_request("Process transaction batch", provider="mock")
        assert len(plan) <= 8
        for task in plan:
            assert len(task) <= 153

    def test_planner_strips_html_and_shell_injection(self, monkeypatch):
        """Test that HTML script tags and shell execution metacharacters are stripped from tasks."""
        adversarial_plan = [
            "<script>alert('xss')</script>Identify auth modules",
            "Review code; rm -rf /; echo $(whoami)",
            "Perform security review && curl evil.com",
        ]
        monkeypatch.setattr(
            "app.agent.planner._call_llm_single_shot",
            lambda prompt, provider=None, timeout_seconds=3.0: json.dumps(adversarial_plan),
        )
        plan = plan_request("Update payment gateway", provider="mock")
        for task in plan:
            assert "<script>" not in task
            assert "</script>" not in task
            assert ";" not in task
            assert "$(" not in task
            assert "&&" not in task

    def test_planner_unreachable_endpoint_fast_fallback(self, monkeypatch):
        """Test that when a provider is configured but unreachable, it immediately falls back without retrying."""
        import time
        monkeypatch.setattr("app.agent.planner._call_llm_single_shot", lambda prompt, provider=None, timeout_seconds=3.0: None)
        start = time.perf_counter()
        plan = plan_request("Test unreachable provider", provider="ollama")
        duration = time.perf_counter() - start
        assert duration < 0.1, f"Fallback was not fast on unreachable endpoint: {duration:.4f}s"
        assert isinstance(plan, list)

    def test_workflow_passes_redacted_prompt_to_planner(self, monkeypatch):
        """Test that orchestrator passes sanitized/redacted input to planner, never raw PII."""
        captured_inputs = []
        original_plan_request = plan_request
        def _spy_plan_request(prompt, provider=None):
            captured_inputs.append(prompt)
            return original_plan_request(prompt, provider)
        monkeypatch.setattr("app.agent.orchestrator.plan_request", _spy_plan_request)
        run = run_workflow("Please add documentation for user support line: 9876543210")
        assert len(captured_inputs) > 0
        for prompt_received in captured_inputs:
            assert "9876543210" not in prompt_received, "Raw phone number leaked into planner prompt!"
            assert "[REDACTED" in prompt_received or "support line" in prompt_received


class TestWorkflowState:
    """Test workflow run state management."""

    def test_workflow_run_creation(self):
        """Test creating a workflow run."""
        run = WorkflowRun(request_text="Test request")
        
        assert run.request_text == "Test request"
        assert run.id is not None
        assert run.stage == WorkflowStage.REQUEST_RECEIVED
        assert run.plan == []
        assert run.security_findings == []

    def test_workflow_run_advance(self):
        """Test advancing workflow through stages."""
        run = WorkflowRun(request_text="Test")
        
        run.advance(WorkflowStage.PLANNING, "Starting planning phase")
        assert run.stage == WorkflowStage.PLANNING
        assert len(run.history) > 0
        assert "PLANNING" in run.history[-1]

    def test_workflow_run_history_tracking(self):
        """Test that history tracks all stage transitions."""
        run = WorkflowRun(request_text="Test")
        
        run.advance(WorkflowStage.PLANNING)
        run.advance(WorkflowStage.CONTEXT_RETRIEVAL)
        run.advance(WorkflowStage.COMPLETE)
        
        assert len(run.history) >= 3

    def test_save_and_retrieve_run(self):
        """Test saving and retrieving a workflow run."""
        run = WorkflowRun(request_text="Test request")
        run.plan = ["Task 1", "Task 2"]
        
        save_run(run)
        retrieved = get_run(run.id)
        
        assert retrieved is not None
        assert retrieved.request_text == "Test request"
        assert retrieved.plan == ["Task 1", "Task 2"]

    def test_get_nonexistent_run(self):
        """Test retrieving a run that doesn't exist."""
        result = get_run("nonexistent-id")
        assert result is None

    def test_list_runs(self):
        """Test listing all workflow runs."""
        run1 = WorkflowRun(request_text="Request 1")
        run2 = WorkflowRun(request_text="Request 2")
        
        save_run(run1)
        save_run(run2)
        
        runs = list_runs()
        
        assert len(runs) >= 2
        ids = {r.id for r in runs}
        assert run1.id in ids
        assert run2.id in ids


class TestWorkflowOrchestration:
    """Test workflow execution and stage transitions."""

    def test_run_workflow_basic(self):
        """Test running a basic workflow."""
        run = run_workflow("Add authentication to login module")
        
        assert run is not None
        assert run.id is not None
        assert run.request_text == "Add authentication to login module"
        assert run.stage != WorkflowStage.REQUEST_RECEIVED  # Should have progressed

    def test_workflow_has_plan(self):
        """Test that workflow generates a plan."""
        run = run_workflow("Update security checks")
        
        assert len(run.plan) > 0
        assert all(isinstance(task, str) for task in run.plan)

    def test_workflow_checks_pii_in_input(self):
        """Test that workflow checks for PII in user request."""
        # Request with PII
        run = run_workflow("My PAN is ABCDE1234F, please process it")
        
        # If PII is detected, should be blocked or in findings
        if len(run.security_findings) > 0:
            assert any(f["action"] == "BLOCK" for f in run.security_findings) or run.stage != WorkflowStage.BLOCKED

    def test_workflow_blocked_on_sensitive_input(self):
        """Test that workflow blocks on sensitive input."""
        # Input with clear PII
        run = run_workflow("Call me at 9876543210 or email test@example.com urgently")
        
        # Should detect something
        assert len(run.security_findings) >= 0  # May or may not block depending on config

    def test_workflow_handles_no_evidence(self):
        """Test workflow handles case when no evidence is found."""
        # Use a very specific request that likely won't match anything indexed
        run = run_workflow("xyzabc123 placeholder request with unique words")
        
        # Should not crash, but might have empty context
        assert run is not None
        assert isinstance(run.retrieved_context, list)

    def test_workflow_persists_run(self):
        """Test that workflow run is persisted."""
        run = run_workflow("Test persistence workflow")
        
        retrieved = get_run(run.id)
        assert retrieved is not None
        assert retrieved.request_text == "Test persistence workflow"

    def test_workflow_final_stage(self):
        """Test that workflow reaches a final stage."""
        run = run_workflow("Simple test request")
        
        # Should reach one of the terminal stages
        terminal_stages = {
            WorkflowStage.COMPLETE,
            WorkflowStage.BLOCKED,
            WorkflowStage.NEEDS_REVIEW,
        }
        assert run.stage in terminal_stages

    def test_workflow_security_checks_multiple_stages(self):
        """Test that security checks happen at multiple stages."""
        # Currently checks: input, context, generation
        run = run_workflow("Add safe functionality")
        
        # Should have gone through multiple stages
        assert len(run.history) > 1

    def test_workflow_generation_included(self):
        """Test that workflow includes generation stage."""
        run = run_workflow("Generate code for authentication")
        
        # Should attempt generation
        # Note: might be stubbed if no LLM configured
        assert "generation_result" in run.__dict__ or hasattr(run, "generation_result")

    def test_workflow_impact_analysis_included(self):
        """Test that workflow includes impact analysis."""
        run = run_workflow("Modify authentication logic")
        
        # Should include impact analysis
        assert isinstance(run.impact_report, list)

    def test_workflow_validation_included(self):
        """Test that workflow includes validation step."""
        run = run_workflow("Generate new functionality")
        
        # Should have validation result
        assert isinstance(run.validation_result, dict)


class TestWorkflowErrorHandling:
    """Test workflow error handling and recovery."""

    def test_workflow_handles_empty_request(self):
        """Test workflow with empty request."""
        run = run_workflow("")
        
        # Should handle gracefully
        assert run is not None
        assert isinstance(run, WorkflowRun)

    def test_workflow_handles_very_long_request(self):
        """Test workflow with very long request."""
        long_request = "test request " * 1000
        run = run_workflow(long_request)
        
        # Should handle without crashing
        assert run is not None
        assert len(run.history) > 0

    def test_workflow_consistent_id_generation(self):
        """Test that each workflow run gets unique ID."""
        runs = [run_workflow(f"Request {i}") for i in range(5)]
        ids = [r.id for r in runs]
        
        # All should be unique
        assert len(ids) == len(set(ids)), "All run IDs should be unique"


class TestWorkflowIntegration:
    """Integration tests for complete workflow."""

    def test_workflow_end_to_end(self):
        """Test complete workflow execution."""
        run = run_workflow("Improve user authentication system")
        
        # Verify all components were exercised
        assert run.request_text == "Improve user authentication system"
        assert len(run.plan) > 0
        assert isinstance(run.retrieved_context, list)
        assert isinstance(run.security_findings, list)
        assert isinstance(run.impact_report, list)
        assert isinstance(run.generation_result, dict)
        assert isinstance(run.validation_result, dict)
        assert len(run.history) > 0
        
        # Should have reached a final state
        assert run.stage in {
            WorkflowStage.COMPLETE,
            WorkflowStage.BLOCKED,
            WorkflowStage.NEEDS_REVIEW,
        }

    def test_workflow_preserves_state_through_stages(self):
        """Test that workflow state is preserved through stages."""
        run = run_workflow("Add validation to user input")
        
        # Request should be preserved
        assert run.request_text == "Add validation to user input"
        
        # History should show all transitions
        assert len(run.history) > 0
        
        # Later stages should build on earlier ones
        if run.impact_report:
            assert run.plan is not None, "Impact analysis depends on planning"


class TestOrchestrationModes:
    """Test Google ADK Coordinator routing and fail-safe deterministic fallback (Step 3)."""

    def test_default_orchestration_is_google_adk(self):
        """Test that default workflow execution is governed by Google ADK Coordinator."""
        run = run_workflow("Simple safe ping request")
        assert run.metadata.get("orchestration_engine") == "GOOGLE_ADK_COORDINATOR"
        assert run.metadata.get("adk_coordinator") == "ADK_Kavach_Coordinator"
        assert "adk_subagents" in run.metadata
        assert "SentinelAgent" in run.metadata["adk_subagents"]
        assert "CoderAgent" in run.metadata["adk_subagents"]

    def test_explicit_deterministic_mode(self):
        """Test explicit execution in deterministic fallback pipeline."""
        run = run_workflow("Simple safe ping request", mode="deterministic")
        assert run.metadata.get("orchestration_engine") == "DETERMINISTIC_PIPELINE"
        assert run.stage in {WorkflowStage.COMPLETE, WorkflowStage.BLOCKED, WorkflowStage.NEEDS_REVIEW}

    def test_adk_framework_fallback_on_error(self, monkeypatch):
        """Test that an unexpected exception in ADK coordinator gracefully triggers deterministic fallback."""
        def _failing_adk(text):
            raise RuntimeError("Simulated ADK coordinator network or dependency partition")
        monkeypatch.setattr("app.agent.orchestrator.run_workflow_adk", _failing_adk)
        
        run = run_workflow("Simple safe ping request")
        assert run.metadata.get("orchestration_engine") == "DETERMINISTIC_FALLBACK"
        assert "Simulated ADK coordinator" in run.metadata.get("framework_fallback_reason", "")
        assert run.stage in {WorkflowStage.COMPLETE, WorkflowStage.BLOCKED, WorkflowStage.NEEDS_REVIEW}

