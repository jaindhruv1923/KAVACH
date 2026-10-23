# 📋 KAVACH (कवच) — BRIEF PROGRESS REPORT (WORK IN PROGRESS)
## Mid-Semester Evaluation Report (Criteria C6 – C10 | 30 Marks)
**Course Code & Title:** CSE3101 — Agentic AI (3 Credits, LDP: 2-0-2)  
**Academic Year:** 2026–27 | **Semester:** 7th Semester B.Tech CSE (Batch 2023)  
**Institution:** School of Engineering and Technology, BML Munjal University (BMU)  
**Course Faculty:** **Dr. Soharab Hossain Shaikh** (Associate Professor) & **Mr. Pranshu Tiwari** (Assistant Professor)  
**Student Team:**  
1. **Dhruv Jain** (Roll: **230532** - Lead)  
2. **Dev Garg** (Roll: **230487**)  
3. **Ansh Rohilla** (Roll: **230794**)  
4. **Ansh Adhikari** (Roll: **230822**)  

---

## 📌 Executive Summary

Autonomous coding agents (e.g., Devin, SWE-agent, GitHub Copilot Workspace) exhibit critical production failure modes: hallucinating non-existent package dependencies (19.7% occurrence), leaking proprietary secrets/PII to cloud LLM clusters, modifying code with unbounded blast radius, and looping endlessly without convergence.

**KAVACH (कवच)** is an enterprise-grade, deterministic multi-agent governance platform designed and implemented for **CSE3101: Agentic AI**. It replaces unconstrained stochastic execution with a 6-stage governed pipeline:
$$\text{User Request} \longrightarrow \text{Sentinel Check} \longrightarrow \text{Qdrant RAG} \longrightarrow \text{AST Blast Radius} \longrightarrow \text{LLM Synthesis} \longrightarrow \text{Package Firewall} \longrightarrow \text{Self-Healing Sandbox}$$

