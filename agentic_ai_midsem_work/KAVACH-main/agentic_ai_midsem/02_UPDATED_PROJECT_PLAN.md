# KAVACH (कवच): Updated Project Plan & Progress-vs-Plan Audit
## 16-Week Agile Milestone Tracking, Slip Analysis & Phase-3 Roadmap
**Academic Course:** CSE3101 — Agentic AI (3 Credits, LDP: 2-0-2)  
**Semester & Batch:** 7th Semester B.Tech CSE (AI & Data Science) · Academic Year 2026–27  
**Faculty Mentors:** Dr. Soharab Hossain Shaikh (Course Coordinator) & Mr. Pranshu Tiwari  
**Institution:** BML Munjal University, Gurugram  
**Team Members:** Dhruv Jain, Hemant Goyal, Rajat Yadav  
**Deliverable Type:** Mid-Term Evaluation (Phase-2) Deliverable 2 (Rubric C6)  

---

## 1. 16-Week Project Execution Schedule: Planned vs. Actual

```
+---------------------------------------------------------------------------------------------------------+
|                                16-WEEK AGENTIC AI CAPSTONE TIMELINE                                     |
+--------+----------------------------------------------------+--------------+-------------+--------------+
| Week   | Milestone / Module Description                     | Planned Wk   | Actual Wk   | Status       |
+--------+----------------------------------------------------+--------------+-------------+--------------+
| W01    | Threat modeling, PEAS definition & Project Charter | Week 1       | Week 1      | COMPLETED    |
| W02    | Baseline regex PII & secret detection engine       | Week 2       | Week 2      | COMPLETED    |
| W03    | Phase-1 Submission & Project Charter Evaluation    | Week 3       | Week 3      | COMPLETED    |
| W04    | AST code parser & function chunking prototype      | Week 4       | Week 4      | COMPLETED    |
+--------+----------------------------------------------------+--------------+-------------+--------------+
| W05    | Qdrant dense vector store integration (all-MiniLM) | Week 5       | Week 5      | COMPLETED    |
| W06    | 10-Stage Finite State Machine (FSM) Orchestrator   | Week 6       | Week 6      | COMPLETED    |
| W07    | Bidirectional AST blast-radius analyzer            | Week 7       | Week 7      | COMPLETED    |
| W08    | PyPI Slopsquatting & package verification firewall | Week 8       | Week 8      | COMPLETED    |
| W09    | Bounded ReAct self-healing sandbox loop (N <= 3)   | Week 9       | Week 9      | COMPLETED    |
| W10    | Model Context Protocol (MCP) & Google A2A protocol | Week 10      | Week 10     | COMPLETED    |
| W11    | Bharat Core Banking Highway & SAGA Governance      | Week 11      | Week 11     | COMPLETED    |
+--------+----------------------------------------------------+--------------+-------------+--------------+
| W12    | GitHub PR Guardian Webhook listener integration    | Week 12      | Roadmap     | IN PROGRESS  |
| W13    | Multi-tenant PostgreSQL database migration         | Week 13      | Roadmap     | PLANNED      |
| W14    | Firecracker / gVisor MicroVM containerization      | Week 14      | Roadmap     | PLANNED      |
| W15    | Comprehensive IEEE research publication bundle     | Week 15      | Roadmap     | IN PROGRESS  |
| W16    | Final Phase-3 Capstone Presentation & Defense Viva | Week 16      | Roadmap     | SCHEDULED    |
+--------+----------------------------------------------------+--------------+-------------+--------------+
```

---

## 2. Deep-Dive Slip Analysis & Architectural Adjustments

In accordance with **Rubric C6 (Progress vs Plan)** and honest senior software engineering principles, the table below documents the engineering slips encountered during Phase-2 implementation, the root causes, and the concrete mitigations executed:

