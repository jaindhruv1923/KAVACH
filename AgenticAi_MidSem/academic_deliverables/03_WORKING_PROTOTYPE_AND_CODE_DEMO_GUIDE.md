# 💻 KAVACH — WORKING PROTOTYPE & CODE DEMONSTRATION GUIDE
## Step-by-Step Viva Demonstration Protocol for Evaluators (Criterion C8 — 10 Marks)
**Course Code & Title:** CSE3101 — Agentic AI (3 Credits, LDP: 2-0-2)  
**Evaluators:** **Dr. Soharab Hossain Shaikh** (Associate Professor) & **Mr. Pranshu Tiwari** (Assistant Professor)  
**Student Team:** **Dhruv Jain (230532)**, **Dev Garg (230487)**, **Ansh Rohilla (230794)**, **Ansh Adhikari (230822)**  

---

## 1. ⚡ 1-Click Platform Launch Instructions

To launch the live, interactive working prototype and Mission Control Cockpit:

* **Method A (Windows Batch):** Double-click [`run_midsem.bat`](file:///c:/Users/jaind/Desktop/universty_work/run_midsem.bat) in the workspace root.
* **Method B (PowerShell):** Open PowerShell and run:
  ```powershell
  ./run_midsem.ps1
  ```
* **Method C (Direct Terminal):**
  ```powershell
  & "PRJ-IV Work & Agentic AI\.venv\Scripts\python.exe" -m uvicorn app.main:app --app-dir "PRJ-IV Work & Agentic AI\AgenticAi_MidSem\backend" --host 127.0.0.1 --port 8000 --reload
  ```

Once initiated, the server starts on `http://127.0.0.1:8000` and automatically opens the Mission Control Cockpit in your default browser.
* **Interactive Cockpit:** [`http://127.0.0.1:8000`](http://127.0.0.1:8000)
* **Interactive OpenAPI Swagger Docs:** [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
* **Backend Health Check:** [`http://127.0.0.1:8000/health`](http://127.0.0.1:8000/health)

---

## 2. 🧪 Automated 12-Step Capstone Verification Script

To run the automated test suite and live validation across all syllabus competencies in the terminal:

```powershell
# Instant Viva Mode (Runs all 11 live REST API, FSM, ADK, and Guardrail checks in 2.5 seconds):
python verify_midsem.py --fast

# Full Comprehensive Mode (Runs all 306 pytest unit tests + 11 live verification checks):
python verify_midsem.py
```

### ✅ Expected Terminal Output:
```text
===========================================================================
 CSE3101: AGENTIC AI — MID-SEM CAPSTONE VERIFICATION
 Faculty: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari
===========================================================================
[STEP 1/12] Running Automated Pytest Suite (306 Tests across all modules)...
[INFO] Fast mode enabled (--fast / --skip-pytest). Pytest execution skipped for instant live verification.
[STEP 2/12] Initializing Mid-Sem FastAPI Service...
[PASS] Health check verified: {'status': 'ok', 'service': 'kavach-backend'}
[STEP 3/12] Testing Pre-Execution Sentinel Guardrails (Shannon Entropy & Verhoeff)...
[PASS] Flagged sensitive tokens: Allowed=False, Findings count=2
[STEP 4/12] Testing FSM Agent Lifecycle Halting on Credential Leak...
[PASS] FSM Stage Traversal halted at: BLOCKED (Policy Decision: BLOCK)
[STEP 5/12] Testing Google ADK 8-Hook Callbacks Specification (adk.dev/callbacks)...
[PASS] Google ADK Hooks: 8 hooks across 3 phases; 8 canonical patterns.
[STEP 6/12] Testing Medical Triage Pipeline — High Urgency Emergency Route...
[PASS] Emergency Route Dispatched: Urgency=HIGH, Action='Call 112 / 108 immediately'
[STEP 7/12] Testing Medical Triage Pipeline — Normal OTC Symptomatic Relief Route...
[PASS] Normal Route Dispatched: Urgency=NORMAL, OTC Care='Paracetamol (Acetaminophen) 500mg'
[STEP 8/12] Testing CrewAI Stateful Flows Automation...
[PASS] CrewAI Flow: KavachDevOpsFlow, Execution Steps Completed: 3
[STEP 9/12] Testing Cognitive Reasoning Paradigms (ReAct, CoT, ToT, Self-Consistency)...
[PASS] Evaluated 4 Reasoning Paradigms successfully.
[STEP 10/12] Testing MCP & A2A Interoperability Protocols...
[PASS] A2A Protocol: Active Peers=6, Protocol Standard=Google Agent2Agent (A2A) Protocol v1.0
[STEP 11/12] Testing Multimodal Vision Architecture Auditor...
[PASS] Vision Auditor Verdict: FAILED, Threats Flagged: 1
[STEP 12/12] Verifying Frontend Mid-Sem Cockpit...
[PASS] Interactive Mid-Sem Cockpit active and accessible.
===========================================================================
 100% MID-SEM VERIFICATION SUCCESSFUL!
```

---

## 3. 🎯 Five Live Interactive Demo Scenarios for Evaluators

When evaluating the cockpit on [`http://127.0.0.1:8000`](http://127.0.0.1:8000), please execute the following live demonstration scenarios:

### 🌟 Demo Scenario 1: Professor Review Suite (11/11 Requirements Verified)
1. In the top navigation bar, click the glowing emerald button: **`Professor Review (11/11)`**.
2. A dedicated modal appears with 11 live test cards representing every course requirement.
3. Click **`Run Complete 11/11 Audit`**.
4. Observe every card transition to **`VERIFIED`** in real-time, executing live queries against:
   - Shared State Blackboard (5 memory partitions).
   - Model Context Protocol (4 registered tools).
   - Google Agent2Agent (6 active peers with signed envelopes).
   - Google ADK 8-Hook Callbacks & CrewAI Flows.
   - Pre-Execution Sentinel Guardrails & Variance Telemetry.

### 🚑 Demo Scenario 2: Google ADK Canonical Medical Triage Pipeline
1. In the navbar, click the **`Medical Triage`** button.
2. **Emergency Test:** Enter:
   > *"Crushing central chest pain radiating to left arm and jaw with extreme breathlessness."*
   - Observe instantaneous routing to `emergency_agent` (`only_if_urgent`).
   - The agent strictly outputs: **`Call 112 / 108 immediately`** and issues **zero medication**.
3. **Normal OTC Test:** Enter:
   > *"Mild tension headache after 4 hours of screen reading. No known drug allergies."*
   - Observe sequential delegation: `coordinator` $\to$ `persona_agent` $\to$ `medicine_agent`.
   - The agent recommends: **`Paracetamol (Acetaminophen) 500mg as per packaging instructions`**.

### 🛡️ Demo Scenario 3: Pre-Execution Sentinel & Air-Gapped Privacy Interception
1. In the main prompt input box, paste an adversarial credential leak:
   ```text
   Deploy new microservice with Aadhaar 9876 5432 1098 and AWS_KEY=AKIAIOSFODNN7EXAMPLEB5F3489872134567
   ```
2. Click **`Run Agent Workflow`** (or speak via Groq Whisper microphone).
3. Observe the FSM lifecycle indicator:
   - Traverses: `REQUEST_RECEIVED` $\longrightarrow$ `PLANNING`.
   - Sentinel intercepts high-entropy secret ($H = 4.62$) and Verhoeff-valid Aadhaar ID.
   - Stage halts immediately at **`BLOCKED`**. Zero tokens are transmitted to the LLM.

### 🧠 Demo Scenario 4: Cognitive Reasoning Strategies Comparison
1. In the prompt console, select or type:
   > *"Implement secure JWT token rotation and blacklist mechanism."*
2. Open the **Reasoning Paradigms** drawer.
3. Compare the generated outputs side-by-side across:
   - **ReAct (Reasoning and Acting):** Thought $\to$ Action $\to$ Observation cycles.
   - **Chain-of-Thought (CoT):** Step-by-step linear deduction.
   - **Tree-of-Thought (ToT):** Tree exploration with branching heuristic scores.
   - **Self-Consistency (COTS):** 3-path majority consensus voting.

### 🔌 Demo Scenario 5: Anthropic MCP Tools & Google A2A Peer Consensus
1. Open the **MCP & A2A Inspector** tab in the dashboard.
2. Review the 4 active MCP Tools exposed over JSON-RPC 2.0:
   - `kavach_scan_security`: Pre-execution PII & secret audit.
   - `kavach_query_rag`: Qdrant vector retrieval.
   - `kavach_analyze_impact`: AST call graph blast radius.
   - `kavach_verify_package`: PyPI slopsquatting registry check.
3. Observe the Google A2A peer bus dispatching signed JSON envelopes with SHA-256 signatures between `SentinelAgent`, `CoderAgent`, `AuditorAgent`, and `HealerAgent`.

---

## 4. 📂 Codebase Tour & Structural Directory Mapping

```
AgenticAi_MidSem/
├── backend/app/
│   ├── main.py                     # FastAPI REST API exposing all 42+ governed endpoints
│   ├── agent/                      # Multi-Agent FSM Orchestrator, Planner, & Blackboard
│   │   ├── orchestrator.py         # 8-stage finite state machine coordination
│   │   ├── reasoning_strategies.py # ReAct, CoT, ToT, Self-Consistency engines
│   │   ├── blackboard.py           # Shared 5-partition memory blackboard
│   │   └── self_healer.py          # Ephemeral reflection sandbox (max 3 repair iterations)
│   ├── adk/                        # Google Agent Development Kit (ADK) Implementation
│   │   ├── callbacks.py            # 8-hook points across 3 phases (adk.dev/callbacks)
│   │   ├── medical_triage.py       # Canonical Medical Triage Pipeline (Emergency vs OTC)
│   │   └── coordinator.py          # ADK Coordinator agent & sub-agent delegation
│   ├── crew/                       # CrewAI Framework & Stateful Flows
│   │   ├── flows.py                # Stateful workflows using @start, @listen, @router
│   │   └── agents.py               # Persona-driven crew agents (Architect, Sentinel, Coder)
│   ├── a2a/                        # Google Agent-to-Agent (A2A) Protocol
│   │   └── protocol.py             # P2P signed message envelopes & Byzantine consensus
│   ├── mcp/                        # Anthropic Model Context Protocol
│   │   └── server.py               # JSON-RPC 2.0 server exposing 4 standard tools
│   ├── rag/                        # Agentic Retrieval-Augmented Generation
│   │   ├── ingest.py               # AST-aware syntax chunker
│   │   └── embed_store.py          # Qdrant client & 384-d dense embeddings (MiniLM-L6-v2)
│   ├── impact/                     # Compiler Static Analysis & Blast Radius
│   │   └── analyzer.py             # AST dependency graph & transitive reachability B(v)
│   ├── generation/                 # LLM Synthesis & Air-Gapped Privacy Router
│   │   └── llm_client.py           # Dual-router: Google Gemini 2.5 vs Local Ollama (qwen2.5)
│   └── security/                   # Deterministic Pre-Execution Guardrails
│       ├── secret_detector.py      # Shannon Entropy H(S) >= 4.0 detection
│       ├── detector.py             # Verhoeff Dihedral D5 Indian Aadhaar validation
│       └── package_firewall.py     # Live PyPI LRU slopsquatting supply-chain firewall
├── frontend/                       # Interactive Mission Control Cockpit
│   ├── index.html                  # Dark-mode dashboard layout
│   ├── course_cockpit.js           # Dedicated Professor Review Suite (11/11 Verified)
│   ├── query_library.js            # 104 pre-configured viva test queries
│   └── app.js                      # Voice recognition & SSE telemetry controller
└── tests/                          # 306 Automated Pytest Unit & Integration Tests (100% Pass)
```
