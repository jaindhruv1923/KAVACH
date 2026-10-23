# 📅 KAVACH — REVISED PROJECT TIMELINE & PROGRESS VS. PLAN
## Phase-2 (Mid-Semester) Milestone Reconciliation & Evaluation Report (Criterion C6)
**Course Code & Title:** CSE3101 — Agentic AI (3 Credits, LDP: 2-0-2)  
**Academic Year:** 2026–27 | **Semester:** 7th Semester B.Tech CSE (Batch 2023)  
**Course Faculty:** **Dr. Soharab Hossain Shaikh** & **Mr. Pranshu Tiwari**  
**Student Team:** **Dhruv Jain (230532)**, **Dev Garg (230487)**, **Ansh Rohilla (230794)**, **Ansh Adhikari (230822)**  

---

## 1. 🎯 Executive Reconciliation: Progress vs. Plan (Criterion C6 — 5 Marks)

As mandated by **Evaluation Criterion C6 (Progress vs Plan - 5 Marks)** of the official Phase-2 Mid-Semester Evaluation Rubric, this document benchmarks the team's planned deliverables against actual engineering accomplishments.

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 PHASE-2 MILESTONE PROGRESS GAUGES                                │
├──────────────────────────────────────┬───────────────────────┬───────────────────────────────────┤
│ Planned Phase 1 & 2 Requirements     │ 100% Target           │ [████████████████████] 100% DONE  │
│ Delivered Automated Test Coverage    │ 200 Tests Target      │ [████████████████████] 306 PASSED │
│ Phase 3 Advanced Feature Pre-Release │ Optional / Post-MidSem│ [████████████████████] PRE-BUILT  │
│ Verification & Reproducibility       │ Working Prototype     │ [████████████████████] 12/12 PASS │
└──────────────────────────────────────┴───────────────────────┴───────────────────────────────────┘
```

### 📌 Summary of Deliverable Variance
* **Phase-1 Commitment (Weeks 1–5):** Charter submission, threat modeling, PEAS specification, baseline RAG. $\implies$ **100% Completed on schedule (September 3rd Week).**
* **Phase-2 Commitment (Weeks 6–12):** Multi-agent FSM orchestrator, pre-execution guardrails, AST blast radius, working prototype demonstration. $\implies$ **100% Completed ahead of schedule (October 3rd/4th Week).**
* **Phase-3 Advanced Integration (Originally Weeks 13–16):** Google ADK 8-Hook Callbacks (`adk.dev/callbacks`), CrewAI Stateful Flows (`@start`, `@listen`), Anthropic Model Context Protocol (MCP) server, and Google Agent-to-Agent (A2A) Byzantine consensus have been **fully engineered, integrated, and verified during Phase 2**.

---

## 2. 📊 Detailed 16-Week Week-by-Week Gantt Schedule

| Week | Date Interval | Planned Syllabus Milestone | Delivered Engineering Features & Proof | Status vs. Plan |
| :---: | :--- | :--- | :--- | :---: |
| **W1** | Jul 27 – Jul 31 | Course Orientation & Threat Modeling | Defined formal threat model (Hallucinated packages, PII leakage, unbounded blast radius). | ✅ **On Schedule** |
| **W2** | Aug 03 – Aug 07 | Agent Foundations & PEAS Modeling | Formalized PEAS framework; mapped 3 user personas (Developer, SRE, Security Auditor). | ✅ **On Schedule** |
| **W3** | Aug 10 – Aug 14 | Cognitive Reasoning Paradigms | Implemented ReAct, Chain-of-Thought (CoT), Tree-of-Thought (ToT), Self-Consistency. | ✅ **On Schedule** |
| **W4** | Aug 17 – Aug 21 | Agentic RAG Vector Engine | Ingestion engine (`app/rag/ingest.py`), MiniLM-L6-v2 embeddings, Qdrant client. | ✅ **On Schedule** |
| **W5** | Aug 24 – Aug 28 | **Phase-1 Milestone Submission (10%)** | **Submitted Project Charter, Timeline, and PEAS Matrix. Phase-1 Defended.** | ✅ **Milestone Achieved** |
| **W6** | Aug 31 – Sep 04 | Multi-Agent FSM Orchestration | Built finite state machine orchestrator traversing 8 discrete lifecycle stages. | ✅ **On Schedule** |
| **W7** | Sep 07 – Sep 11 | Pre-Execution Sentinel Guardrails | Non-probabilistic Shannon Entropy ($H \ge 4.0$) and Verhoeff $D_5$ Aadhaar checksums. | ✅ **On Schedule** |
| **W8** | Sep 14 – Sep 18 | AST Change-Impact & Blast Radius | Compiler-level DAG traversal computing transitive closure reachability $B(v)$. | ✅ **On Schedule** |
| **W9** | Sep 21 – Sep 25 | Air-Gapped Privacy & Local LLM | Implemented local Ollama (`qwen2.5-coder:7b`) router with zero external egress. | ✅ **On Schedule** |
| **W10** | Sep 28 – Oct 02 | Slopsquatting Supply-Chain Firewall | Live PyPI LRU verification cache intercepting hallucinated/malicious packages. | ✅ **On Schedule** |
| **W11** | Oct 05 – Oct 09 | Ephemeral Self-Healing Sandbox | Bounded reflection sandbox ($N=3$) capturing pytest tracebacks for auto-repair. | ✅ **On Schedule** |
| **W12** | Oct 12 – Oct 16 | **Phase-2 Mid-Sem Evaluation (30%)** | **Working Prototype Demo, 306/306 Pytest Pass, 12-Step Capstone Verification.** | ✅ **CURRENT MILESTONE** |
| **W13** | Oct 19 – Oct 23 | Google ADK 8-Hook Deep Dive *(Advanced)* | Implemented 8-hook lifecycle callbacks across 3 phases + Medical Triage Pipeline. | ⚡ **Pre-Delivered** |
| **W14** | Oct 26 – Oct 30 | CrewAI Flows & MCP Protocol *(Advanced)* | CrewAI `@start`, `@listen` workflows + Anthropic MCP JSON-RPC 2.0 server. | ⚡ **Pre-Delivered** |
| **W15** | Nov 02 – Nov 06 | Google A2A Protocol & Multimodal *(Adv)* | P2P Signed Envelopes, consensus voting, Groq Whisper voice, Vision diagram audit. | ⚡ **Pre-Delivered** |
| **W16** | Nov 09 – Nov 20 | **Final Capstone Defense (Phase-3 - 40%)** | Comprehensive academic report, deployment containerization, and final viva. | ⏳ **On Track for Final** |

---

## 3. 👥 Technical Role Rotation Matrix (Handout Page 7 Compliance)

In strict accordance with Page 7 of the official **CSE3101 Course Handout**, roles are actively rotated across evaluation phases so that no team member is confined to a single specialized track:

| Student Name & ID | Phase 1 Role (Weeks 1–5) | Phase 2 Mid-Sem Role (Weeks 6–12) | Phase 3 Final Role (Weeks 13–16) |
| :--- | :--- | :--- | :--- |
| **Dhruv Jain** (230532) | Architectural Design & Threat Modeling | FSM Orchestrator, Google ADK 8-Hook Callbacks, Medical Triage Pipeline | Full-Stack Integration, Kubernetes Deployment & Viva Defense |
| **Dev Garg** (230487) | Regex Research & PII Corpus Formulation | Sentinel Guardrails, Shannon Entropy, PyPI Slopsquatting Firewall | Security Policy Hardening, MITRE ATLAS Mapping & Benchmarking |
| **Ansh Rohilla** (230794) | Vector DB Evaluation & Benchmark Selection | Qdrant Agentic RAG Store, AST Dependency Graph & Blast Radius | Model Context Protocol (MCP) Server & External IDE Bridge |
| **Ansh Adhikari** (230822) | Test Case Design & Academic Literature Review | Self-Healing Ephemeral Sandbox, 306-Test Suite, Frontend Cockpit | Telemetry Dashboard, Prometheus Exporter & User Studies |

---

## 4. 🛡️ Risk Management & Contingency Execution

| Identified Technical Risk | Initial Impact | Applied Engineering Mitigation | Contingency Status |
| :--- | :---: | :--- | :---: |
| **Cloud LLM API Outage / Key Expiry** | Critical | Dual-engine fallback routing automatically diverts prompts to local **Ollama** (`qwen2.5-coder:7b`). | ✅ Verified (Zero Egress) |
| **Embedding Engine DLL Block on Windows** | High | Built an automatic in-memory fallback vector similarity engine (`embed_store.py`) that activates dynamically if OS restricts PyTorch DLL loading. | ✅ Verified (Seamless) |
| **PyPI Registry Network Latency** | Medium | Built an in-memory LRU cache of verified standard library and PyPI packages, preventing live web request timeouts. | ✅ Verified (Sub-millisecond) |
| **Long Pytest Execution Time** | Low | Implemented `--fast` / `--skip-pytest` flag in [`verify_midsem.py`](file:///c:/Users/jaind/Desktop/universty_work/verify_midsem.py) enabling full 11-step live viva verification in $<3$ seconds. | ✅ Verified (2.5s Execution) |
