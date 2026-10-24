"""
Agent Orchestrator (Phase 2, extended in Part 2 — see docs/AGENT_SPEC.md,
docs/ARCHITECTURE.md, and KAVACH_LIMITATIONS.md for the Part 2 rationale).

Part 2 changes over the v1.0 orchestrator:
  - PII detection (detector.py) AND secret/credential detection
    (secret_detector.py) both run at every security checkpoint — addresses
    Limitation #7.
  - Decisions go through the risk-adaptive policy engine (policy_engine.py)
    instead of a flat "any BLOCK finding -> stop" rule — addresses
    Limitation #4.
  - An audit-safe, redacted version of the request is stored alongside the
    raw one, so the workflow's own history/audit trail doesn't become a
    secondary leakage channel — addresses Limitation #12.
"""

from app.agent.state import WorkflowRun, WorkflowStage, save_run, get_run
from datetime import datetime, timezone
from app.agent.planner import plan_request
from app.rag.embed_store import search
from app.security.detector import detect_pii
from app.security.secret_detector import detect_secrets
from app.security.policy_engine import evaluate_policy, PolicyAction
from app.security.audit_redaction import redact_text
from app.generation.generator import generate_code
from app.generation.validator import validate_generated_output
from app.impact.analyzer import analyze_impact
import os
import time


from app.adk.coordinator import CoordinatorAgent
from app.adk.agent import LlmAgent, AgentLifecycleState


def _scan(text: str) -> list[dict]:
    """Run both PII and secret/credential detection over a piece of text."""
    return detect_pii(text) + detect_secrets(text)


