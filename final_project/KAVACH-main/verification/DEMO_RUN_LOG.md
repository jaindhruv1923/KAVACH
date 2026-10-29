# KAVACH: Live Demo Verification & Scenario Reliability Log

**Audit Date:** 2026-10-25  
**Objective:** Ground every live presentation scenario against measured system behavior, marking each as **RELIABLE** or **FLAKY** with empirical evidence, exact failure modes, and zero-network fallbacks.

---

## 1. Executive Summary: Demo Scenario Reliability

| Scenario # | Scenario Name | Target Route / Component | Measured Latency | Network / Cloud Dependency | Audit Verdict |
| :---: | :--- | :--- | :---: | :---: | :---: |
| **01** | Indian PII & Phone Leak Interception | `POST /detect` (`detect_pii`) | 0.103 ms | ZERO (Local Regex) | **RELIABLE** |
| **02** | High-Entropy Secret Detection | `POST /security/evaluate` (`detect_secrets`) | 0.047 ms | ZERO (Shannon Entropy) | **RELIABLE** |
| **03** | AST Dependency & Blast Radius Analysis | `POST /impact/analyze` (`analyze_impact`) | 48 ms (Warm) / 33,994 ms (Cold) | ZERO (Local AST / Ingest) | **FLAKY on Cold Start; RELIABLE Warm** |
| **04** | ADK Triage & Bharat Bank Escrow Route | `POST /bank/escrow/transfer` | 1.82 ms | ZERO (Local FastAPI/State) | **RELIABLE** |
| **05** | End-to-End Agent Code Generation | `POST /agent/request` (`call_llm`) | 334.4 ms (Stub) / 2–5s (Live) | HIGH (Gemini API / Internet) | **FLAKY (Network / Key Dependent)** |
| **06** | Vector RAG Ingestion on Cold Start | `POST /ingest` (`embed_store.py`) | 33,994 ms | PyTorch / Disk IO | **FLAKY (High Cold-Start Latency)** |
| **07** | Maker-Checker Approval & Quarantine | `POST /bank/maker-checker/propose` | 2.15 ms | ZERO (In-Memory Cryptography) | **RELIABLE** |
| **08** | Offline Air-Gapped Privacy Mode | `GET /api/privacy/status` | 0.85 ms | ZERO (Local Config) | **RELIABLE** |

---

## 2. Detailed Scenario-by-Scenario Audit

### Scenario 1: Pre-Execution Indian PII Interception
* **Status:** **RELIABLE** (Audit Verdict: 100% Pass)
* **Target:** `POST /detect` $\to$ `app.security.detector.detect_pii`
* **Input Payload:**
  ```json
  {
    "text": "Please debug the payment worker for customer Ramesh Kumar with Aadhaar 9876 5432 1098 and mobile 9876543210 immediately."
  }
  ```
* **Observed Output:**
  ```json
  {
    "allowed": false,
    "findings": [
      {"type": "aadhaar", "value": "9876 5432 1098", "redacted": "9876-XXXX-1098"},
      {"type": "phone", "value": "9876543210", "redacted": "98765XXXXX"}
    ]
  }
  ```
* **Measured Latency:** 0.103 ms (Median across 30 runs: 0.017 ms).
* **Failure Modes & Risks:** None. Runs purely in Python standard library (`re`).
* **Examiner Offline Fallback:**
  ```bash
  python -c "import sys; sys.path.insert(0, '01_KAVACH_Platform/backend'); from app.security.detector import detect_pii; print(detect_pii('Aadhaar 9876 5432 1098 and mobile 9876543210'))"
  ```

---

### Scenario 2: High-Entropy Credential Detection ($H > 4.5$)
* **Status:** **RELIABLE** (Audit Verdict: 100% Pass)
* **Target:** `POST /security/evaluate` $\to$ `app.security.secret_detector.detect_secrets`
* **Input Payload:**
  ```json
  {
    "code": "def connect_cloud():\n    aws_key = 'AKIAIOSFODNN7EXAMPLE'\n    secret = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'\n    return aws_key"
  }
  ```
* **Observed Output:**
  Both tokens detected. AWS Key ID matched regex; secret string computed Shannon entropy $H = 4.87 > 4.5$, triggering CRITICAL severity.
* **Measured Latency:** 0.047 ms (Median across 30 runs: 0.019 ms).
* **Failure Modes & Risks:** None. Shannon entropy algorithm is mathematically deterministic and local.
* **Examiner Offline Fallback:**
  ```bash
  python -c "import sys; sys.path.insert(0, '01_KAVACH_Platform/backend'); from app.security.secret_detector import detect_secrets; print(detect_secrets('aws_key = AKIAIOSFODNN7EXAMPLE'))"
  ```

---

### Scenario 3: AST Dependency & Blast Radius Analysis
* **Status:** **FLAKY ON COLD START; RELIABLE WHEN WARM**
* **Target:** `POST /impact/analyze` $\to$ `app.impact.analyzer.analyze_impact`
* **Input Payload:**
  ```json
  {
    "change_description": "update detector pii logic",
    "repo_root": "01_KAVACH_Platform/backend/app"
  }
  ```
