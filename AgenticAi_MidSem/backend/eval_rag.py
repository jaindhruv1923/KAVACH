import os
import sys
import json
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

def run_evaluation():
    repo_path = str(Path(__file__).resolve().parent.parent / "demo_repo")
    
    chunks = ingest_repository(repo_path)
    index_chunks(chunks)

    queries = [
        {"query": "Authenticate user credentials with password hash verification", "ground_truth": ["auth.py"]},
        {"query": "Database connection and session record lookup", "ground_truth": ["database.py"]},
        {"query": "API routes and endpoints for user management", "ground_truth": ["api.py"]},
        {"query": "Password length validation and SHA-256 storage", "ground_truth": ["auth.py"]},
        {"query": "Kavach architecture and demonstration walkthrough", "ground_truth": ["DEMO.md"]}
    ]
    
    results = []
    latencies = []
    
    for _ in range(3):
        search("Kavach security", top_k=5)
        
    for q in queries:
        start_time = time.perf_counter()
        retrieved = search(q["query"], top_k=5)
        end_time = time.perf_counter()
        
        latency_ms = (end_time - start_time) * 1000
        latencies.append(latency_ms)
        
        def _clean_path(p: str) -> str:
            p = p.replace("\\", "/").lower()
            if "app/" in p:
                p = p.split("app/", 1)[1]
            return p.lstrip("./")

        retrieved_paths = [_clean_path(r["file_path"]) for r in retrieved]
        ground_truth_normalized = [_clean_path(gt) for gt in q["ground_truth"]]

        hit = 1 if any(any(gt in rp or rp in gt for gt in ground_truth_normalized) for rp in retrieved_paths) else 0
        found_gt_count = sum(1 for gt in ground_truth_normalized if any(gt in rp or rp in gt for rp in retrieved_paths))
        recall = found_gt_count / len(ground_truth_normalized)
        
        results.append({
            "query": q["query"],
            "ground_truth": q["ground_truth"],
            "retrieved_top_5": retrieved_paths,
            "hit": hit,
            "recall": recall,
            "latency_ms": latency_ms
        })
        
    total_hits = sum(r["hit"] for r in results)
    avg_recall = sum(r["recall"] for r in results) / len(results)
    
    avg_latency = sum(latencies) / len(latencies)
    sorted_latencies = sorted(latencies)
    median_latency = sorted_latencies[len(sorted_latencies)//2]
    p95_latency = sorted_latencies[int(len(sorted_latencies)*0.95)] if len(sorted_latencies) > 1 else sorted_latencies[0]
    
    eval_data = {
        "benchmark_metadata": {
            "execution_command": "python eval_rag.py",
            "executed_at": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
            "environment": "Local Qdrant In-Memory Vector Store + all-MiniLM-L6-v2 Embeddings",
            "corpus": "01_KAVACH_Platform/demo_repo",
            "total_queries_evaluated": len(results)
        },
        "hit_at_5": total_hits / len(results),
        "mean_recall_at_5": avg_recall,
        "avg_latency_ms": round(avg_latency, 2),
        "median_latency_ms": round(median_latency, 2),
        "p95_latency_ms": round(p95_latency, 2),
        "results": results
    }

    results_dir = Path(__file__).resolve().parent
    with open(results_dir / "eval_results.json", "w", encoding="utf-8") as f:
        json.dump(eval_data, f, indent=2)

    import csv
    with open(results_dir / "eval_results.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Query_ID", "Evaluated_Query", "Ground_Truth", "Retrieved_Top_1", "Hit_At_5", "Recall_At_5", "Latency_ms", "Executed_Command", "Executed_At"])
        for idx, r in enumerate(results, start=1):
            top1 = r["retrieved_top_5"][0] if r["retrieved_top_5"] else "NONE"
            writer.writerow([
                f"RAG-EVAL-{idx:02d}",
                r["query"],
                ";".join(r["ground_truth"]),
                top1,
                r["hit"],
                round(r["recall"], 2),
                round(r["latency_ms"], 2),
                "python eval_rag.py",
                eval_data["benchmark_metadata"]["executed_at"]
            ])

if __name__ == "__main__":
    run_evaluation()

