# KAVACH: Comprehensive Viva Defense & Evaluator Master Pack
**Course Code:** CSE3101 — Agentic AI & Capstone Project-IV  
**Institution:** School of Engineering and Technology, BML Munjal University (BMU)  
**Evaluator Reference:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  
**Student:** Dhruv Jain  
**Verification Baseline:** 100% matched to current committed codebase (`main` branch)  

---

## 1. Verified Module Breakdowns, Key Decisions & Honest Limitations

### Module 1: Agent Orchestrator & Lifecycle Coordination
* **Files:** [`backend/app/agent/orchestrator.py`](backend/app/agent/orchestrator.py), [`backend/app/agent/state.py`](backend/app/agent/state.py)
* **Key Design Decisions:**
  - **Google ADK Coordinator:** Manages the full agent lifecycle (`INITIALIZED` $\to$ `PLANNING` $\to$ `EXECUTING_TOOL` $\to$ `REFLECTING` $\to$ `COMPLETED`).
  - **Fail-Safe Fallback:** If any framework exception or timeout occurs, execution gracefully falls back to the procedural `run_workflow_deterministic()`.
  - **Privacy Boundary:** Raw user input is de-identified via `redact_text()` before dispatching to the planner sub-agent; prompts sent downstream never contain raw PII.
* **Limitations (Honest Scope):**
  - Human-in-the-Loop (`NEEDS_REVIEW`) halts the execution graph until explicitly resumed via `POST /agent/runs/{id}/resume`. Automatic escalation policies are not yet autonomous.

---

### Module 2: Sensitive Data Detection & Verhoeff Checksum Verification
* **Files:** [`backend/app/security/detector.py`](backend/app/security/detector.py), [`backend/app/security/verhoeff.py`](backend/app/security/verhoeff.py), [`backend/app/security/patterns.py`](backend/app/security/patterns.py)
* **Key Design Decisions:**
  - **Dihedral Group $D_5$ Verhoeff Checksum:** UIDAI-compliant algorithmic validation enforcing leading digit constraints ($\notin \{0, 1\}$) and error-detecting permutation multiplication.
  - **Two-Tier Identity Context Heuristic:**
    - High-Confidence Aadhaar: Valid Verhoeff checksum + identity context ("aadhaar", "uid", "आधार", "pehchan") $\to$ Classified as `Aadhaar-like` (`BLOCK`, high severity).
    - Isolated 12-Digit Number: Valid Verhoeff checksum without context $\to$ Classified as `possible_id` (`REDACT`, low severity). Never triggers a false hard BLOCK.
  - **Word Boundary Regex:** Enforces `(?<!\w)` and `(?!\w)` boundaries, preventing UUIDs (e.g. `urn:uuid:23456789-0124-4000...`) from falsely matching `"uid"`.
* **Empirical Benchmark Results:**
  - Evaluated on a 68-case test set (`tests/test_aadhaar_verhoeff.py`):
    - False Positive Rate: **0.00%** (0 / 49 false positive candidates)
    - False Negative Rate: **0.00%** (0 / 19 valid numbers missed)
    - Accuracy: **100.00%**
    - Unjustified Hard Blocks: **0**

---

### Module 3: Change-Impact Blast-Radius Analysis
* **Files:** [`backend/app/impact/analyzer.py`](backend/app/impact/analyzer.py), [`backend/app/rag/embed_store.py`](backend/app/rag/embed_store.py)
* **Key Design Decisions:**
  - **Hybrid Relevance Scoring:** Fuses AST dependency link parsing (+0.40 bonus for direct callers/importers) with Sentence-Transformers dense vector cosine similarity (0.60 weight).
  - **Impact Tiers:** Categorized into `CRITICAL` ($\ge 0.70$), `HIGH` ($\ge 0.50$), `MEDIUM` ($\ge 0.30$), and `LOW` ($< 0.30$).
* **Limitations:**
  - Dynamic runtime reflection (`getattr`, `importlib`) and indirect RPC calls across microservices are not tracked by static AST import parsing.

---

### Module 4: Cryptographic Audit Ledger & Tamper Detection (Kaikei)
* **Files:** [`backend/app/security/merkle_ledger.py`](backend/app/security/merkle_ledger.py), [`backend/app/main.py`](backend/app/main.py)
* **Key Design Decisions:**
  - **NIST FIPS 202 SHA3-512 (Keccak Sponge):** Immune to Merkle-Damgård Length Extension Attacks (LEA) by design, with 256-bit collision security margin.
  - **Cryptographic Merkle Proofs:** Binary tree parent node chaining generating inclusion proofs for DPDP Act 2023 statutory audit compliance.
  - **In-Memory Tamper Simulator (`POST /security/merkle/tamper-demo`):** Clones a deep copy of the ledger in memory, injects an adversarial payload modification, and mathematically demonstrates `verify_ledger_integrity()` isolating the exact corrupted leaf index without touching live records.
* **Limitations:**
  - The ledger is append-only in memory with JSON persistence. Distributed Byzantine fault tolerance across external validator nodes is left for future clustering.

