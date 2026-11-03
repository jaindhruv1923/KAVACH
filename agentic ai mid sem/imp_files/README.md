# KAVACH — Essential Source Code Showcase (`imp_files`)
**Course:** CSE3101 - Agentic AI (Academic Year 2026–27, 7th Semester)  
**Evaluators:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari | BML Munjal University  
**Lead Student Architect:** Dhruv Jain (Roll No. 230532)  

---

## What is in this Folder?
This folder (`c:\Users\jaind\OneDrive\Desktop\uni\Ageentic&PRJ-IV\imp_files`) contains a curated, clean copy of the core implementation files directly demanded by the **CSE3101 Agentic AI Course Handout**. 

All original files in `agentic_ai_midsem_work/` remain intact and unedited. This folder allows you to show any file or code snippet to the professors in 5 seconds without searching through deep repository directories.

---

## Directory Layout & Handout Mapping

```
imp_files/
├── 01_Google_ADK/                  # Handout Module 3 & 4: ADK Callbacks & Coordinator
│   ├── callbacks.py                # 8-Hook lifecycle interceptors (Agent, LLM, Tool)
│   ├── coordinator.py              # CoordinatorAgent managing sub-agents & delegation
│   ├── agent.py                    # Base LlmAgent & AgentLifecycleState machine
│   ├── workflow.py                 # AdkWorkflow runner chaining stages
│   └── memory.py                   # Session state & transient vs persistent memory
│
├── 02_CrewAI/                      # Handout Module 3: Workflow Automation with Flows
│   ├── flows.py                    # Pure-Python @start, @listen, @router & BaseFlow
│   ├── agents.py                   # Specialist swarm agents (Sentinel, AST, Synthesizer)
│   ├── tasks.py                    # Typed agent task schemas with expected outputs
│   └── crew_runner.py              # Swarm execution runner
│
├── 03_Guardrails_And_Security/     # Handout Module 2: Guardrails, Checksums & Firewalls
│   ├── detector.py                 # Pre-execution Sentinel gatekeeper & Unicode scrubber
│   ├── secret_detector.py          # Shannon Information Entropy (H >= 4.5 bits/char)
│   ├── package_firewall.py         # Aadhaar Dihedral D5 Verhoeff & PyPI Slopsquatting
│   ├── token_vault.py              # Zero-Knowledge DPDP TokenVault (UUID masking)
│   └── budget_guardrail.py         # Token & financial budget circuit breaker (4K tokens)
│
├── 04_Agentic_Design_Patterns/     # Handout Module 2: ReAct, GoT, LATS, FSM
│   ├── self_healer.py              # Bounded ReAct sandbox self-healing (N <= 3 cycles, 5s timeout)
│   ├── react_engine.py             # Thought -> Action -> Observation execution engine
│   ├── graph_of_thought.py         # Non-linear DAG reasoning with cycle detection
│   ├── lats_planner.py             # Language Agent Tree Search with Monte Carlo rollouts
│   ├── orchestrator.py             # 6-Stage Finite State Machine orchestrator
│   └── state.py                    # Typed Pydantic v2 WorkflowRun state model
│
├── 05_Protocols_MCP_And_A2A/       # Handout Module 4: Tools via MCP & A2A Interop
│   ├── mcp_server.py               # FastMCP JSON-RPC 2.0 tool server (4 core tools)
│   ├── mcp_client.py               # Client bridge connecting IDEs/agents to MCP
│   ├── a2a_protocol.py             # Google Agent-to-Agent message envelope & dispatcher
│   └── a2a_interop_bridge.py       # Interop bridge connecting Google ADK to CrewAI
│
├── 06_Bharat_Core_Banking/         # Handout Module 4 & 5: Autonomous Financial Highway
│   ├── banking_server.py           # FastAPI commercial core banking gateway (/bank)
│   ├── core_banking.py             # ACID SQLite banking core (accounts, ledger, escrow)
│   ├── kavach_banking_shield.py    # 5-Gate financial transaction shield & memo filter
│   └── advanced_banking_engines.py # Distributed SAGA Orchestrator, Maker-Checker, Basel III
│
└── 07_Observability_And_SSOT_Metrics/ # Handout Module 5: Provenance & Single Source of Truth
    ├── results_hub.py              # NIST FIPS 202 SHA3-512 Merkle DAG in SQLite WAL mode
    └── generate_metrics.py         # Automated code reality auditor (641 tests, 0.02ms latencies)
```

---

## 30-Second Examiner Quick-Reference

1. **"Show me your Google ADK callbacks":**
   * Open `imp_files/01_Google_ADK/callbacks.py` $\rightarrow$ Show lines 10–25 (the 8 lifecycle hooks).
2. **"Show me your CrewAI flows":**
   * Open `imp_files/02_CrewAI/flows.py` $\rightarrow$ Show `@start`, `@listen`, and `@router` decorators.
3. **"Show me the Aadhaar Checksum math":**
   * Open `imp_files/03_Guardrails_And_Security/package_firewall.py` $\rightarrow$ Show `validate_aadhaar_verhoeff()` using Dihedral $D_5$ group permutations.
4. **"Show me the Secret Scanner":**
   * Open `imp_files/03_Guardrails_And_Security/secret_detector.py` $\rightarrow$ Show `calculate_shannon_entropy()` with $H \ge 4.5$ boundary.
5. **"Show me Bounded ReAct Reflection":**
   * Open `imp_files/04_Agentic_Design_Patterns/self_healer.py` $\rightarrow$ Show `for attempt in range(1, 4):` and the 5.0-second CPU watchdog.
6. **"Show me MCP Tools and A2A Protocol":**
   * Open `imp_files/05_Protocols_MCP_And_A2A/mcp_server.py` $\rightarrow$ Show FastMCP `@mcp.tool()` declarations.
   * Open `imp_files/05_Protocols_MCP_And_A2A/a2a_protocol.py` $\rightarrow$ Show `A2AMessageEnvelope`.
7. **"Show me the Core Banking SAGA Rollback":**
   * Open `imp_files/06_Bharat_Core_Banking/advanced_banking_engines.py` $\rightarrow$ Show `DistributedSagaOrchestrator` backward compensation.
8. **"Show me how you verified your numbers":**
   * Open `imp_files/07_Observability_And_SSOT_Metrics/generate_metrics.py` $\rightarrow$ Show automated audit of 641 tests and 142 endpoints.

