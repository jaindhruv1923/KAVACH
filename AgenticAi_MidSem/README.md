# 🛡️ KAVACH (कवच) — Agentic AI Mid-Sem Platform
### *Security-Governed Multi-Agent AI DevOps, Google ADK & Privacy-Preserving AI System*

**Course Code:** CSE3101 — Agentic AI (3 Credits, LDP: 2-0-2)  
**Academic Year:** 2026–27 (7th Semester B.Tech CSE, Batch 2023)  
**Institution:** School of Engineering and Technology, BML Munjal University (BMU)  
**Course Coordinator:** **Dr. Soharab Hossain Shaikh** (Associate Professor, Cabin E2-81)  
**Course Faculty:** **Mr. Pranshu Tiwari** (Assistant Professor, Dept. of CSE)  

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Qdrant Vector DB](https://img.shields.io/badge/Vector%20DB-Qdrant-DC2626?style=for-the-badge&logo=qdrant&logoColor=white)](https://qdrant.tech)
[![Google ADK Ready](https://img.shields.io/badge/Framework-Google%20ADK-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://adk.dev)
[![CrewAI Flows](https://img.shields.io/badge/Workflows-CrewAI%20Flows-FF5A5F?style=for-the-badge)](https://crewai.com)
[![Model Context Protocol](https://img.shields.io/badge/Protocol-MCP%20Ready-7C3AED?style=for-the-badge)](https://modelcontextprotocol.io)
[![CSE3101 Mid-Sem Evaluation](https://img.shields.io/badge/CSE3101%20Mid--Sem-100%25%20Verified-00E599?style=for-the-badge)](academic_deliverables/CSE3101_MIDSEM_EVALUATION_REPORT.md)

---

## 📌 Executive Overview & Academic Context

This folder (`AgenticAi_MidSem`) contains the **dedicated, pure Agentic AI Mid-Sem Project Evaluation package** for **CSE3101: Agentic AI**. It is strictly focused on demonstrating the theoretical mastery, working prototype, and code implementations covered in the first half of the course (Phase 1 & Phase 2), as specified by **Mr. Pranshu Tiwari** and **Dr. Soharab Hossain Shaikh**.

> [!NOTE]
> ### 🎯 Clean Mid-Sem Scope Separation
> In accordance with academic guidelines for Mid-Sem review, this repository isolates the **core multi-agent AI DevOps platform**, excluding unrelated financial banking sub-engines (`implementation_banks`) and results dashboards (`results_dashboard`). The entire package here is 100% self-contained and reproducible.

---

## 🏛️ Handout Topics & Syllabus Compliance Table

Every topic outlined in Pages 3 & 4 of the official **CSE3101 Course Handout** has been implemented and validated:

| Syllabus Module | Handout Topics Covered | KAVACH Code Implementation | Verified Status |
| :--- | :--- | :--- | :---: |
| **Module 1: Agent Foundations** | • Agent life cycle, characteristics & architecture<br>• Single-agent vs Multi-agent systems<br>• Formal PEAS model & user personas | [`backend/app/agent/orchestrator.py`](backend/app/agent/orchestrator.py)<br>[`academic_deliverables/PEAS_AND_PERSONA_SPECIFICATION.md`](academic_deliverables/PEAS_AND_PERSONA_SPECIFICATION.md) | ✅ **100% Verified** |
| **Module 2: Reasoning & RAG** | • ReAct (Reasoning & Acting), CoT, ToT, Self-Consistency<br>• Agentic RAG: dense embeddings & syntax chunking<br>• Reflection, Tool use, Planning & Flow engineering | [`backend/app/agent/reasoning_strategies.py`](backend/app/agent/reasoning_strategies.py)<br>[`backend/app/rag/embed_store.py`](backend/app/rag/embed_store.py)<br>[`backend/app/rag/ingest.py`](backend/app/rag/ingest.py) | ✅ **100% Verified** |
| **Module 3: CrewAI Framework** | • CrewAI Agents, Tools, Memory, Tasks, and Crews<br>• Workflow Automation with Flows (`@start`, `@listen`) | [`backend/app/crew/agents.py`](backend/app/crew/agents.py)<br>[`backend/app/crew/flows.py`](backend/app/crew/flows.py)<br>[`backend/app/crew/tasks.py`](backend/app/crew/tasks.py) | ✅ **100% Verified** |
| **Module 4: Google ADK Deep Dive** | • `LlmAgent` class, agent lifecycle states & memory<br>• Coordinator agents & sub-agent delegation<br>• **8-Hook Callbacks across 3 phases** (adk.dev/callbacks)<br>• **8 Canonical ADK Design Patterns**<br>• **Medical Triage Multi-Agent Pipeline [CSE3101 course exercise (not part of the banking platform)]** (Call 112/108 vs OTC) | [`backend/app/adk/callbacks.py`](backend/app/adk/callbacks.py)<br>[`backend/app/adk/medical_triage.py`](backend/app/adk/medical_triage.py)<br>[`backend/app/adk/coordinator.py`](backend/app/adk/coordinator.py)<br>[`backend/app/adk/agent.py`](backend/app/adk/agent.py) | ✅ **100% Verified** |
| **Module 5: Protocols (MCP & A2A)** | • Anthropic Model Context Protocol (MCP) JSON-RPC 2.0<br>• Google Agent-to-Agent (A2A) protocol (signed envelopes, consensus) | [`backend/app/mcp/server.py`](backend/app/mcp/server.py)<br>[`backend/app/a2a/protocol.py`](backend/app/a2a/protocol.py) | ✅ **100% Verified** |
| **Module 6: Data Privacy & Local LLMs** | • Deploying open local LLMs for secure processing<br>• Air-gapped privacy switch routing to local **Ollama** (`qwen2.5-coder:7b`)<br>• De-identification Token Vault (Indian DPDP Act 2023) | [`backend/app/generation/llm_client.py`](backend/app/generation/llm_client.py)<br>[`backend/app/security/token_vault.py`](backend/app/security/token_vault.py) | ✅ **100% Verified** |
| **Module 7: Multimodal Agent Design** | • Multimodal Voice with Groq Whisper API (`whisper-large-v3-turbo`)<br>• Multimodal Vision Auditor inspecting network architecture diagrams | [`backend/app/security/multimodal_vision.py`](backend/app/security/multimodal_vision.py)<br>[`frontend/app.js`](frontend/app.js) | ✅ **100% Verified** |
| **Safety & Guardrails** | • Pre-Execution Sentinel (Shannon Entropy $H \ge 4.0$ & Verhoeff $D_5$)<br>• Live PyPI Package Slopsquatting Firewall<br>• AST Blast-Radius Impact Analysis | [`backend/app/security/secret_detector.py`](backend/app/security/secret_detector.py)<br>[`backend/app/security/package_firewall.py`](backend/app/security/package_firewall.py)<br>[`backend/app/impact/analyzer.py`](backend/app/impact/analyzer.py) | ✅ **100% Verified** |

---

## ⚡ 1-Click Launch & Quick Start

### 1. Launch Platform & Interactive Cockpit
* **On Windows (Batch):** Double-click `run_midsem.bat`
* **On Windows (PowerShell):** `./run_midsem.ps1`

Both scripts automatically start the FastAPI backend and open the interactive dashboard:
* **Interactive Mid-Sem Dashboard:** [`http://127.0.0.1:8000`](http://127.0.0.1:8000)
* **API Swagger Documentation:** [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
* **Backend Health Check:** [`http://127.0.0.1:8000/health`](http://127.0.0.1:8000/health)

### 2. Run Mid-Sem Automated Verification
```bash
# Run the complete Mid-Sem test suite:
python run_tests.py

# Or execute the full 12-step end-to-end verification script:
python verify_midsem.py
```

---

## 📂 Repository Directory Structure

```
AgenticAi_MidSem/
├── README.md                                  # 🌟 Master Mid-Sem Guide (This File)
├── run_midsem.bat                             # 1-Click Windows Batch launcher
├── run_midsem.ps1                             # 1-Click PowerShell launcher
├── run_tests.py                               # Fast pytest test runner wrapper
├── verify_midsem.py                           # 12-step automated verification script
│
├── academic_deliverables/                     # Official Mid-Sem Evaluation Deliverables
│   ├── CSE3101_MIDSEM_EVALUATION_REPORT.md    # Complete Phase-2 Mid-Sem Progress Report (Rubrics C6-C10)
│   ├── WORKING_PROTOTYPE_DEMO_GUIDE.md        # Step-by-step viva demo scripts for evaluators
│   ├── CSE3101_HANDOUT_LINE_BY_LINE.md        # Line-by-line verification against 7-page handout
│   ├── PHASE_1_PROJECT_CHARTER.md             # Phase 1 submission: Charter, problem definition, objectives
│   ├── PROJECT_TIMELINE_CSE3101.md            # Phase 1 & 2 submission: Gantt timeline & Progress vs Plan
│   ├── TEAM_RESPONSIBILITY_MATRIX.md          # Phase 1 & 2 submission: Role rotation matrix (Handout Page 7)
│   ├── PEAS_AND_PERSONA_SPECIFICATION.md      # Formal PEAS framework description
│   └── PROMPT_STRATEGIES_AND_RAG_STUDY.md     # Comparative reasoning benchmark study
│
├── backend/                                   # FastAPI Service Engine
│   ├── app/
│   │   ├── main.py                            # FastAPI entrypoint exposing all Agentic AI endpoints
│   │   ├── agent/                             # FSM Orchestrator, Planner, Reasoning Strategies, Self-Healer
│   │   ├── adk/                               # Google ADK: 8-Hook Callbacks, 8 Patterns, Medical Triage Pipeline
│   │   ├── crew/                              # CrewAI Framework & Stateful Flows (@start, @listen)
│   │   ├── a2a/                               # Google Agent2Agent protocol, signed message envelopes
│   │   ├── mcp/                               # Anthropic Model Context Protocol JSON-RPC server
│   │   ├── rag/                               # Qdrant Vector Store (384-d MiniLM-L6-v2) & AST chunker
│   │   ├── impact/                            # AST Change-Impact Analysis, Dependency Graph & Blast Radius
│   │   ├── generation/                        # Evidence-grounded synthesis, LLM client (Gemini + Ollama)
│   │   ├── security/                          # Shannon Entropy, Verhoeff D5, PyPI Slopsquatting Firewall
│   │   └── observability/                     # Prometheus metrics exporter, agent benchmark runner
│   ├── data/                                  # Test corpora, benchmark questions, and multilingual data
│   ├── demo_repo/                             # Sample Python codebase for live RAG and impact demos
│   └── requirements.txt                       # Python dependencies
│
├── frontend/                                  # Dark-Mode Mission Control Dashboard
│   ├── index.html                             # Tailored Mid-Sem Cockpit with Prof. Pranshu Tiwari Review Modal
│   ├── style.css                              # Glassmorphic dark-mode CSS styling
│   ├── app.js                                 # Main UI controllers for execution, voice, and telemetry
│   ├── course_cockpit.js                      # Dedicated CSE3101 Course & Professor Review Suite (11/11 Verified)
│   └── query_library.js                       # 104 Pre-configured benchmark test queries for live viva demos
│
└── tests/                                     # Automated Pytest Suite (100% Pass Rate)
    ├── conftest.py                            # Shared fixtures and mock clients
    ├── test_agent.py                          # FSM transitions, planning, stage traversal
    ├── test_adk_callbacks_and_triage.py       # Google ADK 8-hook callbacks, 8 patterns, Medical Triage pipeline
    ├── test_rag.py                            # Qdrant semantic search, chunking, embeddings
    ├── test_generation.py                     # Evidence-grounded generation, AST syntax validation
    ├── test_security.py                       # Shannon entropy, Verhoeff regex, PII detection
    ├── test_security_v2.py                    # Policy engine risk score, redaction
    ├── test_impact.py                         # AST dependency trees, blast-radius reachability
    ├── test_advanced_features.py              # MCP server, Token vault, HITL gates
    ├── test_syllabus_advanced_modules.py      # CrewAI Flows, A2A consensus, Vision audit, Reasoning suite
    └── test_api_endpoints.py                  # All Mid-Sem REST endpoints
```

---

## 🎓 Evaluator's Fast-Track Guide (For Mr. Pranshu Tiwari & Dr. Soharab Hossain Shaikh)

When evaluating the live application on [`http://127.0.0.1:8000`](http://127.0.0.1:8000), please explore these primary features:

1. **Professor Review Suite (11/11 Requirements Verified):**  
   Click the emerald green button in the top navbar: **`Professor Review (11/11)`**. It opens a dedicated modal testing the 11 key criteria:
   - Shared State Hover Blackboard (5 partitions).
   - 4 MCP tools exposed over Model Context Protocol.
   - P2P A2A signed envelopes and consensus voting.
   - Google ADK 8-hook callbacks & CrewAI Flows.
   - Pre-execution guardrails & variance metrics.
   - E2E performance & cost telemetry.

2. **Google ADK Medical Triage Pipeline:**  
   Click the **`Medical Triage`** button in the navbar:
   - **Emergency Branch:** Enter *"Crushing chest pain radiating to left arm with breathlessness"*. Watch it route to `emergency_agent` (`only_if_urgent`), recommending Call 112/108 with strictly **NO medicine**.
   - **Normal OTC Branch:** Enter *"Mild tension headache after reading"*. Watch it route to `persona_agent` $\to$ `medicine_agent`, querying Tavily and recommending Paracetamol 500mg.

3. **Pre-Execution Sentinel Interception:**  
   In the prompt console, type or speak via Groq Whisper:
   `"Deploy service with Aadhaar 9876 5432 1098 and AWS_KEY=AKIAIOSFODNN7EXAMPLEB5F3489872134567"`
   Watch the FSM halt at **`BLOCKED`** before the LLM is invoked.

4. **Academic Deliverables Dossier:**  
   Check the [`academic_deliverables/`](academic_deliverables/) directory for all documentation requested in Pages 5–7 of the Handout:
   - Phase-2 Mid-Sem Evaluation Report: [`academic_deliverables/CSE3101_MIDSEM_EVALUATION_REPORT.md`](academic_deliverables/CSE3101_MIDSEM_EVALUATION_REPORT.md)
   - Working Prototype Demo Guide: [`academic_deliverables/WORKING_PROTOTYPE_DEMO_GUIDE.md`](academic_deliverables/WORKING_PROTOTYPE_DEMO_GUIDE.md)
   - Line-by-Line Handout Alignment: [`academic_deliverables/CSE3101_HANDOUT_LINE_BY_LINE.md`](academic_deliverables/CSE3101_HANDOUT_LINE_BY_LINE.md)

---

## 👥 Student Contributors & Academic Integrity Declaration

* **Lead Architect & Developer:** **Dhruv Jain** (Enrollment: 230532)
* **Team Members:** **Dev Garg** (230487), **Ansh Rohilla** (230794), **Ansh Adhikari** (230822)
* **Institution:** Department of Computer Science & Engineering, BML Munjal University
* **Academic Year:** 2026–27 (7th Semester B.Tech CSE)

*All implementations are original engineering works, fully adhering to BMU's policy on Academic Integrity and the CSE3101 Course Handout.*