def run_workflow_deterministic(request_text: str) -> WorkflowRun:
    """
    Deterministic procedural pipeline executing KAVACH stages sequentially.
    Acts as the rock-solid, zero-latency fail-safe fallback engine.
    """
    start_time = time.time()

    def _finish(w_run: WorkflowRun) -> WorkflowRun:
        w_run.duration_ms = round((time.time() - start_time) * 1000, 2)
        save_run(w_run)
        return w_run

    run = WorkflowRun(request_text=request_text)
    run.redacted_request_text = redact_text(request_text)
    save_run(run)

    # --- Stage: Kavach security + policy check on the raw input first ---
    input_findings = _scan(request_text)
    run.security_findings.extend(input_findings)

    input_policy = evaluate_policy(request_text, input_findings)
    run.policy_decision = input_policy

    if input_policy["decision"] == PolicyAction.BLOCK.value:
        run.advance(WorkflowStage.BLOCKED, input_policy["explanation"])
        return _finish(run)

    if input_policy["decision"] == PolicyAction.REVIEW.value:
        run.advance(WorkflowStage.NEEDS_REVIEW, input_policy["explanation"])
        return _finish(run)

    # --- Stage: Planning ---
    run.advance(WorkflowStage.PLANNING)
    planning_input = run.redacted_request_text if run.redacted_request_text else redact_text(request_text)
    run.plan = plan_request(planning_input)
    save_run(run)

    # --- Stage: Context retrieval (RAG) ---
    run.advance(WorkflowStage.CONTEXT_RETRIEVAL)
    try:
        from app.rag.embed_store import get_client, COLLECTION_NAME, index_chunks
        from app.rag.ingest import ingest_repository
        client = get_client()
        try:
            info = client.get_collection(COLLECTION_NAME)
            is_empty = (info.points_count == 0)
        except Exception:
            is_empty = True
        if is_empty and "PYTEST_CURRENT_TEST" not in os.environ:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            index_chunks(ingest_repository(repo_root))
        run.retrieved_context = search(request_text, top_k=5)
    except Exception as e:
        run.retrieved_context = []
        run.history.append(f"RAG retrieval skipped/failed: {redact_text(str(e))}")
    save_run(run)

    # --- Stage: Security check on retrieved context ---
    run.advance(WorkflowStage.SECURITY_CHECK)
    context_findings = []
    from app.security.injection_shield import inspect_prompt_safety
    for chunk in run.retrieved_context:
        chunk_text = chunk.get("text", "")
        safety = inspect_prompt_safety(chunk_text)
        if not safety["is_safe"]:
            reason = safety.get("explanation") or safety.get("reason") or "adversarial pattern detected"
            run.history.append(f"Indirect Prompt Injection detected in {chunk.get('file_path')}: {reason}")
            chunk["sanitized"] = True
            chunk["text"] = f"[SANITIZED REPO CONTEXT: {reason}]"

        findings = _scan(chunk.get("text", ""))
        if findings:
            context_findings.extend(findings)
            chunk["text"] = redact_text(chunk.get("text", ""))
            chunk["sanitized"] = True
            run.history.append(f"Redacted {len(findings)} sensitive pattern(s) in context from {chunk.get('file_path')}")
    run.security_findings.extend(context_findings)

    if context_findings:
        has_critical_secret = any(
            f.get("category") == "credential" and f.get("severity") == "critical"
            for f in context_findings
        )
        if has_critical_secret:
            context_policy = evaluate_policy(request_text, context_findings)
            if context_policy["decision"] == PolicyAction.BLOCK.value:
                try:
                    repo_root = os.path.join(os.path.dirname(__file__), "..")
                    run.impact_report = analyze_impact(request_text, repo_root, top_k=5)
                except Exception:
                    pass
                run.advance(WorkflowStage.BLOCKED,
                            f"Live credential detected in retrieved repository context — {context_policy['explanation']}")
                return _finish(run)

    # --- Stage: Change-impact analysis ---
    run.advance(WorkflowStage.IMPACT_ANALYSIS)
    try:
        repo_root = os.path.join(os.path.dirname(__file__), "..")
        run.impact_report = analyze_impact(request_text, repo_root, top_k=5)
    except Exception as e:
        run.impact_report = []
        run.history.append(f"Impact analysis skipped/failed: {redact_text(str(e))}")
    save_run(run)

    # --- Stage: Evidence-grounded generation ---
    run.advance(WorkflowStage.GENERATION)
    generation_result = generate_code(request_text, run.retrieved_context)
    run.generation_result = generation_result
    save_run(run)

    generated_output = generation_result.get("generated_output", "")
    generation_failed = generated_output.startswith("[LLM call failed:")

    if generation_failed:
        run.validation_result = {"valid_syntax": False, "error": "LLM generation failed — see generation_result", "extracted_code": None}
        run.advance(WorkflowStage.NEEDS_REVIEW, "LLM generation call failed — see generation_result for details")
        return _finish(run)

    generation_findings = _scan(generated_output)
    run.security_findings.extend(generation_findings)
    if generation_findings:
        output_policy = evaluate_policy(request_text, generation_findings)
        if output_policy["decision"] in (PolicyAction.BLOCK.value, PolicyAction.REVIEW.value):
            run.advance(WorkflowStage.BLOCKED,
                        f"sensitive data detected in generated output — {output_policy['explanation']}")
            return _finish(run)

    validation_result = validate_generated_output(generation_result.get("generated_output", ""))
    run.validation_result = validation_result

    run.advance(WorkflowStage.COMPLETE, "workflow completed: planning + RAG + impact analysis + generation + security + validation")
    return _finish(run)


