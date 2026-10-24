"""
RAG Retrieval Evaluation Suite for KAVACH.

Modes:
  1. Full Evaluation (Default):
     - Corpus: KAVACH backend source code (app/) containing 600+ indexed chunks.
     - Sample Size (n): 32 diverse software engineering queries.
     - Ground Truth: Pre-defined file targets established prior to retrieval execution.
     - Metrics: Hit@1, Hit@3, Hit@5, Recall@5, Mean Reciprocal Rank (MRR), and latency profile (Mean, Median, P95).
     - Metadata: Execution command, UTC timestamp, git commit hash, and corpus size.
  2. Smoke Test (--smoke):
     - Labeled explicitly as 'retrieval smoke test (5 queries, 3-file demo repo)'.
"""

import argparse
import csv
import json
import os
import subprocess
import sys
import time
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

try:
    from app.rag.ingest import ingest_repository, Chunk
    from app.rag.embed_store import index_chunks, search
except ImportError as e:
    print(f"Import error: {e}")
    sys.exit(1)


# 32 Ground-Truth Evaluation Queries established prior to running retrieval
EVALUATION_QUERIES_32 = [
    {"id": 1, "query": "FastAPI HTTP server routes, middleware configuration, and application entrypoint", "ground_truth": ["main.py"]},
    {"id": 2, "query": "Detection of Indian personal data PII such as PAN card, Aadhaar number, phone, email", "ground_truth": ["security/detector.py"]},
    {"id": 3, "query": "Regex patterns and compiled regex signatures for sensitive data detection", "ground_truth": ["security/patterns.py"]},
    {"id": 4, "query": "Scanning source code for exposed AWS credentials, GitHub tokens, and private keys", "ground_truth": ["security/secret_detector.py"]},
    {"id": 5, "query": "Risk-adaptive policy engine evaluating BLOCK, REVIEW, and ALLOW policy actions", "ground_truth": ["security/policy_engine.py"]},
    {"id": 6, "query": "Redacting sensitive PII entities and credentials before writing to audit trail", "ground_truth": ["security/audit_redaction.py"]},
    {"id": 7, "query": "Cryptographic SHA-256 Merkle tree tamper-evident immutable audit ledger", "ground_truth": ["security/merkle_ledger.py"]},
    {"id": 8, "query": "Indirect prompt injection shield and adversarial jailbreak pattern sanitization", "ground_truth": ["security/injection_shield.py"]},
    {"id": 9, "query": "Software Bill of Materials SBOM generation in CycloneDX and SPDX format", "ground_truth": ["security/sbom_generator.py"]},
    {"id": 10, "query": "Constructing python abstract syntax tree AST dependency graphs across imports", "ground_truth": ["impact/dependency_graph.py"]},
    {"id": 11, "query": "Analyzing blast radius and change impact combining semantic search with dependency graph", "ground_truth": ["impact/analyzer.py"]},
    {"id": 12, "query": "Multi-stage agent orchestrator workflow executing security, RAG, generation, and impact", "ground_truth": ["agent/orchestrator.py"]},
    {"id": 13, "query": "Task decomposition breaking natural language developer requests into structured sub-tasks", "ground_truth": ["agent/planner.py"]},
    {"id": 14, "query": "Workflow run state machine managing transitions and JSON file persistence", "ground_truth": ["agent/state.py"]},
    {"id": 15, "query": "Evidence-grounded code generation prompting Google Gemini with retrieved repository context", "ground_truth": ["generation/generator.py"]},
    {"id": 16, "query": "Google Gemini REST client and local Ollama air-gapped inference fallback", "ground_truth": ["generation/llm_client.py"]},
    {"id": 17, "query": "Validating generated python output for AST syntax correctness and safety", "ground_truth": ["generation/validator.py"]},
    {"id": 18, "query": "Repository file ingestion, markdown chunking, and code parser extraction", "ground_truth": ["rag/ingest.py"]},
    {"id": 19, "query": "Qdrant vector store client setup, collection creation, and cosine similarity search", "ground_truth": ["rag/embed_store.py"]},
    {"id": 20, "query": "Google ADK LlmAgent lifecycle states INITIALIZED, PLANNING, EXECUTING, REFLECTING", "ground_truth": ["adk/agent.py"]},
    {"id": 21, "query": "Google ADK 8-hook callbacks event bus before_agent, after_model, before_tool", "ground_truth": ["adk/callbacks.py"]},
    {"id": 22, "query": "Google ADK medical triage academic course exercise with urgency classifier and branching", "ground_truth": ["adk/medical_triage.py"]},
    {"id": 23, "query": "Google ADK coordinator executing multi-agent DAG workflow sequences", "ground_truth": ["adk/coordinator.py"]},
    {"id": 24, "query": "Google A2A agent-to-agent protocol message schema and signed task delegation envelopes", "ground_truth": ["a2a/protocol.py"]},
    {"id": 25, "query": "Cross-framework interoperability bridge translating between Google ADK and CrewAI", "ground_truth": ["a2a/interop_bridge.py"]},
    {"id": 26, "query": "CrewAI personas Sentinel, Retriever, BlastRadiusAnalyst, Coder, and Supervisor", "ground_truth": ["crew/agents.py"]},
    {"id": 27, "query": "CrewAI stateful flows using start and listen lifecycle decorators", "ground_truth": ["crew/flows.py"]},
    {"id": 28, "query": "Package firewall checking dependency vulnerabilities and typosquatting risks", "ground_truth": ["security/package_firewall.py"]},
    {"id": 29, "query": "Server-side request forgery SSRF protection blocking private IP ranges and cloud metadata", "ground_truth": ["security/ssrf_shield.py"]},
    {"id": 30, "query": "Role-based access control RBAC checking user roles and security clearance permissions", "ground_truth": ["security/rbac_engine.py"]},
    {"id": 31, "query": "Cryptographic token vault for PII tokenization and reversible AES encryption", "ground_truth": ["security/token_vault.py"]},
    {"id": 32, "query": "Human-in-the-loop HITL approval gating workflow for dangerous or high-risk actions", "ground_truth": ["agent/hitl_gate.py"]},
]