### 🏆 Phase-2 Mid-Sem Status At A Glance
* **Phase 1 & Phase 2 Completion:** **100% of planned requirements delivered.**
* **Automated Pytest Test Suite:** **306 Passed out of 306 Tests (100% Pass Rate).**
* **Advanced Modules Pre-Delivered:** Google ADK 8-Hook Callbacks, Canonical Medical Triage Pipeline, CrewAI Flows, Anthropic MCP Server, and Google A2A Byzantine Protocol.
* **Working Prototype:** Fully interactive dark-mode dashboard running at [`http://127.0.0.1:8000`](http://127.0.0.1:8000).
* **Interactive Comic Cloud Explainers (ELI5):** Animated comic-book thought-bubble system translating all 15 syllabus and architectural topics into punchy 1-liners and intuitive analogies, backed by full mathematical dossiers.

---

## Chapter 1: Introduction & Updated Problem Statement
### 1.1 Threat Model of Autonomous Agents
When an autonomous agent operates in a software repository, it makes decisions probabilistically. This induces four distinct threat vectors:
1. **Slopsquatting & Dependency Poisoning:** The agent generates `import py_jwt_vault_secure`. An adversary registers that package on PyPI containing malicious code. When the CI/CD executes `pip install`, arbitrary code execution occurs.
2. **Confidential Egress & Indian DPDP Act 2023 Violations:** Prompts containing database connection strings, AWS keys, or customer Aadhaar/PAN cards are dispatched to external cloud APIs.
3. **Unchecked Blast Radius:** An agent changes a core utility parameter, breaking 15 dependent services that were not in the agent's immediate context window.
4. **Stochastic Oscillation:** The agent attempts a repair, fails a test, reverts, tries another invalid fix, and oscillates until timeout.

### 1.2 Dedicated Mid-Sem Scope Separation
In strict accordance with academic guidelines for the Mid-Sem review, this package isolates the **core multi-agent AI DevOps platform**, excluding unrelated financial banking sub-engines (`implementation_banks`) and results dashboards (`results_dashboard`). The entire package here is 100% self-contained and reproducible.

---

## Chapter 2: Technical Understanding & Academic Rigor (Criterion C7 — 5 Marks)
### 2.1 Information Theory: Shannon Entropy for Secret Interception
Standard regexes cannot catch obfuscated or arbitrary API keys. KAVACH employs Shannon's Information Entropy $H(S)$ over character frequencies:
$$H(S) = -\sum_{i=1}^{k} P(c_i) \log_2 P(c_i), \quad P(c_i) = \frac{\text{count}(c_i)}{|S|}$$
English source code exhibits low entropy ($H \approx 2.0 - 3.2$), whereas cryptographic secrets, base64 strings, and hex keys exhibit high entropy ($H \ge 4.0$). Any token with $H \ge 4.0$ triggers an immediate FSM halt at `BLOCKED`.

### 2.2 Abstract Algebra: Verhoeff Dihedral Group ($D_5$) for Aadhaar Validation
To eliminate false positives from random 12-digit integers while guaranteeing 100% catch rate on valid Indian Aadhaar cards, KAVACH implements the Verhoeff check over the non-commutative dihedral symmetry group $D_5$ (permutations of a regular pentagon):
$$\left( \sum_{i=0}^{n-1} d\left( \text{perm}[i \bmod 8], c_i \right) \right) = 0$$
This detects 100% of single-digit substitution errors and adjacent transposition errors ($ab \leftrightarrow ba$).

### 2.3 Compiler Static Analysis: AST Transitive Blast-Radius Reachability
KAVACH uses Python's compiler parser `ast.parse` to construct a Directed Acyclic Graph (DAG) $G = (V, E)$ of symbol definitions and call expressions. The blast-radius score $B(v)$ of modified symbol $v$ is:
$$B(v) = \frac{|\text{Reach}(v)|}{|V| - 1}, \quad \text{where } \text{Reach}(v) = \{u \in V \mid v \rightsquigarrow u\}$$
If $B(v) > 0.40$ (i.e., affects $>40\%$ of the codebase), KAVACH enforces a Human-In-The-Loop (HITL) approval gate.

---

## Chapter 3: Project Requirements Met Till Now with Actual Approach (Criterion C8 — 10 Marks)

Every syllabus competency across Chapters 1 to 4 of the CSE3101 Handout has been built with an authentic, verified engineering implementation:

| Module & Requirement | Syllabus Topic | KAVACH Actual Implementation Approach | Verified Status |
| :--- | :--- | :--- | :---: |
| **Req 1: Agent FSM Orchestration** | MAS Architecture & Lifecycle | Deterministic 8-stage finite state machine (`REQUEST_RECEIVED` $\to$ `PLANNING` $\to$ `CONTEXT_RETRIEVAL` $\to$ `IMPACT_ANALYSIS` $\to$ `SECURITY_EVALUATION` $\to$ `GENERATION` $\to$ `VALIDATION` $\to$ `COMPLETE` / `BLOCKED`). | ✅ **100% Verified** |
| **Req 2: Pre-Execution Sentinel** | Guardrails & Safety | Mathematical Shannon Entropy ($H \ge 4.0$) + Verhoeff $D_5$ Aadhaar validator halts dangerous execution before invoking LLM. | ✅ **100% Verified** |
| **Req 3: Agentic RAG Store** | Dense Embeddings & Vector DB | Syntax-aware AST chunker (`app/rag/ingest.py`) with local Qdrant vector database and 384-d dense embeddings (`all-MiniLM-L6-v2`). | ✅ **100% Verified** |
| **Req 4: Compiler Blast Radius** | Code Impact Analysis | Computes transitive closure reachability $B(v)$ over symbol dependency DAG using Python's native AST module. | ✅ **100% Verified** |
| **Req 5: Slopsquatting Firewall** | Supply-Chain Defense | AST parser extracts all `import` statements; verifies existence against live PyPI registry LRU cache; catches typosquats via Damerau-Levenshtein. | ✅ **100% Verified** |
| **Req 6: Self-Healing Sandbox** | ReAct Reflection Loop | Ephemeral subprocess runner executes targeted `pytest`; captures failure tracebacks; feeds back into bounded reflection loop ($N=3$). | ✅ **100% Verified** |
| **Req 7: Google ADK 8 Hooks** | Google ADK Callbacks | Conformance to official `adk.dev/callbacks` specification: 8 hook points across 3 phases (`before/after_agent`, `before/after_model`, `before/after_tool`, `on_model/tool_error`). | ✅ **100% Verified** |
| **Req 8: Medical Triage Pipeline** | Canonical ADK Architecture | Two-branch triage: High Urgency (Chest pain $\to$ Emergency Agent $\to$ Call 112/108 with NO medication) vs Normal (Headache $\to$ Persona Agent $\to$ Medicine Agent $\to$ Paracetamol 500mg). | ✅ **100% Verified** |
| **Req 9: CrewAI Stateful Flows** | Workflow Automation | Stateful flow engine implementing `@start`, `@listen`, and `@router` annotations with specialized crew agents. | ✅ **100% Verified** |
| **Req 10: Cognitive Reasoning** | Prompt Strategies | Side-by-side comparative engine for ReAct, Chain-of-Thought (CoT), Tree-of-Thought (ToT), and Self-Consistency (COTS). | ✅ **100% Verified** |
| **Req 11: Interoperability (MCP & A2A)** | Standard Protocols | Anthropic Model Context Protocol (MCP) JSON-RPC 2.0 server (4 tools) + Google Agent-to-Agent (A2A) protocol with signed envelopes and Byzantine consensus. | ✅ **100% Verified** |
| **Req 12: Air-Gapped Privacy Router** | Local LLM Deployment | Zero-knowledge token vaulting + automatic traffic divert to local **Ollama** (`qwen2.5-coder:7b`) with zero cloud network egress. | ✅ **100% Verified** |

---

## Chapter 4: Working Documentation & Code Architecture (Criterion C9 — 5 Marks)
### 4.1 Automated Pytest Suite (306 Tests Passing)
The test suite is partitioned into 12 targeted verification modules:
1. `test_agent.py`: FSM state transitions, planning, error recovery.
2. `test_security.py`: Shannon entropy, Verhoeff checksums, Indian PII detection.
3. `test_security_v2.py`: Policy engine, risk score computation, audit redaction.
4. `test_cyber_defense_tough.py`: 50+ adversary attack vectors (Trojan source, SSRF, Bidi, Obfuscation).
5. `test_adk_callbacks_and_triage.py`: 8-hook callbacks, 8 patterns, Medical Triage pipeline.
6. `test_rag.py`: AST chunking, Qdrant indexing, cosine vector retrieval.
7. `test_impact.py`: AST dependency graph, blast-radius reachability.
8. `test_generation.py`: Evidence-grounded generation, syntax verification.
9. `test_advanced_features.py`: MCP server, token vault, HITL gates, self-healer.
10. `test_syllabus_advanced_modules.py`: CrewAI flows, A2A consensus, vision auditor, reasoning paradigms.
11. `test_api_endpoints.py`: All 42 REST endpoints.
12. `conftest.py`: Shared mock clients and environment fixtures.

### 4.2 Comprehensive Deliverables Library
All formal academic deliverables are archived in [`academic_deliverables/`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/academic_deliverables):
* `01_UPDATED_PROJECT_CHARTER_AND_SYNOPSIS.md`: Problem statement, scope, mathematical equations.
* `02_REVISED_PROJECT_TIMELINE_PROGRESS_VS_PLAN.md`: Progress vs plan, Gantt chart, role rotation.
* `03_WORKING_PROTOTYPE_AND_CODE_DEMO_GUIDE.md`: Step-by-step viva demonstration protocols.
* `04_BRIEF_PROGRESS_REPORT_WIP.md`: This comprehensive work-in-progress report.
* `05_COVERAGE_MATRIX_1_SLIDE.pptx`: Official 1-Slide presentation covering all criteria.
* `CSE3101_HANDOUT_LINE_BY_LINE.md`: 36KB line-by-line audit against the 7-page university handout.

---

## Chapter 5: Individual Contribution & Viva Defense Matrix (Criterion C10 — 5 Marks)

In strict accordance with **Criterion C10 (Individual Contribution / Viva - 5 Marks)** and Page 7 of the CSE3101 Handout, each student has specialized architectural ownership and is prepared for individual defense:

### 1. Dhruv Jain (230532 — Team Lead)
* **Specialized Ownership:** Core FSM Orchestrator (`orchestrator.py`), Google ADK 8-Hook Callbacks (`callbacks.py`), and Canonical Medical Triage Multi-Agent Pipeline (`medical_triage.py`).
* **Viva Defense Competencies:** Explaining asynchronous FSM transition mechanics, Google ADK lifecycle interceptors, urgency classification thresholds, and coordinator-agent delegation trees.

### 2. Dev Garg (230487)
* **Specialized Ownership:** Pre-Execution Sentinel (`secret_detector.py`, `detector.py`), Shannon Entropy calculation, and PyPI Slopsquatting Firewall (`package_firewall.py`).
* **Viva Defense Competencies:** Deriving Shannon Entropy $H(S)$, Verhoeff Dihedral Group multiplication tables, and LRU cache synchronization against registry APIs.

### 3. Ansh Rohilla (230794)
* **Specialized Ownership:** Qdrant Vector Database Integration (`embed_store.py`), AST-aware syntax chunker (`ingest.py`), and Compiler Blast-Radius Analysis (`analyzer.py`).
* **Viva Defense Competencies:** Dense vector similarity mathematics, transitive closure graph algorithms, and AST visitor pattern traversal.

### 4. Ansh Adhikari (230822)
* **Specialized Ownership:** Ephemeral Pytest Self-Healing Sandbox (`self_healer.py`), 306-Test Automated Suite, and Glassmorphic Mission Control Cockpit (`app.js`, `course_cockpit.js`).
* **Viva Defense Competencies:** Subprocess sandbox isolation, bounded ReAct reflection loops ($N=3$), SSE telemetry streams, and Prometheus metric instrumentation.

---

## Chapter 6: Progress vs. Plan & Conclusion (Criterion C6 — 5 Marks)
* **Plan vs. Delivery:** All Phase 1 (September) and Phase 2 (October) targets are 100% delivered and verified.
* **Proactive Acceleration:** Advanced Phase 3 topics (MCP, A2A, ADK Callbacks, CrewAI Flows) are already operational.
* **Final Term Trajectory:** The platform is fully prepared for Phase 3 enterprise containerization, Kubernetes helm packaging, and final university capstone defense.
