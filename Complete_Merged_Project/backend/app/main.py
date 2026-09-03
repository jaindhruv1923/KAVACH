"""
Kavach backend — FastAPI entrypoint.

Run locally with:
    pip install -r backend/requirements.txt
    uvicorn app.main:app --reload --app-dir backend

See docs/IMPLEMENTATION_STATUS.md for current build progress across phases.
"""

import os

from dotenv import load_dotenv

print("Loading env...")
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
print("Env loaded.")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.rag.ingest import ingest_repository
from app.rag.embed_store import index_chunks, search
from app.security.detector import detect_pii
from app.security.evaluator import evaluate
from app.agent.orchestrator import run_workflow
from app.agent.state import get_run, list_runs
from app.impact.analyzer import analyze_impact
from app.impact.evaluator import evaluate as evaluate_impact


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Kavach",
    description="Multilingual Security-Governed Agentic AI DevOps Platform — backend API",
    version="0.0.1",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# STATIC FRONTEND
# ============================================================

# Resolve the frontend directory from this file's actual location.
# main.py is inside:
# Complete_Merged_Project/backend/app/main.py
#
# Therefore:
# __file__ -> app
# ..      -> backend
# ..      -> Complete_Merged_Project
# frontend -> Complete_Merged_Project/frontend

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")


def resolve_repository_path(repo_path: str) -> str:
    """Resolve repository paths relative to the integrated project root."""
    path = os.path.expanduser(repo_path)
    if not os.path.isabs(path):
        project_path = os.path.join(PROJECT_ROOT, path)
        backend_path = os.path.join(PROJECT_ROOT, "backend", path)
        path = project_path if os.path.exists(project_path) else backend_path
    return os.path.abspath(path)

app.mount(
    "/static",
    StaticFiles(directory=FRONTEND_DIR),
    name="static",
)


@app.get("/", include_in_schema=False)
def frontend_root():
    """Serve the frontend entrypoint for browser users."""
    return RedirectResponse(url="/static/index.html", status_code=307)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():
    """Basic liveness check — confirms the service is running."""
    return {
        "status": "ok",
        "service": "kavach-backend",
    }


# ============================================================
# SECURITY DETECTION
# ============================================================

class DetectRequest(BaseModel):
    text: str


@app.post("/detect")
def detect(payload: DetectRequest):
    """
    Proof-of-concept PII detector.

    Scans the input text for PAN-like, phone-like,
    and email patterns and reports what it found.
    """
    findings = detect_pii(payload.text)

    return {
        "input": payload.text,
        "findings": findings,
        "allowed": len(findings) == 0,
    }


# ============================================================
# PHASE 1 — REPOSITORY INGESTION + RAG
# ============================================================

class IngestRequest(BaseModel):
    repo_path: str


@app.post("/ingest")
def ingest(payload: IngestRequest):
    """
    Walk the given repository path, chunk its files, embed them,
    and store them in the local Qdrant index.
    """
    repository_path = resolve_repository_path(payload.repo_path)
    chunks = ingest_repository(repository_path)
    indexed_count = index_chunks(chunks)

    return {
        "repo_path": repository_path,
        "files_chunks_found": len(chunks),
        "chunks_indexed": indexed_count,
    }


class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


@app.post("/search")
def search_repository(payload: SearchRequest):
    """
    Given a natural-language or code-like query, return the
    most relevant indexed repository chunks.
    """
    results = search(
        payload.query,
        top_k=payload.top_k,
    )

    return {
        "query": payload.query,
        "results": results,
    }


# ============================================================
# PHASE 2 — AGENT ORCHESTRATOR
# ============================================================

class AgentRequest(BaseModel):
    request_text: str


@app.post("/agent/request")
def submit_agent_request(payload: AgentRequest):
    """
    Submit a natural-language developer request to the
    Kavach-governed agent workflow.
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
        return {
            "error": f"No workflow run found with id {run_id}"
        }

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
    """List all workflow runs."""

    runs = list_runs()

    return {
        "count": len(runs),
        "runs": [
            {
                "id": r.id,
                "stage": r.stage,
                "request": r.request_text,
            }
            for r in runs
        ],
    }


# ============================================================
# SECURITY ENGINE EVALUATION
# ============================================================

@app.get("/evaluate")
def evaluate_security_engine():
    """
    Run the multilingual test corpus through the security
    engine and return precision/recall/F1.
    """
    return evaluate()


# ============================================================
# PHASE 5 — CHANGE IMPACT ANALYSIS
# ============================================================

class ImpactAnalyzeRequest(BaseModel):
    change_description: str
    repo_path: str = "app"


@app.post("/impact/analyze")
def analyze_change_impact(payload: ImpactAnalyzeRequest):
    """
    Given a natural-language description of a proposed change,
    return a ranked list of files likely to be affected.
    """

    repo_root = resolve_repository_path(payload.repo_path)

    report = analyze_impact(
        payload.change_description,
        repo_root,
    )

    return {
        "change_description": payload.change_description,
        "impact_report": report,
    }


@app.get("/impact/evaluate")
def evaluate_impact_analyzer():
    """
    Run known change-description test cases through the
    impact analyzer and compare predicted vs actual affected files.
    """
    return evaluate_impact()