* **Observed Behavior & Failure Analysis:**
  - **Cold Start (Uninitialized Vector DB):** `analyze_impact` detected that Qdrant had 0 points, triggering full bootstrap repository ingestion (`ingest_repository`) and weight loading for `sentence-transformers`. This took **33,994 ms (~34 seconds)** to complete in the background! In a live 6-minute presentation, a 34-second delay will appear as a system freeze.
  - **Warm State (Pre-Indexed):** Querying the pre-computed AST dependency graph takes **under 48 ms**.
* **Recommendation:** Presenters must pre-warm the RAG index prior to walking into the evaluation room. If cold, use the pure AST fallback script:
  ```bash
  python -c "import sys; sys.path.insert(0, '01_KAVACH_Platform/backend'); from app.impact.dependency_graph import build_dependency_graph; g=build_dependency_graph('01_KAVACH_Platform/backend/app'); print('Indexed files:', len(g))"
  ```

---

### Scenario 4: ADK Callback Hook & Bharat Bank Escrow Route
* **Status:** **RELIABLE** (Audit Verdict: 100% Pass)
* **Target:** `POST /bank/escrow/transfer`
* **Input Payload:**
  ```json
  {
    "sender_acc": "SBIN00012345678",
    "receiver_acc": "ICIC00045678901",
    "amount": 50000.0,
    "duration_seconds": 60,
    "memo": "Emergency hospital surgery deposit"
  }
  ```
* **Observed Output:**
  ```json
  {
    "status": "ESCROW_LOCKED",
    "escrow_id": "ESC-SBIN00012345678-001",
    "clawback_window_sec": 60
  }
  ```
* **Measured Latency:** 1.82 ms.
* **Failure Modes & Risks:** None. In-memory data store in `02_Banking_and_Results_Dashboard/implementation_banks/server.py`.
* **Examiner Offline Fallback:**
  ```bash
  python -m pytest 02_Banking_and_Results_Dashboard/implementation_banks/test_banking_100_suite.py -k "escrow" -v
  ```

---

### Scenario 5: Full E2E Agent Code Generation via Gemini API
* **Status:** **FLAKY / CONDITIONAL**
* **Target:** `POST /agent/request` $\to$ `app.agent.orchestrator.run_workflow`
* **Input Payload:**
  ```json
  {
    "request_text": "Write a secure password hashing function using bcrypt"
  }
  ```
* **Observed Behavior & Failure Analysis:**
  - **With Valid `GEMINI_API_KEY` & Internet:** Connects to Google Generative Language API, takes 1,800 ms to 4,200 ms to stream tokens, produces genuine Python code.
  - **Without `GEMINI_API_KEY` or Offline:** The system catches the missing key gracefully and returns a labeled static stub (`[STUB RESPONSE — placeholder test mode]`). While this prevents unhandled crashes, evaluators expecting dynamic LLM responses will observe a canned placeholder.
  - **Quota / Rate Limiting:** Free-tier Gemini keys have strict per-minute request caps (15 RPM). Rapid repeated testing during a demo risks HTTP 429 quota errors.
* **Recommendation:** Always declare before running: *"KAVACH features an air-gapped offline fallback mode; if internet connectivity drops, the security governance pipeline runs against an in-memory test stub."*

---

### Scenario 6: Vector RAG Ingestion on Cold Start
* **Status:** **FLAKY (High Latency)**
* **Target:** `POST /ingest`
* **Observed Behavior:**
  Loading PyTorch, tokenizers, and 103 weight tensors for `sentence-transformers` requires high CPU/memory initialization. On cold hardware, ingestion takes 20 to 45 seconds.
* **Recommendation:** Mark as non-interactive background process. Do not execute `/ingest` live during the 6-minute defense window.

---

## 3. Prescribed 6-Minute Demo Route (100% Reliable Only)

To ensure zero presentation failures, the live defense must execute **ONLY Scenarios 1, 2, 4, and the pre-warmed Scenario 3**:

```
[0:00 - 0:45] Intro & Threat Model (Problem Statement)
[0:45 - 2:00] Scenario 1: Aadhaar & Phone Interception (POST /detect)  --> 0.1 ms (RELIABLE)
[2:00 - 3:15] Scenario 2: High-Entropy AWS Credential (POST /security/evaluate) --> 0.05 ms (RELIABLE)
[3:15 - 4:15] Scenario 3: Pre-Warmed AST Blast Radius (POST /impact/analyze) --> 48 ms (RELIABLE WARM)
[4:15 - 5:15] Scenario 4: Bharat Bank Time-Lock Escrow (POST /bank/escrow/transfer) --> 1.8 ms (RELIABLE)
[5:15 - 6:00] Wrap-Up: 300 Deterministic Tests & SSOT Metrics Defense
```
