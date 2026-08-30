"""
Kavach backend — FastAPI entrypoint.

Run locally with:
    pip install -r backend/requirements.txt
    uvicorn app.main:app --reload --app-dir backend

See docs/IMPLEMENTATION_STATUS.md for current build progress across phases.
"""

import os
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from fastapi import FastAPI
from pydantic import BaseModel

from app.rag.ingest import ingest_repository
from app.rag.embed_store import index_chunks, search
from app.security.detector import detect_pii
from app.security.evaluator import evaluate
from app.agent.orchestrator import run_workflow
from app.agent.state import get_run, list_runs
from app.impact.analyzer import analyze_impact
from app.impact.evaluator import evaluate as evaluate_impact

app = FastAPI(
    title="Kavach",
    description="Multilingual Security-Governed Agentic AI DevOps Platform — backend API",
    version="0.0.1",
)


@app.get("/health")
def health_check():
    """Basic liveness check — confirms the service is running."""
    return {"status": "ok", "service": "kavach-backend"}


# --- Kavach security detection (see docs/SECURITY_SPEC.md, docs/PII_PATTERNS.md) ---

class DetectRequest(BaseModel):
    text: str


@app.post("/detect")
def detect(payload: DetectRequest):
    """
    Proof-of-concept PII detector. Scans the input text for PAN-like,
    phone-like, and email patterns and reports what it found.
    """
    findings = detect_pii(payload.text)
    return {
        "input": payload.text,
        "findings": findings,
        "allowed": len(findings) == 0,
    }


# --- Phase 1: Repository ingestion + RAG (see docs/RAG_SPEC.md) ---

class IngestRequest(BaseModel):
    repo_path: str  # absolute or relative path to the repo to index


@app.post("/ingest")
def ingest(payload: IngestRequest):
    """
    Walk the given repository path, chunk its files, embed them, and store
    them in the local Qdrant index. Run this once (or after significant
    repo changes) before using /search or /agent/request.
    """
    chunks = ingest_repository(payload.repo_path)
    indexed_count = index_chunks(chunks)
    return {
        "repo_path": payload.repo_path,
        "files_chunks_found": len(chunks),
        "chunks_indexed": indexed_count,
    }


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@app.post("/search")
def search_repository(payload: SearchRequest):
    """
    Given a natural-language or code-like query, return the most relevant
    indexed repository chunks.
    """
    results = search(payload.query, top_k=payload.top_k)
    return {"query": payload.query, "results": results}


# --- Phase 2: Agent Orchestrator (see docs/AGENT_SPEC.md) ---

class AgentRequest(BaseModel):
    request_text: str


@app.post("/agent/request")
def submit_agent_request(payload: AgentRequest):
    """
    Submit a natural-language developer request to the Kavach-governed
    agent workflow. Runs it through: security check on input -> planning ->
    RAG context retrieval -> security check on retrieved context.

    Later phases (code generation, test generation, build/test, CI/CD,
    change-impact analysis) will extend this same workflow as they're built —
    see docs/AGENT_SPEC.md for the full intended state machine.
    """
    run = run_workflow(payload.request_text)
    return {
        "workflow_id": run.id,
        "final_stage": run.stage,
        "plan": run.plan,
        "retrieved_context": run.retrieved_context,
        "security_findings": run.security_findings,
        "generation_result": run.generation_result,
        "validation_result": run.validation_result,
        "impact_report": run.impact_report,
        "history": run.history,
    }


@app.get("/agent/runs/{run_id}")
def get_agent_run(run_id: str):
    """Look up a specific workflow run by id."""
    run = get_run(run_id)
    if run is None:
        return {"error": f"No workflow run found with id {run_id}"}
    return {
        "workflow_id": run.id,
        "request_text": run.request_text,
        "final_stage": run.stage,
        "plan": run.plan,
        "retrieved_context": run.retrieved_context,
        "security_findings": run.security_findings,
        "generation_result": run.generation_result,
        "validation_result": run.validation_result,
        "impact_report": run.impact_report,
        "history": run.history,
    }


@app.get("/agent/runs")
def get_all_agent_runs():
    """List all workflow runs (in-memory — resets on server restart for now)."""
    runs = list_runs()
    return {"count": len(runs), "runs": [{"id": r.id, "stage": r.stage, "request": r.request_text} for r in runs]}


@app.get("/evaluate")
def evaluate_security_engine():
    """
    Run the multilingual test corpus through the security engine and return
    precision/recall/F1 — overall and per language. See docs/EVALUATION_PLAN.md.
    """
    return evaluate()


# --- Phase 5: Change-Impact Analysis (see docs/IMPACT_ANALYSIS_SPEC.md) ---

class ImpactAnalyzeRequest(BaseModel):
    change_description: str
    repo_path: str = "app"  # relative to backend/, defaults to the backend/app source tree


@app.post("/impact/analyze")
def analyze_change_impact(payload: ImpactAnalyzeRequest):
    """
    Given a natural-language description of a proposed change, return a
    ranked list of files likely to be affected — combining semantic
    similarity (RAG) with explicit import/dependency relationships.
    Standalone endpoint for testing the analyzer independent of the full
    agent workflow (which also runs this internally — see /agent/request).
    """
    import os
    repo_root = os.path.join(os.path.dirname(__file__), "..", payload.repo_path)
    report = analyze_impact(payload.change_description, repo_root)
    return {"change_description": payload.change_description, "impact_report": report}


@app.get("/impact/evaluate")
def evaluate_impact_analyzer():
    """
    Run known change-description test cases through the impact analyzer and
    compare predicted vs. actual affected files, returning precision/
    recall/F1 — overall and per case. See docs/EVALUATION_PLAN.md,
    Research Question 3.
    """
    return evaluate_impact()


@app.get("/")
def root():
    return {
        "message": "Kavach backend is running.",
        "docs": "/docs",
        "status_file": "See docs/IMPLEMENTATION_STATUS.md for current build progress.",
    }
