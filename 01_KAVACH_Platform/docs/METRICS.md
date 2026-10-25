# KAVACH System Metrics (Single Source of Truth)

**Generated**: `2026-10-25T02:34:01Z`  
**Commit Hash**: `ad2277e21fd1af43a7d9204262d7639395849682`  
**Source Script**: [`scripts/generate_metrics.py`](file:///scripts/generate_metrics.py)  
**Rule**: All documentation figures must reference or match values in this report.

---

## 1. Machine & Environment Specifications

| Parameter | Measured Specification |
|---|---|
| **Operating System** | Windows 11 (Build 10.0.26300) |
| **Architecture** | AMD64 |
| **Processor** | Intel64 Family 6 Model 154 Stepping 3, GenuineIntel |
| **CPU Logical Cores** | 20 |
| **System RAM** | 15.75 GB |
| **Python Version** | 3.14.7 |

---

## 2. Test Suite & Verification Inventory

| Suite Name | Scope & Path | Tests | Pass Rate | Status |
|---|---|---|---|---|
| **KAVACH Deterministic 100** | `01_KAVACH_Platform/tests/test_kavach_100_suite.py` | 100 | 100% | PASS |
| **Bharat Banking 100** | `02_Banking_and_Results_Dashboard/implementation_banks/test_banking_100_suite.py` | 100 | 100% | PASS |
| **Unified Cross-Platform 100** | `02_Banking_and_Results_Dashboard/tests_unified/test_unified_100_suite.py` | 100 | 100% | PASS |
| **Deterministic Master Verification Total** | **All 3 Deterministic Verification Suites** | **300** | **100%** | **PASS (300/300)** |
| **Complete Repo Pytest Inventory** | Complete repository test suite (18 test files) | **641** | **100%** | **PASS (641/641)** |

---

## 3. API Endpoints Catalog

- **KAVACH Core Platform Registered Routes**: `120`
- **Mounted Sub-Applications**:
  - `/bank`: Bharat Core Banking Highway (15 API endpoints)
  - `/results`: Unified Results Cockpit (7 API endpoints)
- **Total Unified Endpoints Across Platform**: `142`

### Endpoint Breakdown by Subsystem
- Core Security & Guardrails: `26`
- Agent Orchestration & Impact: `21`
- Threat Intelligence & v3.0: `18`
- ADK & Crew Architecture: `12`
- RAG & Ingestion: `4`
- Observability & Evaluation: `7`
- System, Webhooks & Static Dashboards: `32`

---

## 4. Pipeline Architecture (Orchestrator Source of Truth)

The agent orchestrator (`app/agent/orchestrator.py`) executes **6 active lifecycle stages** before transitioning to a terminal state:

1. **`REQUEST_RECEIVED`**: Ingests developer request, runs initial PII and secret detection, and evaluates entry risk policy.
2. **`PLANNING`**: Decomposes prompt into step-by-step tasks with keyword identification.
3. **`CONTEXT_RETRIEVAL`**: Searches indexed repository vector database (RAG) for top-k contextual code chunks.
4. **`SECURITY_CHECK`**: Sanitizes retrieved repository context, scrubs Trojan Source markers, and enforces indirect prompt injection shields.
5. **`IMPACT_ANALYSIS`**: Computes affected files combining AST import dependencies and semantic similarity.
6. **`GENERATION`**: Evidence-grounded generation via configured LLM/stub with AST syntax validation and output safety checks.

**Terminal Decision States (3)**:
- `COMPLETE`: Successful execution through all 6 security-governed stages.
- `BLOCKED`: Hard halt on unredactable critical secrets, severe PII, or attack payloads.
- `NEEDS_REVIEW`: Human-in-the-loop review required.

**Roadmap / Unwired Enum States**:
- `TEST_GENERATION`, `BUILD_AND_TEST`, `CICD_GATE` (defined in `state.py` enum as future roadmap phases; honestly labeled as passthrough/unwired in current orchestrator).

---

## 5. Security Engine & Detector Evaluation

### 5.1 Baseline V1 Dataset (Author-Curated)
- **Dataset**: `data/test_corpus.json (V1 Baseline)` (50 samples)
- **Authorship Caveat**: Author-curated unit-test corpus
- **Precision**: `100.0%`
- **Recall**: `100.0%`
- **F1 Score**: `100.0%`
- **Confusion Matrix**: TP=31, FP=0, FN=0, TN=19

### 5.2 Held-Out V2 Dataset (Independent & Hard Negatives)
- **Dataset**: `data/held_out_eval_v2.json (V2 Held-Out)` (45 fresh cases)
- **Authorship Caveat**: Independent held-out evaluation corpus with realistic false-positive distractors (order codes, SKUs, timeouts)
- **Precision**: `89.3%`
- **Recall**: `100.0%`
- **F1 Score**: `94.3%`
- **Confusion Matrix**: TP=25, FP=3, FN=0, TN=17
- **Analysis**: Identified 3 false-positive edge cases (order IDs / SKU codes containing 10-digit numeric chunks). Recall remains 100% (25/25 sensitive patterns caught).

---

## 6. Red-Team Cyber Attack Simulator Benchmark

- **Total Adversarial Vectors**: `19`
- **Attacks Neutralized / Intercepted**: `19`
- **Interception Rate**: `100.0%`
- **Taxonomy Alignment**: MITRE ATLAS & OWASP Top 10 for LLMs
- **Dataset Caveat**: Authored 15-vector adversarial simulation corpus spanning prompt injection, trojan source, SSRF, and steganography.

---

## 7. Latency Benchmarks (30 Runs)

| Component | Runs | Median Latency | p95 Latency | Min Latency | Max Latency |
|---|---|---|---|---|---|
| **PII Detector** | 30 | **0.02 ms** | 0.02 ms | 0.02 ms | 0.03 ms |
| **Secret Detector** | 30 | **0.02 ms** | 0.02 ms | 0.02 ms | 0.06 ms |
| **Agent Workflow (E2E)** | 30 | **665.73 ms** | 783.16 ms | 257.52 ms | 814.10 ms |
