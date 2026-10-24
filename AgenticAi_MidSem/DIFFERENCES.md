# Architectural Differences & Syllabus Mapping Dossier
**Project:** KAVACH Platform  
**Comparison:** `01_KAVACH_Platform` (MAIN Source of Truth) vs. `AgenticAi_MidSem` (COURSE PACKAGE)  
**Course:** CSE3101: Agentic AI — BML Munjal University  
**Evaluators:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  
**Student:** Dhruv Jain  

---

## 1. Intentional Separation Rationale

The two workspaces in this project serve distinct, intentional purposes:

| Dimension | `01_KAVACH_Platform` (MAIN) | `AgenticAi_MidSem` (COURSE PACKAGE) |
| :--- | :--- | :--- |
| **Primary Role** | Enterprise-grade AI DevOps Security Platform | Dedicated Academic Evaluation & Viva Defense Package |
| **Domain Focus** | Secure AI code synthesis, supply-chain firewall, banking transaction highway | Pure Agentic AI syllabus modules (Modules 1–7) |
| **Course Reference Exercise** | Excluded (strictly enterprise DevOps & banking) | Included: Google ADK Medical Triage Multi-Agent Pipeline |
| **Interactive Educational Aids** | Enterprise Metrics Cockpit & Blast Radius Graphs | Comic Cloud Visual Explainers (ELI5) for A2A and Callbacks |
| **External Dependencies** | Dual LLM routers (Gemini + local Ollama fallback), full vector RAG | Fast deterministic fallbacks for instant, zero-flake grading |
| **Verification Suite** | `verify_project.py` (Enterprise 278-test cyber suite) | `verify_midsem.py` (12/12 syllabus compliance checkpoints) |

---

## 2. CSE3101 Handout Module Mapping

The `AgenticAi_MidSem` package maps 1-to-1 to every module in the official **CSE3101 Course Handout**:

### Module 1: Agent Foundations & PEAS Modeling
- **Theoretical Base:** Agent lifecycle states, rational behavior, and environmental properties.
- **Code Reference:** [`backend/app/agent/orchestrator.py`](backend/app/agent/orchestrator.py) and [`academic_deliverables/PEAS_AND_PERSONA_SPECIFICATION.md`](academic_deliverables/PEAS_AND_PERSONA_SPECIFICATION.md).
- **Verification:** Unit tests verifying finite state transitions (`INITIALIZED` $\to$ `PLANNING` $\to$ `COMPLETED`).

### Module 2: Reasoning Paradigms & Agentic RAG
- **Theoretical Base:** ReAct (Reasoning + Acting), Chain-of-Thought (CoT), Tree-of-Thoughts (ToT), Self-Consistency.
- **Code Reference:** [`backend/app/agent/reasoning_strategies.py`](backend/app/agent/reasoning_strategies.py) and [`backend/app/rag/embed_store.py`](backend/app/rag/embed_store.py).
- **Verification:** Empirically evaluated on 32 ground-truth queries (Hit@1: 68.75%, Hit@5: 96.88%, MRR: 0.8281).

### Module 3: CrewAI Framework & Stateful Flows
- **Theoretical Base:** Autonomous agent personas, task assignment, memory buffers, and event-driven Flows.
- **Code Reference:** [`backend/app/crew/agents.py`](backend/app/crew/agents.py) and [`backend/app/crew/flows.py`](backend/app/crew/flows.py).
- **Verification:** `@start`, `@listen`, and `@router` decorators validated in `test_crewai_flows_stateful_automation`.

### Module 4: Google ADK (Agent Development Kit) Deep Dive
- **Theoretical Base:** `LlmAgent` lifecycle, `CoordinatorAgent` sub-agent delegation, and the **8-Hook Callback Architecture** across 3 phases (Agent, Model, Tool).
- **Code Reference:** [`backend/app/adk/agent.py`](backend/app/adk/agent.py), [`backend/app/adk/coordinator.py`](backend/app/adk/coordinator.py), and [`backend/app/adk/callbacks.py`](backend/app/adk/callbacks.py).
- **Verification:** All 8 hook points and 8 canonical design patterns passing in `test_adk_all_eight_hook_points`.

### Module 5: Cross-Framework Protocols (A2A & MCP)
- **Theoretical Base:** Google Agent-to-Agent (A2A) signed JSON-RPC 2.0 messages and Anthropic Model Context Protocol (MCP).
- **Code Reference:** [`backend/app/a2a/protocol.py`](backend/app/a2a/protocol.py) and [`backend/app/mcp/server.py`](backend/app/mcp/server.py).
- **Verification:** Cross-framework task delegation (ADK $\leftrightarrow$ CrewAI) validated under cryptographic signatures.

### Module 6: Privacy Guardrails & Local Inference
- **Theoretical Base:** Air-gapped processing, local LLM execution via Ollama, and DPDP Act compliance.
- **Code Reference:** [`backend/app/security/detector.py`](backend/app/security/detector.py), [`backend/app/security/verhoeff.py`](backend/app/security/verhoeff.py), and [`backend/app/security/token_vault.py`](backend/app/security/token_vault.py).
- **Verification:** 68-case empirical benchmark verifying 0.00% False Positive Rate on Indian Aadhaar numbers.

### Module 7: Multimodal Agent Design
- **Theoretical Base:** Multimodal Voice processing (Groq Whisper) and Vision auditing for network diagrams.
- **Code Reference:** [`backend/app/security/multimodal_vision.py`](backend/app/security/multimodal_vision.py) and [`frontend/app.js`](frontend/app.js).

---

## 3. Explicit Course Exercise Labeling: Medical Triage Pipeline

The Medical Triage Multi-Agent Pipeline located at:
[`backend/app/adk/medical_triage.py`](backend/app/adk/medical_triage.py)

is an **isolated academic exercise** built directly from the course professor's quiz problem statement and reference architecture:
- **Urgency == HIGH:** Triggers `emergency_agent` $\to$ automatically initiates emergency routing (112 / 108), advises safe waiting steps, and strictly forbids dispensing medicine.
- **Urgency == NORMAL:** Triggers `normal_flow` $\to$ invokes `persona_agent` for patient vitals followed by `medicine_agent` for Tavily OTC remedy discovery.

> [!IMPORTANT]
> **Strict Isolation Notice:**  
> The Medical Triage pipeline is purely a **CSE3101 course exercise (not part of the banking platform)**. It is excluded from the MAIN `01_KAVACH_Platform` production codebase and operates solely within `AgenticAi_MidSem` to demonstrate conditional callback routing and multi-agent safety gates.
