# KAVACH: Post-Audit Engineering Progress Report

**Project Title:** KAVACH — Security-Governed Agentic AI DevOps Platform  
**Academic Course:** CSE3101 — Agentic AI (Academic Year 2026–2027)  
**Report Type:** Post-Verification Audit Progress & Corrections Report (1–2 Pages)  
**Evaluation Standard:** Measured reality via automated test suites and `docs/METRICS.json`  

---

## 1. Executive Summary & What Was Built

KAVACH is an enterprise-grade agentic AI DevOps governance and cyber-defense platform designed to enforce deterministic security gates across the autonomous software engineering lifecycle. Over the 16-week execution timeline, KAVACH evolved into an integrated multi-tier system:

1. **Pre-Execution Security Firewall:** Zero-latency Shannon entropy scanner (`app/security/secret_detector.py`) and context-aware regex detectors (`app/security/detector.py`) intercepting Indian national identifiers (Aadhaar, PAN), financial cards, API keys, and private credentials.
2. **Context-Aware Code RAG:** Abstract Syntax Tree (AST) code chunker (`app/rag/ingest.py`) coupled with local Qdrant vector retrieval (`all-MiniLM-L6-v2`) to provide security-grounded repository context.
3. **Multi-Agent Orchestration & Self-Healing:** Finite-state machine orchestrator with 6 active lifecycle stages (`REQUEST_RECEIVED`, `PLANNING`, `CONTEXT_RETRIEVAL`, `SECURITY_CHECK`, `IMPACT_ANALYSIS`, `GENERATION`), AST blast radius analysis, and an ephemeral pytest-driven reflection repair loop.
4. **Supply Chain & Extensibility:** Slopsquatting defense (`app/security/package_verifier.py`) against hallucinated packages, JSON-RPC 2.0 Model Context Protocol (MCP) server (`app/mcp/server.py`), and a unified Mission Control dashboard integrating a 15-endpoint Bharat Bank core banking simulation.

---

## 2. What Changed During the Corrections Stage

Following the comprehensive verification audit, the repository underwent systematic alignment to ensure absolute fidelity between code reality and documentation:

- **Single Source of Truth (SSOT):** Implemented `scripts/generate_metrics.py`, which programmatically executes test suites, benchmark evaluators, red-team attacks, and latency timers, outputting machine-verifiable `docs/METRICS.json` and `docs/METRICS.md`.
- **Elimination of Superlatives & Unverified Scores:** Removed subjective claims (such as "Evaluation Score 9.6/10", "production-quality", and "100% interceptor guarantees").
- **Framework Transparency:** Relabeled custom orchestrator implementations (`app/crew/` and `app/adk/`) as native "CrewAI-pattern" and "ADK-pattern" architectures rather than external pip dependencies, preventing dependency falsification.
- **Link & Path Correction:** Repaired 106 broken asset links, corrected repository clone URLs to `https://github.com/jaindhruv1923/KAVACH.git`, and unified test count reporting across all markdown documents.
- **API Error Handling Fix:** Added a global `ValueError` exception handler in `01_KAVACH_Platform/backend/app/main.py` mapping unhandled validation errors to clean HTTP 400 Bad Request responses.

---

## 3. Measured Results & Empirical Data

All metrics originate from automated execution on Windows 11 (AMD64, 20 CPU cores, 15.75 GB RAM, Python 3.14.7):

| Evaluation Dimension | Benchmark Dataset & Description | Measured Outcome | Author Caveat & Statistical Context |
| :--- | :--- | :---: | :--- |
| **Deterministic Verification Tests** | 300 deterministic pytest assertions (100 KAVACH, 100 Bharat Bank, 100 Unified) | **300 / 300 Passed (100.0%)** | Fully passing in 13.72s. Zero flaky assertions. |
| **Full Repository Test Suite** | 641 total test assertions across unit, integration, and security modules | **641 / 641 Passed (100.0%)** | 100% passing across all 16 test files. |
| **Registered API Endpoints** | FastAPI route tables across KAVACH core, Bharat Bank (`/bank`), and Cockpit (`/results`) | **142 Total (120 Core + 22 Mounted)** | 120 core KAVACH routes, 15 bank routes, 7 results routes. |
| **Detector Evaluator ($V_1$ Baseline)** | 50 curated cases (30 sensitive, 20 non-sensitive) in `data/eval_dataset.json` | **P: 1.000 \| R: 1.000 \| F1: 1.000** | Synthesized authored dataset; risk of overfitting on known patterns. |
| **Fresh Held-Out Evaluation ($V_2$)** | 45 newly generated cases (25 sensitive, 20 benign prompts with distractors) | **P: 0.8929 \| R: 1.000 \| F1: 0.9434** | Freshly authored held-out set. Identified 3 false positives on 10-digit SKUs/order codes. |
| **Red-Team Attack Simulator** | 19 simulated attack vectors across MITRE ATLAS and OWASP LLM Top 10 | **19 / 19 Intercepted (100.0%)** | Evaluated against authored heuristic test harness. |
| **PII & Secret Detector Latency** | 30 benchmark runs measuring median and 95th percentile execution | **Median: 0.02 ms \| p95: 0.05 ms** | Sub-millisecond pre-execution regex & Shannon entropy checks. |
| **End-to-End Workflow Latency** | 30 benchmark runs through multi-agent planning and AST analysis | **Median: 608.44 ms \| p95: 692.62 ms** | End-to-end multi-agent lifecycle execution under 700 ms. |

---

## 4. Known Limitations (Audit Findings)

1. **Context-Insensitive 10-Digit Numeric Matching:** The mobile phone regex in `app/security/detector.py` flags any isolated 10-digit number. While achieving 100% recall on phone numbers, it produced 3 false positives on alphanumeric catalog order IDs (`BLK-9876543210`) in held-out set $V_2$.
2. **Synchronous AST Dependency Ingestion:** AST parsing traverses local Python files synchronously. While fast (~350 ms for small repos), monolithic codebases (>50,000 LOC) require asynchronous task queues to avoid blocking FastAPI event loops.
3. **In-Repo Architecture Pattern vs. PyPI Libraries:** The multi-agent implementation deliberately uses clean native Python classes mimicking Google ADK and CrewAI rather than pulling heavy external distributions.
4. **Local Vector Storage Locking on Windows:** Concurrent writes to on-disk Qdrant storage can trigger Windows file-lock contention; mitigated by configuring `:memory:` storage during parallel test runs.

---

## 5. Next Steps

- **Disambiguation Heuristics:** Implement negative lookbehind patterns or entity prefix whitelists (`ORDER-`, `SKU-`) to eliminate false positives on 10-digit product codes.
- **Enterprise Storage Migration:** Migrate from JSON file persistence (`workflow_runs.json`) to PostgreSQL with Alembic migrations for concurrent production deployments.
- **Async AST Worker Architecture:** Offload deep AST call-graph traversals to background Celery or Redis streams.
- **Containerized Sandbox Isolation:** Transition from ephemeral subprocess test execution to gVisor or Firecracker microVM sandboxing for untrusted LLM-generated code execution.