| Slip ID | Component / Milestone | Planned Approach | Actual Implementation Reality | Root Cause & Technical Justification | Architectural Mitigation Executed |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **SLIP-01** | **Air-Gapped Local LLM Routing** | Run a live, local `qwen2.5-coder:7b` Ollama daemon on all evaluation workstations. | Graceful Dual-Engine router: Google Gemini 2.5 Flash live cloud inference, switching to simulated zero-network code synthesis when offline. | Running an unquantized 7B/8B model requires $> 8\text{ GB}$ dedicated GPU VRAM, which frequently caused out-of-memory crashes on student laptops. | Implemented an air-gapped privacy switch in `app/generation/llm_client.py` that routes to local Ollama when VRAM is available and gracefully activates a deterministic, zero-network code generator otherwise. |
| **SLIP-02** | **External Framework Dependencies (CrewAI & ADK)** | Install external `crewai` and `google-adk` PyPI distribution packages via `requirements.txt`. | Engineered clean, in-repo native Python architectural abstractions implementing the exact design patterns (`app/adk/callbacks.py` and `app/crew/flows.py`). | External pip packages brought heavy dependency conflicts, unstable API breaking changes across releases, and bloated container images by $> 1.8\text{ GB}$. | Authored the 8-hook callback lifecycle, agent coordinator, and stateful `@start`/`@listen` flows in native pure Python. This eliminates supply-chain risks and ensures sub-millisecond execution. |
| **SLIP-03** | **Windows Concurrent Qdrant File Locking** | Maintain persistent on-disk SQLite/Qdrant vector indexes across concurrent pytest workers. | Configured in-memory `:memory:` vector collection modes during test and verification runs. | Windows OS enforces strict mandatory file locking (`WinError 32`), causing access contention when parallel test suites hit on-disk vector stores simultaneously. | Added environment check (`PYTEST_CURRENT_TEST`); when detected, the system automatically runs Qdrant in ephemeral memory mode, eliminating locking bottlenecks. |
| **SLIP-04** | **Scope Expansion: Banking Governance** | Confine platform strictly to software engineering DevOps pull requests. | Expanded scope to include **Bharat Core Banking Highway** mounted at `/bank` with 15 dedicated endpoints. | Realized that the OWASP LLM01 prompt injection and lack of transactional atomicity represent an even more acute risk in financial execution than DevOps. | Architected a complete banking sub-application with SAGA compensations, Maker-Checker 4-eyes controls, and time-lock escrow for transfers $> ₹50,000$. |

---

## 3. Team Role Rotation & Phase-Wise Responsibility Matrix

To satisfy the mandatory university guideline from **Page 7 of the Course Handout** (*"Roles must rotate across phases. No student may limit their contribution to a single area"*), tasks are systematically rotated across Phase-1, Phase-2, and Phase-3:

```
+-------------------------------------------------------------------------------------------------------------+
|                                        PHASE-WISE ROLE ROTATION MATRIX                                      |
+-------------------+-------------------------------+------------------------+--------------------------------+
| Evaluation Phase  | Dhruv Jain                    | Hemant Goyal           | Rajat Yadav                    |
+-------------------+-------------------------------+------------------------+--------------------------------+
| **PHASE 1**       | Lead Architecture & FSM       | Pre-Execution Security | Agentic RAG & Qdrant Chunking  |
| (Foundations)     | (State Machine & PEAS)        | (Regex & Secret Engine)| (Dense MiniLM Vector Index)    |
+-------------------+-------------------------------+------------------------+--------------------------------+
| **PHASE 2**       | Banking Highway & SAGA Engine | AST Blast Radius Lead  | Frontend Dashboard & Voice STT |
| (Midsem Baseline) | (Time-Lock Escrow & Core Bank)| (Static AST Call Graph)| (Groq Whisper & SSE Telemetry) |
+-------------------+-------------------------------+------------------------+--------------------------------+
| **PHASE 3**       | MCP & Interoperability Lead   | Empirical Benchmarking | CI/CD Webhooks & Merkle Ledger |
| (Final Capstone)  | (Cursor/Claude JSON-RPC Bus)  | (V2 Held-Out & Attacks)| (GitHub Actions Pre-Merge Gate)|
+-------------------+-------------------------------+------------------------+--------------------------------+
```

---

## 4. Phase-3 Final Sprint Roadmap (Weeks 12 to 16)

The remaining sprints leading to the final capstone defense focus on cloud production readiness:
1. **Sprint 12 (GitHub PR Guardian Bot):** Complete webhook listener (`/webhook/github`) that posts automated AST blast-radius and slopsquatting annotations directly into GitHub Pull Request threads.
2. **Sprint 13 (Production PostgreSQL Migration):** Replace local SQLite session persistence with multi-tenant PostgreSQL managed via SQLAlchemy and Alembic migrations.
3. **Sprint 14 (Firecracker MicroVM Isolation):** Graduate the ephemeral subprocess test runner into hardware-isolated microVM sandboxing for untrusted third-party code execution.
4. **Sprint 15 (IEEE Conference Manuscript Finalization):** Finalize LaTeX publication draft titled *"Deterministic Pre-Execution Governance and Supply-Chain Firewalls for Autonomous AI Coding Agents"*.
5. **Sprint 16 (Final Capstone Defense & Viva):** Execute the 6-minute live presentation and demonstrate 100% test pass rate to the examination panel.
