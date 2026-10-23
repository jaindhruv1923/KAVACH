# 🎬 KAVACH: Working Prototype & Code Demonstration Guide
## CSE3101: Agentic AI — Mid-Sem Viva & Code Walkthrough
### Instructors: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari

---

## ⚡ Quick 1-Click Launch
1. Double click `run_midsem.bat` (or execute `./run_midsem.ps1` in PowerShell).
2. The browser automatically opens the **Mission Control Dashboard** at:
   - **Interactive UI:** [`http://127.0.0.1:8000`](http://127.0.0.1:8000)
   - **OpenAPI Swagger Docs:** [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs)
   - **System Health:** [`http://127.0.0.1:8000/health`](http://127.0.0.1:8000/health)

---

## 🎯 6 Interactive Code Demos for Evaluators

### Demo 1: Professor Pranshu Tiwari Standardization Suite (11/11 Verified)
- **In UI:** Click the emerald green button in the top navbar: **`Professor Review (11/11)`**.
- **What opens:** An interactive modal testing all 11 evaluation requirements:
  1. *Hover Blackboard:* Live shared state across 5 partitions.
  2. *MCP Tools:* 4 live tool declarations (`kavach_scan_security`, `kavach_verify_packages`, `kavach_self_heal`, `kavach_generate_sbom`).
  3. *A2A Interop:* Agent2Agent consensus protocol envelopes.
  4. *ADK Patterns:* Google ADK 8-hook callbacks & 8 design patterns.
  5. *Guardrails & Variances:* Shannon entropy and prompt injection defense.
  6. *E2E Metrics:* Latency and cost benchmarks.
  7. *Cloud Deploy:* Docker, Cloud Run, and Kubernetes configurations.

### Demo 2: Medical Triage Multi-Agent Pipeline (Google ADK)
- **In UI:** Click the cyan button in the top navbar: **`Medical Triage`** (or go to the Evaluation tab).
- **Test Case A (Emergency Escalation):**
  - Click the preset *"Chest Pain Emergency"* or type: *"Crushing chest pain radiating to left arm with severe breathlessness"*.
  - Click **Run Medical Triage Pipeline**.
  - **Observation:** Urgency detected as `HIGH`. Dispatches `emergency_agent` (`only_if_urgent`). Recommends immediate Call 112 / 108. Strictly **NO medicine** is recommended.
- **Test Case B (Normal OTC Symptomatic Care):**
  - Click the preset *"Mild Headache"* or type: *"25-year-old male with mild tension headache after screen time"*.
  - Click **Run Medical Triage Pipeline**.
  - **Observation:** Urgency detected as `NORMAL`. Dispatches `persona_agent` $\to$ `medicine_agent` via Tavily Search tool. Recommends safe OTC Paracetamol 500mg with usage warnings.

### Demo 3: Pre-Execution Sentinel Intercepting Credentials (FSM Halting)
- **In UI:** Navigate to the **Console** tab.
- **Type or speak via Groq Whisper:**
  ```
  Deploy authentication microservice using AWS_SECRET_KEY=AKIAIOSFODNN7EXAMPLEB5F3489872134567 and Aadhaar 2345 6789 0123
  ```
- **Click Run Pipeline:**
  - Sentinel calculates Shannon entropy ($H = 4.62 > 4.0$) and flags Indian Aadhaar identifier.
  - FSM state machine transitions directly from `PLANNING` $\to$ **`BLOCKED`**.
  - Zero tokens are sent to external LLM APIs; credentials remain unexposed.

### Demo 4: CrewAI Stateful Flows Automation (`@start`, `@listen`)
- **Via cURL / Python:**
  ```bash
  curl -X POST http://127.0.0.1:8000/crew/flow \
       -H "Content-Type: application/json" \
       -d '{"prompt": "Deploy secure microservice"}'
  ```
- **Observation:** Executes stateful `@start` method in `KavachDevOpsFlow`, passing structured Pydantic state to `@listen` methods across sub-agents.

### Demo 5: Reasoning Strategies Comparator (ReAct, CoT, ToT, Self-Consistency)
- **Via cURL / Python:**
  ```bash
  curl -X POST http://127.0.0.1:8000/reasoning/strategies \
       -H "Content-Type: application/json" \
       -d '{"query": "Implement secure JWT rotation with blacklisting"}'
  ```
- **Observation:** Returns structured comparison table contrasting reasoning latencies, tree branches, and confidence scores.

### Demo 6: AST Blast-Radius & Change-Impact Graph
- **Via cURL / Python:**
  ```bash
  curl -X POST http://127.0.0.1:8000/impact \
       -H "Content-Type: application/json" \
       -d '{"target_file": "auth.py", "repo_path": "./demo_repo"}'
  ```
- **Observation:** Parses Python ASTs to extract caller-callee Directed Acyclic Graphs (DAG), outputting blast radius percentage and list of affected downstream files (`api.py`).

---

*Authored by Dhruv Jain · B.Tech CSE (AI & Data Science) · CSE3101 Agentic AI Mid-Sem Demo Guide*