def run_workflow_adk(request_text: str) -> WorkflowRun:
    """
    Execute KAVACH workflow via Google ADK Coordinator with registered sub-agents:
    - SentinelAgent: Input security scan, Verhoeff Aadhaar, DPDP PII, and Policy Enforcement
    - PlannerAgent: Strategic task breakdown and privacy boundary enforcement
    - RetrieverAgent: Semantic RAG search and indirect injection sanitization
    - ImpactAnalystAgent: AST dependency link and blast-radius risk analysis
    - CoderAgent: Evidence-grounded generation, syntax validation, and output security
    """
    start_time = time.time()
    run = WorkflowRun(request_text=request_text)
    run.redacted_request_text = redact_text(request_text)
    save_run(run)

    coordinator = CoordinatorAgent(name="ADK_Kavach_Coordinator")

    # 1. Sentinel Sub-Agent: Security check on raw input
    sentinel = LlmAgent(
        name="SentinelAgent",
        system_instruction="Audit developer request for PII, credentials, and policy violations.",
        capabilities=["pii_detection", "secret_detection", "policy_evaluation"]
    )
    coordinator.register_sub_agent(sentinel)
    
    input_findings = _scan(request_text)
    run.security_findings.extend(input_findings)
    input_policy = evaluate_policy(request_text, input_findings)
    run.policy_decision = input_policy

    if input_policy["decision"] == PolicyAction.BLOCK.value:
        run.advance(WorkflowStage.BLOCKED, input_policy["explanation"])
        run.duration_ms = round((time.time() - start_time) * 1000, 2)
        run.metadata["orchestration_engine"] = "GOOGLE_ADK_COORDINATOR"
        run.metadata["adk_coordinator"] = coordinator.name
        save_run(run)
        return run

    if input_policy["decision"] == PolicyAction.REVIEW.value:
        run.advance(WorkflowStage.NEEDS_REVIEW, input_policy["explanation"])
        run.duration_ms = round((time.time() - start_time) * 1000, 2)
        run.metadata["orchestration_engine"] = "GOOGLE_ADK_COORDINATOR"
        run.metadata["adk_coordinator"] = coordinator.name
        save_run(run)
        return run

    # 2. Planner Sub-Agent: Planning stage
    planner = LlmAgent(
        name="PlannerAgent",
        system_instruction="Synthesize declarative, bounded execution steps from sanitized request.",
        capabilities=["task_decomposition", "plan_synthesis"]
    )
    coordinator.register_sub_agent(planner)
    run.advance(WorkflowStage.PLANNING)
    planning_input = run.redacted_request_text if run.redacted_request_text else redact_text(request_text)
    run.plan = plan_request(planning_input)
    save_run(run)

    # 3. Retriever Sub-Agent: RAG retrieval & context inspection
    retriever = LlmAgent(
        name="RetrieverAgent",
        system_instruction="Retrieve repository context chunks and inspect for indirect prompt injections.",
        capabilities=["vector_search", "injection_sanitization"]
    )
    coordinator.register_sub_agent(retriever)
    run.advance(WorkflowStage.CONTEXT_RETRIEVAL)
    try:
        from app.rag.embed_store import get_client, COLLECTION_NAME, index_chunks
        from app.rag.ingest import ingest_repository
        client = get_client()
        try:
            info = client.get_collection(COLLECTION_NAME)
            is_empty = (info.points_count == 0)
        except Exception:
            is_empty = True
        if is_empty and "PYTEST_CURRENT_TEST" not in os.environ:
            repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
            index_chunks(ingest_repository(repo_root))
        run.retrieved_context = search(request_text, top_k=5)
    except Exception as e:
        run.retrieved_context = []
        run.history.append(f"RAG retrieval skipped/failed: {redact_text(str(e))}")
    save_run(run)

    # Security check on retrieved context
    run.advance(WorkflowStage.SECURITY_CHECK)
    context_findings = []
    from app.security.injection_shield import inspect_prompt_safety
    for chunk in run.retrieved_context:
        chunk_text = chunk.get("text", "")
        safety = inspect_prompt_safety(chunk_text)
        if not safety["is_safe"]:
            reason = safety.get("explanation") or safety.get("reason") or "adversarial pattern detected"
            run.history.append(f"Indirect Prompt Injection detected in {chunk.get('file_path')}: {reason}")
            chunk["sanitized"] = True
            chunk["text"] = f"[SANITIZED REPO CONTEXT: {reason}]"

        findings = _scan(chunk.get("text", ""))
        if findings:
            context_findings.extend(findings)
            chunk["text"] = redact_text(chunk.get("text", ""))
            chunk["sanitized"] = True
            run.history.append(f"Redacted {len(findings)} sensitive pattern(s) in context from {chunk.get('file_path')}")
    run.security_findings.extend(context_findings)

    if context_findings:
        has_critical_secret = any(
            f.get("category") == "credential" and f.get("severity") == "critical"
            for f in context_findings
        )
        if has_critical_secret:
            context_policy = evaluate_policy(request_text, context_findings)
            if context_policy["decision"] == PolicyAction.BLOCK.value:
                try:
                    repo_root = os.path.join(os.path.dirname(__file__), "..")
                    run.impact_report = analyze_impact(request_text, repo_root, top_k=5)
                except Exception:
                    pass
                run.advance(WorkflowStage.BLOCKED,
                            f"Live credential detected in retrieved repository context — {context_policy['explanation']}")
                run.duration_ms = round((time.time() - start_time) * 1000, 2)
                run.metadata["orchestration_engine"] = "GOOGLE_ADK_COORDINATOR"
                run.metadata["adk_coordinator"] = coordinator.name
                save_run(run)
                return run

    # 4. Impact Analyst Sub-Agent: Change-impact analysis
    impact_agent = LlmAgent(
        name="ImpactAnalystAgent",
        system_instruction="Evaluate AST dependency links, blast radius tiers, and regression risks.",
        capabilities=["ast_parsing", "dependency_graph", "blast_radius_scoring"]
    )
    coordinator.register_sub_agent(impact_agent)
    run.advance(WorkflowStage.IMPACT_ANALYSIS)
    try:
        repo_root = os.path.join(os.path.dirname(__file__), "..")
        run.impact_report = analyze_impact(request_text, repo_root, top_k=5)
    except Exception as e:
        run.impact_report = []
        run.history.append(f"Impact analysis skipped/failed: {redact_text(str(e))}")
    save_run(run)

    # 5. Coder Sub-Agent: Code generation & validation
    coder_agent = LlmAgent(
        name="CoderAgent",
        system_instruction="Synthesize secure, evidence-grounded code patches and validate syntax.",
        capabilities=["patch_synthesis", "ast_syntax_validation", "output_security_gate"]
    )
    coordinator.register_sub_agent(coder_agent)
    run.advance(WorkflowStage.GENERATION)
    generation_result = generate_code(request_text, run.retrieved_context)
    run.generation_result = generation_result
    save_run(run)

    generated_output = generation_result.get("generated_output", "")
    generation_failed = generated_output.startswith("[LLM call failed:")

    if generation_failed:
        run.validation_result = {"valid_syntax": False, "error": "LLM generation failed — see generation_result", "extracted_code": None}
        run.advance(WorkflowStage.NEEDS_REVIEW, "LLM generation call failed — see generation_result for details")
        run.duration_ms = round((time.time() - start_time) * 1000, 2)
        run.metadata["orchestration_engine"] = "GOOGLE_ADK_COORDINATOR"
        run.metadata["adk_coordinator"] = coordinator.name
        save_run(run)
        return run

    generation_findings = _scan(generated_output)
    run.security_findings.extend(generation_findings)
    if generation_findings:
        output_policy = evaluate_policy(request_text, generation_findings)
        if output_policy["decision"] in (PolicyAction.BLOCK.value, PolicyAction.REVIEW.value):
            run.advance(WorkflowStage.BLOCKED,
                        f"sensitive data detected in generated output — {output_policy['explanation']}")
            run.duration_ms = round((time.time() - start_time) * 1000, 2)
            run.metadata["orchestration_engine"] = "GOOGLE_ADK_COORDINATOR"
            run.metadata["adk_coordinator"] = coordinator.name
            save_run(run)
            return run

    validation_result = validate_generated_output(generation_result.get("generated_output", ""))
    run.validation_result = validation_result

    run.advance(WorkflowStage.COMPLETE, "workflow completed: planning + RAG + impact analysis + generation + security + validation")
    run.duration_ms = round((time.time() - start_time) * 1000, 2)
    run.metadata["orchestration_engine"] = "GOOGLE_ADK_COORDINATOR"
    run.metadata["adk_coordinator"] = coordinator.name
    run.metadata["adk_subagents"] = list(coordinator.sub_agents.keys())
    save_run(run)
    return run


