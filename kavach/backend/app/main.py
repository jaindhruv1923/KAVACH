"""
Kavach backend — FastAPI entrypoint.

Run locally with:
    pip install -r backend/requirements.txt
    uvicorn app.main:app --reload --app-dir backend

See docs/IMPLEMENTATION_STATUS.md for current build progress across phases.
"""

import json
import os
import re
import urllib.error
import urllib.request

from dotenv import load_dotenv

print("Loading env...")
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
print("Env loaded.")

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.rag.ingest import chunk_text, ingest_repository
from app.rag.embed_store import index_chunks, search
from app.security.detector import detect_pii
from app.security.secret_detector import detect_secrets
from app.security.policy_engine import evaluate_policy
from app.security.evaluator import evaluate
from app.agent.orchestrator import run_workflow
from app.agent.state import get_run, list_runs
from app.impact.analyzer import analyze_impact
from app.impact.evaluator import evaluate as evaluate_impact
from app.security.evaluator_v2 import evaluate_v2
from app.generation.llm_client import is_llm_configured


# ============================================================
# FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="Kavach",
    description="Security-Governed Agentic AI DevOps Platform — backend API",
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
# kavach/backend/app/main.py
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


@app.get("/config/status")
def configuration_status():
    """Expose safe configuration metadata without returning secrets."""
    return {
        "gemini_configured": is_llm_configured(),
        "gemini_model": os.environ.get("GEMINI_MODEL", "gemini-3.5-flash"),
        "env_file": os.path.join(PROJECT_ROOT, "backend", ".env"),
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


class CodeReviewRequest(BaseModel):
    code: str
    filename: str = "pasted-code.txt"


@app.post("/review")
def review_code(payload: CodeReviewRequest):
    """Review pasted code through the shared PII, secret, and policy engines."""
    findings = detect_pii(payload.code) + detect_secrets(payload.code)
    policy = evaluate_policy(f"Review {payload.filename}", findings)
    categories = {finding.get("category") for finding in findings}
    recommendations = []
    if "credential" in categories:
        recommendations.append("Remove the credential, rotate it immediately, and load it from backend/.env.")
    if categories.intersection({"PAN", "Aadhaar-like", "bank_account", "phone_number", "email"}):
        recommendations.append("Redact sensitive personal data and avoid committing it to source control.")
    if not recommendations:
        recommendations.append("No sensitive-data or credential pattern was detected by the configured rules.")
    return {
        "filename": payload.filename,
        "finding_count": len(findings),
        "findings": findings,
        "policy_decision": policy,
        "recommendations": recommendations,
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


class GithubIngestRequest(BaseModel):
    repository_url: str
    max_files: int = 30


@app.post("/github/ingest")
def ingest_github_repository(payload: GithubIngestRequest):
    """Index a public GitHub repository without requiring a local clone."""
    match = re.fullmatch(r"https?://github\.com/([^/]+)/([^/#]+?)(?:\.git)?/?", payload.repository_url.strip())
    if not match:
        raise ValueError("Use a public GitHub URL such as https://github.com/owner/repository")
    owner, repository = match.groups()
    api_url = f"https://api.github.com/repos/{owner}/{repository}/git/trees/HEAD?recursive=1"
    request = urllib.request.Request(api_url, headers={"User-Agent": "Kavach-Security-Workspace"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            tree = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        raise ValueError(f"GitHub returned HTTP {error.code}; check that the repository is public.") from error
    except urllib.error.URLError as error:
        raise ValueError(f"Could not reach GitHub: {error.reason}") from error

    extensions = {".py", ".js", ".ts", ".jsx", ".tsx", ".md", ".json", ".yaml", ".yml", ".sql", ".html", ".css"}
    files = [item["path"] for item in tree.get("tree", [])
             if item.get("type") == "blob" and os.path.splitext(item["path"])[1].lower() in extensions]
    files = files[:max(1, min(payload.max_files, 100))]
    chunks = []
    findings = []
    for file_path in files:
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repository}/HEAD/{file_path}"
        try:
            raw_request = urllib.request.Request(raw_url, headers={"User-Agent": "Kavach-Security-Workspace"})
            with urllib.request.urlopen(raw_request, timeout=15) as response:
                text = response.read(250_000).decode("utf-8", errors="ignore")
        except (urllib.error.HTTPError, urllib.error.URLError):
            continue
        chunks.extend(chunk_text(text, file_path))
        findings.extend(detect_pii(text))
        findings.extend(detect_secrets(text))

    indexed_count = index_chunks(chunks)
    return {
        "repository": f"{owner}/{repository}",
        "files_scanned": len(files),
        "chunks_indexed": indexed_count,
        "findings": findings[:50],
        "finding_count": len(findings),
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
        "policy_decision": run.policy_decision,
        "redacted_request_text": run.redacted_request_text,
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
        "policy_decision": run.policy_decision,
        "redacted_request_text": run.redacted_request_text,
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
    Run the test corpus through the security
    engine and return precision/recall/F1.
    """
    return evaluate()


@app.get("/agent/runs/{run_id}/explain")
def explain_decision(run_id: str):
    """
    Plain-English explanation of why a workflow run was allowed, blocked,
    or sent for review — for a non-technical reader (e.g. a demo audience
    or a developer who just wants to know what to fix). Built on top of
    the existing policy_decision data, not a new decision source.
    """
    run = get_run(run_id)
    if run is None:
        return {"error": f"No workflow run found with id {run_id}"}

    policy = run.policy_decision
    stage = run.stage

    if not policy:
        return {
            "workflow_id": run_id,
            "plain_english": "This request completed without triggering any security policy check that stopped it.",
        }

    decision = policy.get("decision", "ALLOW")
    risk_score = policy.get("risk_score", 0.0)
    action_risk = policy.get("action_risk_classification", "low")
    categories = sorted(set(f.get("category", "unknown") for f in run.security_findings)) if run.security_findings else []
    cat_text = ", ".join(categories) if categories else "no specific sensitive-data category"

    if decision == "BLOCK":
        plain = (
            f"This request was blocked. Kavach detected {cat_text} in the request or its "
            f"repository context, and the action you asked for was classified as "
            f"'{action_risk}' risk. Combined, this produced a risk score of {risk_score} "
            f"(out of 1.0), which is above the threshold for blocking outright."
        )
    elif decision == "REVIEW":
        plain = (
            f"This request needs human review before it can proceed. Kavach found {cat_text}, "
            f"but the combined risk score ({risk_score}) wasn't high enough to block automatically "
            f"— it's ambiguous enough that a human should look at it."
        )
    elif decision == "REDACT":
        plain = (
            f"This request was allowed to continue, but {cat_text} was found and should be "
            f"redacted from any output or logs before being shown or stored."
        )
    else:
        plain = "This request was allowed — no significant sensitive-data or high-risk-action signal was detected."

    return {
        "workflow_id": run_id,
        "final_stage": stage,
        "decision": decision,
        "plain_english": plain,
        "technical_detail": policy,
    }


@app.get("/evaluate/v2")
def evaluate_security_engine_v2():
    """Part 2 evaluation: secret/credential detection + hard-negative cases + action-risk classification accuracy. See KAVACH_LIMITATIONS.md."""
    return evaluate_v2()


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

