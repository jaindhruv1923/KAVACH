# KAVACH: Comprehensive Viva Defense Code Map

**Project Title:** KAVACH — Security-Governed Agentic AI DevOps Platform  
**Target Audience:** Viva Examiners, Technical Evaluators, and Viva Defense Candidates  
**Source of Truth Baseline:** Git Commit `f81e625` / Single Source of Truth `docs/METRICS.json`  

---

## 1. Quick Navigation Matrix

| Viva Topic & Evaluation Category | Primary Code Location | Supporting Module | Deterministic Test File |
| :--- | :--- | :--- | :--- |
| **API Entrypoint & Exception Handling** | [01_KAVACH_Platform/backend/app/main.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/main.py#L50-L80) | [FastAPI Routers](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/main.py#L120-L500) | [test_api_endpoints.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/tests/test_api_endpoints.py) |
| **PII & National ID Detection** | [backend/app/security/detector.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/security/detector.py#L40-L130) | [evaluator_v2.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/security/evaluator_v2.py) | [test_security.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/tests/test_security.py) |
| **High-Entropy Secrets & Keys** | [backend/app/security/secret_detector.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/security/secret_detector.py#L38-L100) | [policy_engine.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/security/policy_engine.py) | [test_security_v2.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/tests/test_security_v2.py) |
| **AST Code RAG & Chunking** | [backend/app/rag/ingest.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/rag/ingest.py#L35-L95) | [embed_store.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/rag/embed_store.py#L40-L110) | [test_rag.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/tests/test_rag.py) |
| **Multi-Agent Orchestration & FSM** | [backend/app/agent/orchestrator.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/agent/orchestrator.py#L50-L160) | [state.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/agent/state.py#L25-L90) | [test_agent.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/tests/test_agent.py) |
| **CrewAI-Pattern Flow Engine** | [backend/app/crew/flows.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/crew/flows.py#L30-L90) | [orchestrator.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/crew/orchestrator.py) | [test_kavach_100_suite.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/tests/test_kavach_100_suite.py) |
| **Google ADK 8-Hook Callbacks** | [backend/app/adk/callbacks.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/adk/callbacks.py#L25-L95) | [coordinator.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/adk/coordinator.py) | [test_adk_callbacks_and_triage.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/tests/test_adk_callbacks_and_triage.py) |
| **AST Blast Radius Impact Engine** | [backend/app/impact/analyzer.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/impact/analyzer.py#L30-L115) | [evaluator.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/impact/evaluator.py) | [test_impact.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/tests/test_impact.py) |
| **Supply Chain Package Defense** | [backend/app/security/package_verifier.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/security/package_verifier.py#L35-L90) | [slopsquatting.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/security/slopsquatting.py) | [test_syllabus_advanced_modules.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/tests/test_syllabus_advanced_modules.py) |
| **Self-Healing Reflection Loop** | [backend/app/agent/self_healing.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/agent/self_healing.py#L25-L85) | [evaluator.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/agent/evaluator.py) | [test_kavach_100_suite.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/tests/test_kavach_100_suite.py) |
| **Model Context Protocol (MCP)** | [backend/app/mcp/server.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/mcp/server.py#L20-L80) | [JSON-RPC Handler](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/mcp/server.py#L85-L140) | [test_kavach_100_suite.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/tests/test_kavach_100_suite.py) |
| **Bharat Core Banking Services** | [02_Banking_and_Results_Dashboard/implementation_banks/server.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/02_Banking_and_Results_Dashboard/implementation_banks/server.py#L1-L240) | [core_banking.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/02_Banking_and_Results_Dashboard/implementation_banks/core_banking.py) | [test_banking_100_suite.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/02_Banking_and_Results_Dashboard/implementation_banks/test_banking_100_suite.py) |
| **Merkle Audit Ledger & Cryptography** | [backend/app/security/merkle_ledger.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/security/merkle_ledger.py#L20-L95) | [Audit Verifier](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/security/merkle_ledger.py#L100-L140) | [test_unified_100_suite.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/02_Banking_and_Results_Dashboard/tests_unified/test_unified_100_suite.py) |
| **Single Source of Truth Metrics** | [scripts/generate_metrics.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/scripts/generate_metrics.py#L1-L280) | [docs/METRICS.json](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/docs/METRICS.json) | `python scripts/generate_metrics.py` |

---

## 2. Key Code Implementations & Architecture

### A. API Error Handling (Post-Audit Fix)
- **Location:** [app/main.py:L74-L82](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/main.py#L74-L82)
- **Mechanism:** Global `@app.exception_handler(ValueError)` intercepts input validation errors across downstream domain services, preventing unhandled HTTP 500 errors and emitting structured HTTP 400 JSON payloads.
- **Verification:** Verified by `test_api_endpoints.py::TestErrorHandling::test_invalid_github_url_returns_400`.

### B. Dual-Regex and High-Entropy Scanning
- **Location:** [app/security/detector.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/security/detector.py) and [app/security/secret_detector.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/security/secret_detector.py)
- **Mechanism:** Dual-layer detection combining optimized regular expressions (Aadhaar `\b[2-9]\d{3}\s?\d{4}\s?\d{4}\b`, PAN `\b[A-Z]{5}[0-9]{4}[A-Z]\b`) with Shannon entropy analysis ($H = -\sum p_i \log_2 p_i \ge 4.5$).
- **Performance:** Measured median latency: 0.02 ms; p95 latency: 0.05 ms.

### C. Agentic Lifecycle State Machine
- **Location:** [app/agent/orchestrator.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/agent/orchestrator.py) and [app/agent/state.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/01_KAVACH_Platform/backend/app/agent/state.py)
- **Stages:** 6 active lifecycle phases:
  1. `REQUEST_RECEIVED`: Incoming task registration and UUID allocation.
  2. `PLANNING`: Sub-task decomposition.
  3. `CONTEXT_RETRIEVAL`: Dense AST chunk search against Qdrant.
  4. `SECURITY_CHECK`: Pre-execution PII, secret, and policy evaluation.
  5. `IMPACT_ANALYSIS`: Blast radius and transitive dependency calculations.
  6. `GENERATION`: LLM-guided patch synthesis with self-healing reflection.
- **Terminal States:** `COMPLETE`, `BLOCKED`, `NEEDS_REVIEW`.

### D. Single Source of Truth Automated Pipeline
- **Location:** [scripts/generate_metrics.py](file:///c:/Users/jaind/Desktop/project_work/KAVACH-main/scripts/generate_metrics.py)
- **Function:** Programmatically introspects system hardware via `ctypes`, enumerates FastAPI routes across all mounts, executes test suites, evaluates baseline $V_1$ (50 cases) and held-out $V_2$ (45 cases), runs 19 red-team attack vectors, and records 30-run median and p95 latency percentiles directly into `docs/METRICS.json` and `docs/METRICS.md`.

---

## 3. How to Answer Standard Examiner Questions

### Q1: *"Did you use external libraries like CrewAI or Google ADK?"*
> **Answer:** *"We implemented clean, native in-repo architectural models following the official specifications (`app/crew/` for CrewAI sequential/hierarchical flows, and `app/adk/` for Google ADK 8-hook callbacks). This intentional architectural choice ensures complete cross-platform stability on Python 3.14 without reliance on fragile external C-extensions, while maintaining exact structural compliance."*

### Q2: *"Why is the PII precision on V2 89.3% instead of 100%?"*
> **Answer:** *"In our post-audit corrections stage, we created a fresh 45-case held-out evaluation set (`data/held_out_eval_v2.json`) with challenging negative distractors. The mobile phone pattern flagged 3 numeric order IDs (such as `BLK-9876543210`) containing 10-digit substrings. Per our strict audit rules, rather than retroactively tuning the detector to artificially inflate numbers, we reported the honest measured reality: 100% recall (zero missed sensitive items) and 89.3% precision."*

### Q3: *"How do you prove these metrics are not hardcoded?"*
> **Answer:** *"All numbers are generated dynamically by executing `python scripts/generate_metrics.py`. The script inspects the running Python interpreter, counts FastAPI route registrations dynamically, executes the test runners, and writes the JSON output stamped with the exact git commit hash."*