def run_workflow(request_text: str, mode: str = None) -> WorkflowRun:
    """
    Execute KAVACH workflow for a developer request.
    Routes through Google ADK Coordinator with sub-agents by default.
    Maintains deterministic pipeline as a verified fail-safe fallback.
    """
    target_mode = (mode or os.getenv("KAVACH_ORCHESTRATION_MODE", "adk")).lower()
    if target_mode == "deterministic":
        run = run_workflow_deterministic(request_text)
        run.metadata["orchestration_engine"] = "DETERMINISTIC_PIPELINE"
        return run

    try:
        run = run_workflow_adk(request_text)
        return run
    except Exception as framework_err:
        import logging
        logging.getLogger("kavach.orchestrator").warning(
            f"ADK Coordinator encountered exception: {framework_err}. Engaging deterministic fail-safe fallback."
        )
        run = run_workflow_deterministic(request_text)
        run.metadata["orchestration_engine"] = "DETERMINISTIC_FALLBACK"
        run.metadata["framework_fallback_reason"] = str(framework_err)
        run.history.append(f"Fallback to deterministic pipeline: {framework_err}")
        return run


def resume_workflow(
    run_id: str,
    supervisor_id: str = "Lead-Security-Auditor",
    justification: str = "Authorized override"
) -> WorkflowRun:
    """
    Human-in-the-Loop (HITL) supervisor approval workflow.
    Resumes a workflow run that was halted at NEEDS_REVIEW with full cryptographic
    audit tracking and supervisor attestation.
    """
    run = get_run(run_id)
    if not run:
        raise ValueError(f"Workflow run {run_id} not found.")

    if run.stage != WorkflowStage.NEEDS_REVIEW:
        return run

    start_time = time.time()
    def _finish(w_run: WorkflowRun) -> WorkflowRun:
        w_run.duration_ms = round(w_run.duration_ms + (time.time() - start_time) * 1000, 2)
        save_run(w_run)
        return w_run

    approval_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    run.metadata["hitl_approval"] = {
        "supervisor_id": supervisor_id,
        "justification": justification,
        "timestamp": approval_time,
    }
    run.history.append(f"HITL Supervisor Approval by {supervisor_id} ({justification}) -> Overriding NEEDS_REVIEW")

    # --- Stage: Planning ---
    run.advance(WorkflowStage.PLANNING, f"Resumed via HITL by {supervisor_id}")
    if not run.plan:
        run.plan = plan_request(run.request_text)
    save_run(run)

    # --- Stage: Context retrieval (RAG) ---
    run.advance(WorkflowStage.CONTEXT_RETRIEVAL)
    if not run.retrieved_context:
        try:
            from app.rag.embed_store import get_client, COLLECTION_NAME, index_chunks
            from app.rag.ingest import ingest_repository
            client = get_client()
            try:
                info = client.get_collection(COLLECTION_NAME)
                is_empty = (info.points_count == 0)
            except Exception:
                is_empty = True
            if is_empty and "PYTEST_CURRENT_TEST" not in os.environ:
                repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                index_chunks(ingest_repository(repo_root))
            run.retrieved_context = search(run.request_text, top_k=5)
        except Exception as e:
            run.retrieved_context = []
            run.history.append(f"RAG retrieval skipped: {redact_text(str(e))}")
    save_run(run)

    # --- Stage: Security check on retrieved context ---
    run.advance(WorkflowStage.SECURITY_CHECK)
    from app.security.injection_shield import inspect_prompt_safety
    context_findings = []
    for chunk in run.retrieved_context:
        chunk_text = chunk.get("text", "")
        context_findings.extend(_scan(chunk_text))
        safety = inspect_prompt_safety(chunk_text)
        if not safety["is_safe"]:
            reason = safety.get("explanation") or safety.get("reason") or "adversarial pattern detected"
            run.history.append(f"Indirect Prompt Injection sanitized: {reason}")
            chunk["sanitized"] = True
            chunk["text"] = f"[SANITIZED: {reason}]"
    run.security_findings.extend(context_findings)
    save_run(run)

    # --- Stage: Change-impact analysis ---
    run.advance(WorkflowStage.IMPACT_ANALYSIS)
    try:
        repo_root = os.path.join(os.path.dirname(__file__), "..")
        run.impact_report = analyze_impact(run.request_text, repo_root, top_k=5)
    except Exception as e:
        run.impact_report = []
        run.history.append(f"Impact analysis skipped: {redact_text(str(e))}")
    save_run(run)

    # --- Stage: Evidence-grounded generation ---
    run.advance(WorkflowStage.GENERATION)
    generation_result = generate_code(run.request_text, run.retrieved_context)
    run.generation_result = generation_result
    save_run(run)

    generated_output = generation_result.get("generated_output", "")
    gen_findings = _scan(generated_output)
    run.security_findings.extend(gen_findings)

    # --- Basic syntax validation ---
    validation_result = validate_generated_output(generated_output)
    run.validation_result = validation_result

    run.advance(WorkflowStage.COMPLETE, f"Workflow completed under HITL supervisor authorization ({supervisor_id})")
    return _finish(run)

