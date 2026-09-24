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

from app.agent.state import WorkflowRun, WorkflowStage, save_run
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


def _scan(text: str) -> list[dict]:
    """Run both PII and secret/credential detection over a piece of text."""
    return detect_pii(text) + detect_secrets(text)


def run_workflow(request_text: str) -> WorkflowRun:
    """
    Execute the currently-implemented portion of the Kavach workflow for a
    single developer request, and return the resulting WorkflowRun (with
    full stage history for transparency/debugging/demo purposes).
    """
    run = WorkflowRun(request_text=request_text)
    run.redacted_request_text = redact_text(request_text)
    save_run(run)

    # --- Stage: Kavach security + policy check on the raw input first ---
    # (Checking the input itself, before any planning/retrieval happens, is
    # deliberate — see docs/SECURITY_SPEC.md: "Where checks happen" includes
    # developer input as the first checkpoint.)
    input_findings = _scan(request_text)
    run.security_findings.extend(input_findings)

    input_policy = evaluate_policy(request_text, input_findings)
    run.policy_decision = input_policy

    if input_policy["decision"] == PolicyAction.BLOCK.value:
        run.advance(WorkflowStage.BLOCKED, input_policy["explanation"])
        save_run(run)
        return run

    # REVIEW is treated as a hard stop for now, same as BLOCK, until a human-
    # approval endpoint exists to resume a REVIEW-flagged run (see
    # KAVACH_LIMITATIONS.md — this is a known, honestly-scoped simplification).
    if input_policy["decision"] == PolicyAction.REVIEW.value:
        run.advance(WorkflowStage.NEEDS_REVIEW, input_policy["explanation"])
        save_run(run)
        return run

    # --- Stage: Planning ---
    run.advance(WorkflowStage.PLANNING)
    run.plan = plan_request(request_text)
    save_run(run)

    # --- Stage: Context retrieval (RAG) ---
    run.advance(WorkflowStage.CONTEXT_RETRIEVAL)
    try:
        run.retrieved_context = search(request_text, top_k=5)
    except Exception as e:
        # RAG index may not exist yet if /ingest hasn't been run — degrade
        # gracefully rather than crash the whole workflow.
        run.retrieved_context = []
        run.history.append(f"RAG retrieval skipped/failed: {redact_text(str(e))}")
    save_run(run)

    # --- Stage: Security check on retrieved context ---
    run.advance(WorkflowStage.SECURITY_CHECK)
    context_findings = []
    for chunk in run.retrieved_context:
        context_findings.extend(_scan(chunk.get("text", "")))
    run.security_findings.extend(context_findings)

    if context_findings:
        context_policy = evaluate_policy(request_text, context_findings)
        if context_policy["decision"] in (PolicyAction.BLOCK.value, PolicyAction.REVIEW.value):
            run.advance(WorkflowStage.NEEDS_REVIEW,
                        f"sensitive data found in retrieved context — {context_policy['explanation']}")
            save_run(run)
            return run

    # --- Stage: Change-impact analysis (Phase 5, Professor Idea #1 focused slice) ---
    run.advance(WorkflowStage.IMPACT_ANALYSIS)
    try:
        repo_root = os.path.join(os.path.dirname(__file__), "..")  # backend/app
        run.impact_report = analyze_impact(request_text, repo_root, top_k=5)
    except Exception as e:
        run.impact_report = []
        run.history.append(f"Impact analysis skipped/failed: {redact_text(str(e))}")
    save_run(run)

    # --- Stage: Evidence-grounded generation (Phase 3, Professor Idea #4) ---
    run.advance(WorkflowStage.GENERATION)
    generation_result = generate_code(request_text, run.retrieved_context)
    run.generation_result = generation_result
    save_run(run)

    generated_output = generation_result.get("generated_output", "")
    generation_failed = generated_output.startswith("[LLM call failed:")

    if generation_failed:
        # Don't hand an API error message to the syntax validator as if it
        # were code — report it as a generation failure instead.
        run.validation_result = {"valid_syntax": False, "error": "LLM generation failed — see generation_result", "extracted_code": None}
        run.advance(WorkflowStage.NEEDS_REVIEW, "LLM generation call failed — see generation_result for details")
        save_run(run)
        return run

    # --- Output security gate on generated code (Limitation #8: generated
    # output needs the same governance as the original request/context) ---
    generation_findings = _scan(generated_output)
    run.security_findings.extend(generation_findings)
    if generation_findings:
        output_policy = evaluate_policy(request_text, generation_findings)
        if output_policy["decision"] in (PolicyAction.BLOCK.value, PolicyAction.REVIEW.value):
            run.advance(WorkflowStage.BLOCKED,
                        f"sensitive data detected in generated output — {output_policy['explanation']}")
            save_run(run)
            return run

    # --- Basic syntax validation of the generated code ---
    validation_result = validate_generated_output(generation_result.get("generated_output", ""))
    run.validation_result = validation_result
    save_run(run)

    run.advance(WorkflowStage.COMPLETE, "workflow completed: planning + RAG + impact analysis + generation + security + validation")
    save_run(run)
    return run