---

### Module 5: API Security & Server Hygiene
* **Files:** [`backend/app/main.py`](backend/app/main.py), [`tests/test_api_endpoints.py`](tests/test_api_endpoints.py)
* **Key Design Decisions:**
  - **FastAPI Lifespan Context Manager:** Replaces deprecated `@app.on_event("startup")` with `@asynccontextmanager async def lifespan(app)`, pre-warming models in background threads and eliminating all Starlette deprecation warnings.
  - **Strict CORS Origin Whitelist:** Reads from `CORS_ORIGINS` environment variable, defaulting strictly to localhost multi-port origins (`8000`, `3000`, `8080`, `5500`, `5173`, `null`).

---

## 2. Five Critical Examiner Questions & Verbatim Code-Grounded Answers

### Q1: "How do you avoid false positive Aadhaar blocks on arbitrary 12-digit numbers or UUIDs?"
> **Verbatim Answer:**  
> *"In `backend/app/security/detector.py` and `patterns.py`, we implement a two-stage filter:  
> 1. Algorithmic Checksum: We run the Dihedral Group $D_5$ Verhoeff algorithm implemented in `verhoeff.py`, verifying checksum validity and rejecting leading digits 0 and 1 per UIDAI specifications.  
> 2. Context Gating: A valid Verhoeff number only triggers an `Aadhaar-like` (`BLOCK`) finding if it has nearby identity context keywords (e.g., 'aadhaar', 'uid', 'पहचान पत्र') matched with word-boundary lookbehinds `(?<!\w)`. Isolated 12-digit numbers that pass Verhoeff by random collision (~10% base-10 rate) are classified as `possible_id` and redacted, but never blocked. On our 68-case benchmark, this achieved an empirical False Positive Rate of exactly 0.00%."*

---

### Q2: "Did you use Google ADK in your primary workflow or is it just a standalone script?"
> **Verbatim Answer:**  
> *"In `backend/app/agent/orchestrator.py`, our primary `run_workflow` routes directly through `run_workflow_adk()`, which instantiates a Google ADK `CoordinatorAgent` registered with five specialized ADK `LlmAgent` sub-agents: `SentinelAgent` for pre-execution policy gating, `PlannerAgent` for privacy-bounded planning, `RetrieverAgent` for vector context retrieval, `ImpactAnalystAgent` for AST blast-radius calculation, and `CoderAgent` for patch synthesis.  
> Crucially, for enterprise fail-safe resilience, if any framework dependency or timeout fails, the system catches the exception and engages `run_workflow_deterministic()` as an explicitly recorded fallback (`run.metadata['orchestration_engine'] = 'DETERMINISTIC_FALLBACK'`). Both execution modes are verified in `tests/test_agent.py`."*

---

### Q3: "How does your Merkle Ledger prove tamper detection without corrupting production data?"
> **Verbatim Answer:**  
> *"Our Kaikei-inspired audit engine in `backend/app/security/merkle_ledger.py` builds a binary Merkle tree over canonical event preimages using NIST FIPS 202 SHA3-512.  
> To safely demonstrate tamper detection to evaluators, we implemented `POST /security/merkle/tamper-demo` in `backend/app/main.py`. This endpoint creates a `deepcopy` of the ledger in memory, injects an unauthorized record alteration at a target leaf index, and executes `verify_ledger_integrity()`. Because the preimage hash no longer matches the stored leaf hash, the root recalculation fails and the engine isolates the exact corrupted leaf index. Meanwhile, the live production ledger remains completely untouched, verified by `GET /security/merkle/verify` returning `is_valid: true`."*

---

### Q4: "What is your RAG retrieval quality and what happens if no LLM API key is present?"
> **Verbatim Answer:**  
> *"We evaluated our dense Sentence-Transformers + Qdrant RAG pipeline on 32 pre-determined ground-truth queries over `backend/app/`. As recorded in our commit `158f636` and `eval_results.json`, retrieval achieved:  
> - Hit@1: **68.75%**  
> - Hit@5: **96.88%**  
> - Mean Reciprocal Rank (MRR): **0.8281**  
> - Mean Latency: **24.75 ms**  
> If no `GEMINI_API_KEY` is configured, our planner and generator do not throw 500 errors or hang: they execute a deterministic fallback planner in $<5$ ms and return an honest test-mode response with zero hallucinated API claims, verified in `tests/test_agent.py`."*

---

### Q5: "What is the role of the Medical Triage Pipeline in your repository?"
> **Verbatim Answer:**  
> *"The Medical Triage pipeline in `backend/app/adk/medical_triage.py` is strictly a CSE3101 course exercise implemented directly from the professor's quiz problem statement and reference architecture. It demonstrates Google ADK conditional callback routing: high-urgency queries gate to `emergency_agent` (dispatching to 112/108 and strictly forbidding medication), while normal urgency gates to `persona_agent` and `medicine_agent` for Tavily OTC remedy discovery.  
> It is strictly isolated and labeled as a course exercise; it is not part of the KAVACH enterprise DevOps or banking platform."*