SMOKE_QUERIES_5 = [
    {"id": 1, "query": "Authenticate user credentials with password hash verification", "ground_truth": ["auth.py"]},
    {"id": 2, "query": "Database connection and session record lookup", "ground_truth": ["database.py"]},
    {"id": 3, "query": "API routes and endpoints for user management", "ground_truth": ["api.py"]},
    {"id": 4, "query": "Password length validation and SHA-256 storage", "ground_truth": ["auth.py"]},
    {"id": 5, "query": "Kavach architecture and demonstration walkthrough", "ground_truth": ["DEMO.md"]}
]


def _get_git_commit() -> str:
    try:
        out = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], stderr=subprocess.DEVNULL)
        return out.decode("utf-8").strip()
    except Exception:
        return "unknown"


def _clean_path(p: str) -> str:
    s = p.replace("\\", "/").lower()
    while "//" in s:
        s = s.replace("//", "/")
    if "/app/" in s:
        s = s.split("/app/", 1)[1]
    elif s.startswith("app/"):
        s = s[len("app/"):]
    return s.lstrip("./")


def run_benchmark(is_smoke: bool = False):
    git_commit = _get_git_commit()
    timestamp_utc = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())

    if is_smoke:
        corpus_path = str(Path(__file__).resolve().parent.parent / "demo_repo")
        benchmark_label = "retrieval smoke test (5 queries, 3-file demo repo)"
        queries = SMOKE_QUERIES_5
        json_filename = "smoke_results.json"
        csv_filename = "smoke_results.csv"
    else:
        corpus_path = str(Path(__file__).resolve().parent / "app")
        benchmark_label = "KAVACH Comprehensive RAG Retrieval Benchmark (32 queries over app/ source)"
        queries = EVALUATION_QUERIES_32
        json_filename = "eval_results.json"
        csv_filename = "eval_results.csv"

    print(f"[eval_rag] Indexing corpus from: {corpus_path}")
    chunks = ingest_repository(corpus_path)
    index_chunks(chunks)
    print(f"[eval_rag] Ingested and indexed {len(chunks)} chunks.")

    # Warmup search
    for _ in range(3):
        search("Kavach security governance", top_k=5)

    results = []
    latencies = []

    print(f"[eval_rag] Executing {len(queries)} evaluation queries...")
    for item in queries:
        q_text = item["query"]
        gt_raw = item["ground_truth"]
        gt_normalized = [_clean_path(g) for g in gt_raw]

        t0 = time.perf_counter()
        retrieved = search(q_text, top_k=5)
        t1 = time.perf_counter()
        latency_ms = (t1 - t0) * 1000
        latencies.append(latency_ms)

        retrieved_paths = [_clean_path(r.get("file_path", "")) for r in retrieved]

        # Calculate rank of first hit
        first_hit_rank = None
        for rank_idx, rp in enumerate(retrieved_paths, start=1):
            if any(gt in rp or rp in gt for gt in gt_normalized):
                first_hit_rank = rank_idx
                break

        hit_at_1 = 1 if first_hit_rank == 1 else 0
        hit_at_3 = 1 if (first_hit_rank is not None and first_hit_rank <= 3) else 0
        hit_at_5 = 1 if (first_hit_rank is not None and first_hit_rank <= 5) else 0
        reciprocal_rank = (1.0 / first_hit_rank) if first_hit_rank else 0.0

        found_gt_count = sum(1 for gt in gt_normalized if any(gt in rp or rp in gt for rp in retrieved_paths))
        recall_at_5 = found_gt_count / len(gt_normalized)

        results.append({
            "query_id": item["id"],
            "query": q_text,
            "ground_truth": gt_raw,
            "retrieved_top_5": retrieved_paths,
            "first_hit_rank": first_hit_rank,
            "hit_at_1": hit_at_1,
            "hit_at_3": hit_at_3,
            "hit_at_5": hit_at_5,
            "reciprocal_rank": reciprocal_rank,
            "recall_at_5": recall_at_5,
            "latency_ms": round(latency_ms, 2)
        })

    n = len(results)
    hit_1_rate = sum(r["hit_at_1"] for r in results) / n
    hit_3_rate = sum(r["hit_at_3"] for r in results) / n
    hit_5_rate = sum(r["hit_at_5"] for r in results) / n
    mean_recall_5 = sum(r["recall_at_5"] for r in results) / n
    mrr = sum(r["reciprocal_rank"] for r in results) / n

    avg_latency = sum(latencies) / n
    sorted_lat = sorted(latencies)
    median_lat = sorted_lat[n // 2]
    min_lat = sorted_lat[0]
    max_lat = sorted_lat[-1]
    p95_lat = sorted_lat[int(n * 0.95)] if n > 1 else sorted_lat[0]

    output_payload = {
        "benchmark_metadata": {
            "benchmark_title": benchmark_label,
            "execution_command": f"python eval_rag.py{' --smoke' if is_smoke else ''}",
            "executed_at_utc": timestamp_utc,
            "git_commit": git_commit,
            "sample_size_n": n,
            "corpus_directory": corpus_path,
            "total_chunks_indexed": len(chunks),
            "embedding_model": "all-MiniLM-L6-v2",
            "vector_store": "Qdrant (In-Memory)",
        },
        "aggregate_metrics": {
            "hit_at_1": round(hit_1_rate, 4),
            "hit_at_3": round(hit_3_rate, 4),
            "hit_at_5": round(hit_5_rate, 4),
            "mean_recall_at_5": round(mean_recall_5, 4),
            "mean_reciprocal_rank_mrr": round(mrr, 4),
            "latency_ms": {
                "mean": round(avg_latency, 2),
                "median": round(median_lat, 2),
                "min": round(min_lat, 2),
                "max": round(max_lat, 2),
                "p95": round(p95_lat, 2)
            }
        },
        "query_details": results
    }

    out_json_path = BACKEND_DIR / json_filename
    with open(out_json_path, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2)

    out_csv_path = BACKEND_DIR / csv_filename
    with open(out_csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "Query_ID",
            "Query",
            "Ground_Truth",
            "Retrieved_Top_1",
            "First_Hit_Rank",
            "Hit_At_1",
            "Hit_At_3",
            "Hit_At_5",
            "MRR_Score",
            "Recall_At_5",
            "Latency_ms",
            "Command",
            "Date_UTC",
            "Git_Commit"
        ])
        for r in results:
            top_1 = r["retrieved_top_5"][0] if r["retrieved_top_5"] else "none"
            writer.writerow([
                r["query_id"],
                r["query"],
                ";".join(r["ground_truth"]),
                top_1,
                r["first_hit_rank"] if r["first_hit_rank"] is not None else 0,
                r["hit_at_1"],
                r["hit_at_3"],
                r["hit_at_5"],
                round(r["reciprocal_rank"], 4),
                round(r["recall_at_5"], 4),
                r["latency_ms"],
                f"python eval_rag.py{' --smoke' if is_smoke else ''}",
                timestamp_utc,
                git_commit
            ])

    print(f"\n=======================================================")
    print(f" {benchmark_label} ")
    print(f"=======================================================")
    print(f" Sample Size (n):      {n} queries")
    print(f" Chunks Indexed:       {len(chunks)}")
    print(f" Hit@1:                {hit_1_rate:.2%}")
    print(f" Hit@3:                {hit_3_rate:.2%}")
    print(f" Hit@5:                {hit_5_rate:.2%}")
    print(f" Mean Recall@5:        {mean_recall_5:.2%}")
    print(f" MRR:                  {mrr:.4f}")
    print(f" Mean Latency:         {avg_latency:.2f} ms")
    print(f" P95 Latency:          {p95_lat:.2f} ms")
    print(f" Git Commit:           {git_commit}")
    print(f" Exported JSON:        {out_json_path.name}")
    print(f" Exported CSV:         {out_csv_path.name}")
    print(f"=======================================================\n")
    return output_payload


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate KAVACH RAG vector retrieval performance.")
    parser.add_argument("--smoke", action="store_true", help="Run 5-query demo smoke test instead of full 32-query suite.")
    args = parser.parse_args()
    run_benchmark(is_smoke=args.smoke)
