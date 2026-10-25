# REVISED PROJECT CHARTER & SYNOPSIS (POST-AUDIT)

**Academic Year:** 2026–27 | **Semester:** 7th Semester (B.Tech CSE)  
**Course Code & Name:** CSE3101 — Agentic AI  
**Course Faculty:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  
**Institution:** School of Engineering & Technology, BML Munjal University  
**Audit & Correction Stage:** Measured Reality Baseline (Commit `ad2277e` / Single Source of Truth: `docs/METRICS.json`)  

---

### Project Title
**KAVACH: A Security-Governed Multi-Agent AI DevOps & Observability Platform**

### 1. Problem Definition (Rubric C1 — Verified & Refined)
Modern autonomous software engineering agents (e.g., Devin, SWE-agent) automate code generation, dependency imports, and pull requests. However, deploying unconstrained agents in enterprise environments introduces critical vulnerabilities:
1. **Supply-Chain Slopsquatting & Hallucination:** Agents hallucinate non-existent package names, creating attack vectors for malicious package takeovers.
2. **Credential & PII Exfiltration:** Agents inadvertently leak proprietary API keys or national identifiers (PAN, Aadhaar) into prompts, code, or logs.
3. **Unbounded Blast Radius:** Agents modify shared code without structural dependency awareness, inducing downstream regressions.
4. **Stochastic Failures & Infinite Loops:** Autonomous code generators drift into ungrounded hallucination without deterministic verification gates.

---

### 2. Measurable Outcomes Table (Rubric C2 — Filled Directly from `METRICS.json`)

| Objective & Metric | Phase-1 Target | Measured Reality (`METRICS.json`) | Status | Evidence / Verification Test |
|---|---|---|---|---|
| **Deterministic Verification Tests** | $\ge 220$ passing tests | **300 / 300 passing** (100% pass rate) across 3 master suites (641 total repo tests) | **EXCEEDED** | `01_KAVACH_Platform/tests/test_kavach_100_suite.py`, `implementation_banks/test_banking_100_suite.py` |
| **High-Entropy Secrets & Key Detection** | 100% detection ($H > 4.5$) | **100% detection** across AWS keys, OpenAI/Gemini tokens, and passwords | **MET** | `01_KAVACH_Platform/tests/test_security_v2.py::test_secret_entropy` |
| **PII Detection Accuracy (V1 Corpus)** | F1 $\ge 0.95$ | **Precision: 100.0%, Recall: 100.0%, F1: 1.000** (50 author-curated cases) | **MET** | `01_KAVACH_Platform/backend/app/security/evaluator.py` |
| **PII Detection Accuracy (V2 Held-Out)** | Fresh evaluation | **Precision: 89.3%, Recall: 100.0%, F1: 0.943** (45 fresh cases, 3 FP edge cases) | **MET** | `01_KAVACH_Platform/data/held_out_eval_v2.json` |
| **Red-Team Attack Interception** | Multi-vector defense | **19 / 19 vectors intercepted (100.0%)** on authored red-team benchmark | **MET** | `01_KAVACH_Platform/backend/app/security/cyber_attack_simulator.py` |
| **PII / Secret Scanning Latency** | $< 50$ ms | **Median: 0.02 ms, p95: 0.02 ms** (30 runs on Intel 20-core machine) | **MET** | `scripts/generate_metrics.py:run_latency_benchmarks` |
| **E2E Governed Workflow Latency** | $< 1500$ ms | **Median: 608.44 ms, p95: 692.62 ms** (30 runs with AST blast-radius) | **MET** | `scripts/generate_metrics.py:run_latency_benchmarks` |
| **API Endpoints Implemented** | $\ge 10$ endpoints | **120 core routes + 22 mounted routes = 142 total endpoints** | **EXCEEDED** | `app.main:app.routes` |

---

### 3. Proposed Methodology & Architecture (Rubric C3)
Kavach enforces a 6-stage active lifecycle state machine (`REQUEST_RECEIVED` $\to$ `PLANNING` $\to$ `CONTEXT_RETRIEVAL` $\to$ `SECURITY_CHECK` $\to$ `IMPACT_ANALYSIS` $\to$ `GENERATION`), reaching one of 3 terminal states (`COMPLETE`, `BLOCKED`, `NEEDS_REVIEW`):
* **Sentinel Pre-Execution Guard:** Regex patterns and Shannon entropy scans identifying PAN, Aadhaar, phone, email, and credentials.
* **Agentic RAG Grounding:** `all-MiniLM-L6-v2` dense embeddings with local Qdrant vector storage and CPU-friendly fallback.
* **AST Dependency & Blast Radius Engine:** Static Python AST parsing extracting import graphs and predicting affected files.
* **Multi-Model Router & Verification:** Gemini 2.5 Flash / Groq Whisper voice input with air-gapped Ollama and stub fallbacks.

---

### 4. Feasibility, Resource Planning & Tech Stack (Rubric C4)
* **Backend:** Python 3.10+, FastAPI (120 routes), Qdrant Vector Client, Pydantic V2.
* **Frontend:** Modern dark-mode Mission Control Dashboard (Vanilla HTML/CSS/JS, zero build step).
* **Multi-Platform Ecosystem:** Commercial Bharat Core Banking microservice (Port 8050) and Unified Results Cockpit (Port 8090).
* **Hardware Requirements:** Runs entirely locally on consumer PC/laptop with zero paid mandatory dependencies.

---

### 5. Individual Understanding & Team Responsibility (Rubric C5)
* **Team Structure:** Core engineering team with role rotation across Workflows, Security Engine, and RAG Tooling.
* **Public Repository:** Fully reproducible open-source repository at `https://github.com/jaindhruv1923/KAVACH.git`.

---

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 DEVIATIONS FROM PHASE-1 PLAN                                     │
├──────────────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. Framework Architecture: Rather than taking on heavy third-party runtime bloat (google-adk /   │
│    crewai pip packages), implemented native in-repo architectural models following Google ADK     │
│    8-hook specifications and CrewAI sequential/hierarchical flow patterns.                      │
│ 2. Pipeline Scope Discipline: Formally demarcated the 6 active execution stages from the 3       │
│    roadmap passthrough stages (TEST_GENERATION, BUILD_AND_TEST, CICD_GATE) in orchestrator code. │
│ 3. Test & Verification Scale: Expanded scope from the planned 220 tests to 300 deterministic     │
│    verification tests and 641 total repository tests, incorporating Bharat Banking & Results.    │
│ 4. Single Source of Truth: Created scripts/generate_metrics.py to guarantee all metrics are     │
│    empirically measured and reproducible, eliminating self-assigned grades (9.6/10 removed).     │
└──────────────────────────────────────────────────────────────────────────────────────────────────┘
```
