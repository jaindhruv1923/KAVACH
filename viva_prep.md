# KAVACH (कवच): Security-Governed Multi-Agent AI DevOps & Mission-Critical Banking Platform
## Comprehensive Viva Preparation, Course Handout Code Navigation & Master Defense Dossier

> **Target Audience:** Viva Examiners (Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari), Project-IV Lead (Prof. Anusha Chhabra), Technical Evaluators, and Viva Candidates  
> **Repository Root Path:** `C:\Users\jaind\OneDrive\Desktop\uni\Ageentic&PRJ-IV`  
> **Academic Context:** B.Tech CSE (AI & Data Science) · Academic Year 2026–27 · BML Munjal University, Gurugram  
> **Courses Covered:** 
> - **CSE3101 — Agentic AI** (3 Credits, LDP: 2-0-2) · Evaluators: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari
> - **Project-IV Capstone** (5 Credits) · Lead Coordinator: Prof. Anusha Chhabra
> **Core Author & Lead Architect:** Dhruv Jain (Enrollment No. 230532)  
> **Contributors & Mid-Term Team:** Hemant Goyal, Rajat Yadav  
> **Single Source of Truth Standard:** *Measured reality is the source of truth. All documentation figures match code measurements directly verified by automated audit scripts.*

---

## Master Table of Contents

1. [Executive Summary & The Core Problem](#1-executive-summary--the-core-problem)
2. [Master Directory Structure & Repository Anatomy](#2-master-directory-structure--repository-anatomy)
3. [MASTER COURSE HANDOUT (CSE3101) TOPIC-BY-TOPIC CODE & NAVIGATION MAP](#3-master-course-handout-cse3101-topic-by-topic-code--navigation-map)
   - [3.1 Prerequisite Review & Evolution to Autonomous Agents](#31-prerequisite-review--evolution-to-autonomous-agents)
   - [3.2 Reasoning & Prompting Strategies (ReAct, CoT, ToT, GoT, LATS)](#32-reasoning--prompting-strategies-react-cot-tot-got-lats)
   - [3.3 Agentic Design Patterns (Reflection, Planning, Tool Use, Flows)](#33-agentic-design-patterns-reflection-planning-tool-use-flows)
   - [3.4 Agentic Retrieval-Augmented Generation (Code RAG & Qdrant)](#34-agentic-retrieval-augmented-generation-code-rag--qdrant)
   - [3.5 CrewAI Framework Deep Dive (Agents, Tasks, Memory, Flows)](#35-crewai-framework-deep-dive-agents-tasks-memory-flows)
   - [3.6 Google Agent Development Kit (ADK) Deep Dive (8-Hook Callbacks, Coordinator, Memory)](#36-google-agent-development-kit-adk-deep-dive-8-hook-callbacks-coordinator-memory)
   - [3.7 Emerging Protocols (Model Context Protocol / MCP & Agent-to-Agent / A2A)](#37-emerging-protocols-model-context-protocol--mcp--agent-to-agent--a2a)
   - [3.8 Guardrails, Cyber Safety & Package Firewall (Slopsquatting, Verhoeff, Entropy)](#38-guardrails-cyber-safety--package-firewall-slopsquatting-verhoeff-entropy)
   - [3.9 Data Security & Privacy (Air-Gapped Local LLM vs Public Cloud)](#39-data-security--privacy-air-gapped-local-llm-vs-public-cloud)
   - [3.10 Multimodal Agent Capabilities (Whisper v3 Audio & Visual Injections)](#310-multimodal-agent-capabilities-whisper-v3-audio--visual-injections)
   - [3.11 Agent Evaluation & Benchmarking (Grounded Metrics, Red-Team 19 Vectors)](#311-agent-evaluation--benchmarking-grounded-metrics-red-team-19-vectors)
   - [3.12 Monitoring & Observability (Telemetry, SSE, SHA3-512 Merkle Ledger)](#312-monitoring--observability-telemetry-sse-sha3-512-merkle-ledger)
   - [3.13 Production Deployment (Docker, Kubernetes, Render, 1-Click Launchers)](#313-production-deployment-docker-kubernetes-render-1-click-launchers)
   - [3.14 Industry Domains & Use Cases (Bharat Core Banking SAGA ACID & DevOps)](#314-industry-domains--use-cases-bharat-core-banking-saga-acid--devops)
4. [TWO-WAY NAVIGATION GUIDE (HOW TO DEMONSTRATE & SHOW THE CODE)](#4-two-way-navigation-guide-how-to-demonstrate--show-the-code)
   - [4.1 Path A: Inside the Inbuilt Web IDE (`</> Inbuilt IDE`)](#41-path-a-inside-the-inbuilt-web-ide--inbuilt-ide)
   - [4.2 Path B: Directly in VS Code (Shortcuts, File Paths & Highlighting)](#42-path-b-directly-in-vs-code-shortcuts-file-paths--highlighting)
5. [The 9 Defensive Stages & Subsystems (Detailed Engineering Architecture)](#5-the-9-defensive-stages--subsystems-detailed-engineering-architecture)
6. [Single Source of Truth (SSOT) Measured Metrics & Verification Reality](#6-single-source-of-truth-ssot-measured-metrics--verification-reality)
7. [Official University Evaluation Matrix (CSE3101: 30 Marks) & Student Submissions](#7-official-university-evaluation-matrix-cse3101-30-marks--student-submissions)
8. [Faculty Examiner Viva Defense Script (Dr. Shaikh & Mr. Tiwari)](#8-faculty-examiner-viva-defense-script-dr-shaikh--mr-tiwari)
9. [Operational Guide: How to Run, Test, and Verify Everything](#9-operational-guide-how-to-run-test-and-verify-everything)
10. [Deliberately Deferred Items, Scope Discipline & Phase 3 Roadmap](#10-deliberately-deferred-items-scope-discipline--phase-3-roadmap)

---

## 1. Executive Summary & The Core Problem

### 1.1 The Vulnerability of Naive Autonomous Coding Agents
Modern autonomous coding agents (such as Devin, SWE-agent, AutoPR, and Copilot Workspace) can decompose complex developer requests, inspect repository files, query vector databases, modify code across multiple directories, run continuous integration (CI) tests, and issue pull requests.

However, deploying unconstrained autonomous agents directly into production codebases and critical infrastructure creates catastrophic failure modes:
1. **Supply-Chain Poisoning & Slopsquatting:** Autonomous agents hallucinate non-existent external dependencies (e.g., `import fastapi_jwt_vault_security`) at an empirical rate of **19.7%** (Spracklen et al., USENIX Security 2025). Adversaries weaponize this behavior by registering these hallucinated package names on public package indices (PyPI, npm), achieving zero-click remote code execution when the agent executes its CI/CD pipeline.
2. **Credential & PII Exfiltration:** Agents inadvertently send unredacted corporate API keys, database credentials, AWS secrets, and Indian national identifiers (Aadhaar, PAN, phone numbers) to external, third-party model inference APIs (e.g., OpenAI, Anthropic), violating the statutory mandates of the **Digital Personal Data Protection Act, 2023 (DPDP Act)** and the **EU AI Act (2024/1689)**.
3. **Unbounded Blast Radius:** Without whole-repository Abstract Syntax Tree (AST) topological awareness, an agent modifying a peripheral helper function may silently break critical downstream services across module boundaries.
4. **Infinite Non-Convergent Debugging Loops:** When tests fail, naive agents enter unbounded reasoning oscillations, burning thousands of dollars in token costs without converging on valid code.
5. **Adversarial Prompt Injection & Trojan Source:** Hidden malicious instructions inside repository markdown files, commit messages, or transaction descriptions hijack the agent's reasoning layer (OWASP LLM01:2025).

### 1.2 The KAVACH Solution
**KAVACH (कवच)** is an enterprise-grade, deterministic, security-governed multi-agent AI DevOps platform, integrated with an industrial-strength financial transaction shield (**Bharat Commercial Core Banking System**) and a cryptographic audit cockpit (**Unified Results Hub**).

Rather than relying on fragile system prompt instructions (*"Please don't leak secrets or hallucinate packages"*), KAVACH enforces **deterministic, multi-stage finite-state machine (FSM) guardrails, Shannon entropy detection, Verhoeff checksum validation, AST dependency graph reachability analysis, live PyPI registry probing, and zero-knowledge tokenization** before any code is dispatched, executed, or committed.

```
[Developer Request (Spoken or Typed)]
                     │
                     ▼
┌────────────────────────────────────────────────────────┐
│               KAVACH GOVERNANCE LAYER                  │
│                                                        │
│  1. Sentinel Pre-Execution Gatekeeper                  │
│     - Shannon Entropy (H > 4.5) & Verhoeff Checksum   │
│     - Zero-Knowledge Token Vault (UUID Masking)       │
│                                                        │
│  2. Dual-Engine Privacy Routing                        │
│     - Public/Clean: Cloud LLM (Gemini 2.5 / Groq)      │
│     - Sensitive/Air-Gapped: Local Ollama (Qwen-Coder) │
│                                                        │
│  3. Agentic Code RAG (Qdrant Vector DB)               │
│     - 384-dim all-MiniLM-L6-v2 Embeddings (cos > 0.70)│
│                                                        │
│  4. AST Dependency Graph & Blast-Radius Engine         │
│     - Static Call-Graph Reachability B(v) Analysis     │
│                                                        │
│  5. Supply-Chain Slopsquatting Firewall                │
│     - AST Import Interception & Live PyPI LRU Probing  │
│                                                        │
│  6. Bounded ReAct Sandbox & Self-Healing Loop          │
│     - Subprocess Pytest Watchdog (Max N=3 cycles)      │
│                                                        │
│  7. Mission-Critical Banking Shield (Bharat Bank)     │
│     - RBI HITL Quarantine (> ₹50,000) & SAGA ACID Roll │
│                                                        │
│  8. Tamper-Evident Cryptographic Merkle Ledger        │
│     - NIST FIPS 202 SHA3-512 Audit Chain               │
└────────────────────────┬───────────────────────────────┘
                         │
                         ▼
        [Verified, Safe, Governed Patch / Execution]
```

---

## 2. Master Directory Structure & Repository Anatomy

The repository is organized into two primary, zero-clutter top-level workspaces:

```
Ageentic&PRJ-IV/
│
├── 📂 "agentic ai mid sem"/                      <-- CSE3101 Agentic AI Mid-Semester Workspace
│   ├── 📂 kavach_platform/                        <-- Unified Platform Codebase & Server (Port 8000)
│   ├── 📂 imp_files/                              <-- 7 Curated Handout Code Modules for Inbuilt IDE
│   │   ├── 📂 01_Google_ADK/                      <-- Callbacks, Coordinator, Memory, Workflow, Triage
│   │   ├── 📂 02_CrewAI/                          <-- Stateful Flows, Agents, Tasks, Crew Runner
│   │   ├── 📂 03_Guardrails_And_Security/         <-- Verhoeff D5, Entropy, Token Vault, Package Firewall
│   │   ├── 📂 04_Agentic_Design_Patterns/         <-- ReAct Engine, Self-Healer, GoT, LATS Planner
│   │   ├── 📂 05_Protocols_MCP_And_A2A/           <-- FastMCP Server/Client, A2A Interop Bridge
│   │   ├── 📂 06_Bharat_Core_Banking/             <-- SAGA Orchestrator, Banking Server, Core Shield
│   │   └── 📂 07_Observability_And_SSOT_Metrics/  <-- Benchmark Generator, Results Hub, Merkle Ledger
│   ├── 📂 documentation_and_reports/              <-- All Academic Reports, Deliverables & Presentations
│   │   ├── 📂 01_Submission_Documents_And_Reports/
│   │   ├── 📂 02_Presentations_And_Viva_Defense/
│   │   ├── 📂 03_Architecture_And_Flowcharts/
│   │   ├── 📂 04_Evaluation_And_Research_Papers/
│   │   └── 📦 Archived_Legacy_Materials.zip
│   ├── 📜 run_midsem.bat                          <-- 1-Click Platform Launcher (Port 8000)
│   ├── 📜 run_live_cloud_tunnel.bat               <-- 1-Click Public Cloud Tunnel
│   └── 📜 README.md                               <-- MidSem Technical & Architecture Overview
│
└── 📂 "PRJ-IV &AgenticAi Final Work"/             <-- PRJ-IV & Agentic AI Final Capstone Workspace
    ├── 📂 kavach_platform/                        <-- Master KAVACH Security Gateway (Port 8001)
    ├── 📂 bharat_core_banking/                    <-- Real-time Core Banking Web Portal (Port 8002)
    ├── 📂 live_agent_swarm/                       <-- 6-Agent Swarm Simulation Engine (Port 8003)
    ├── 📂 documentation_and_reports/              <-- Presentations, Progress Reports & Course Rubrics
    │   ├── 📂 01_Presentations_And_Reports/       <-- Master PPTX (16 Slides), Defense Outline & Video Scripts
    │   └── 📂 02_Course_Handouts_And_Rubrics/     <-- Rubric Alignment, Handout Traceability & Viva Questions
    ├── 📂 adapters/                               <-- Multi-Model Protocol Adapters
    ├── 📂 scripts/                                <-- Automated Validation & Testing Suites
    ├── 📜 run_all_services.bat                    <-- 1-Click Master Launcher (Ports 8001, 8002, 8003)
    ├── 📜 run_live_cloud_tunnel.bat               <-- 1-Click Public Live Cloud Tunnel
    └── 📜 README.md                               <-- PRJ-IV Architecture & Mathematical Specification
```

---

## 3. MASTER COURSE HANDOUT (CSE3101) TOPIC-BY-TOPIC CODE & NAVIGATION MAP

This section provides the **exact, line-by-line mapping** of every single topic listed in the official **BML Munjal University CSE3101 Agentic AI Course Handout** to the physical codebase.

### 3.1 Prerequisite Review & Evolution to Autonomous Agents
* **Handout Syllabus:** Review of Transformers, LLM Training & Embeddings, Evolution from LLMs to Autonomous AI Agents, Agent Characteristics, Life Cycle, Single vs. Multi-Agent Systems.
* **Mapped Course Outcome:** `CO1`
* **Where We Implemented It in Code:**
  * `agentic ai mid sem/imp_files/01_Google_ADK/agent.py` (Lines 15–85: `LlmAgent` class with lifecycle stages: `INITIALIZING`, `THINKING`, `ACTING`, `OBSERVING`, `TERMINATED`).
  * `agentic ai mid sem/imp_files/04_Agentic_Design_Patterns/state.py` (Lines 20–75: `AgentExecutionState` dataclass tracking invocation IDs, session context, and transitions).
  * `agentic ai mid sem/kavach_platform/01_KAVACH_Platform/backend/app/agent/orchestrator.py` (Lines 45–160: 6-stage finite-state machine governing single vs. multi-agent flow).
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `state.py` or `orchestrator.py`, press `Enter`.
* **Inbuilt IDE Navigation:** Click `[</> Inbuilt IDE]` $ightarrow$ Category filter `Design Patterns` $ightarrow$ select `state.py` / `orchestrator.py`.
* **Viva Explanation to Dr. Shaikh & Mr. Tiwari:**
  > *"Sir, we define the agent lifecycle not as an uncontrolled while-loop, but as an explicit Finite State Machine in `state.py`. We initialize an immutable dataclass containing the PEAS parameters (Performance measure: zero-security-leakage, Environment: Git repository & Bharat Bank, Actuators: AST patch engine, Sensors: static code parser). The lifecycle transitions deterministically from `REQUEST_RECEIVED` to `PLANNING`, `SECURITY_CHECK`, `CONTEXT_RETRIEVAL`, and `GENERATION`."*

---

### 3.2 Reasoning & Prompting Strategies (ReAct, CoT, ToT, GoT, LATS)
* **Handout Syllabus:** Reasoning & Prompting Strategies: ReAct (Reasoning + Acting) integrating reasoning and tool use; Chain-of-Thought (CoT), Tree-of-Thought (ToT), Graph-of-Thought (GoT), Language Agent Tree Search (LATS), Self-consistency.
* **Mapped Course Outcome:** `CO1, CO2, CO3`
* **Where We Implemented It in Code:**
  * **ReAct Engine:** `agentic ai mid sem/imp_files/04_Agentic_Design_Patterns/react_engine.py` (Lines 30–120: `execute_react_cycle()`, regex action extraction `Action:\s*(\w+)`, tool dispatch, and observation feedback).
  * **Graph-of-Thought (GoT):** `agentic ai mid sem/imp_files/04_Agentic_Design_Patterns/graph_of_thought.py` (Lines 25–115: `GraphOfThoughts` DAG reasoner implementing Kahn's topological sort theorem to eliminate cyclic reasoning deadlocks).
  * **Language Agent Tree Search (LATS):** `agentic ai mid sem/imp_files/04_Agentic_Design_Patterns/lats_planner.py` (Lines 40–145: Monte Carlo Tree Search rollouts, node expansion, heuristic backpropagation).
  * **Autonomous Self-Healer:** `agentic ai mid sem/imp_files/04_Agentic_Design_Patterns/self_healer.py` (Lines 35–130: Bounded reflection loop capped at $N \le 3$ cycles).
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `react_engine.py` or `graph_of_thought.py`, press `Ctrl+G` line 35.
* **Inbuilt IDE Navigation:** Click `[</> Inbuilt IDE]` $ightarrow$ Category `Design Patterns` $ightarrow$ Click `self_healer.py` or `react_engine.py` $ightarrow$ View live ASCII Execution Flowchart on the right panel.
* **Viva Defense Answer:**
  > *"Sir, standard Chain-of-Thought is purely linear. In complex code repair, errors branch unpredictably. In `graph_of_thought.py`, we implemented a Directed Acyclic Graph where thoughts can fork into parallel sub-analyses and merge via consensus nodes. In `react_engine.py`, we implement pure ReAct: the agent emits a Thought, selects a registered Tool Action, executes it in a sandboxed subprocess, and appends the Observation back into context before deciding the next step."*

---

### 3.3 Agentic Design Patterns (Reflection, Planning, Tool Use, Flows)
* **Handout Syllabus:** Agentic Design Patterns: Reflection, Dynamic Tool use, Planning, Multi-agent workflows; Flow Engineering in agentic systems.
* **Mapped Course Outcome:** `CO1, CO2`
* **Where We Implemented It in Code:**
  * **Bounded Reflection:** `agentic ai mid sem/imp_files/04_Agentic_Design_Patterns/self_healer.py` (Lines 55–98: `heal_code_patch()`, subprocess pytest execution, capture of stderr/traceback, reflection prompt synthesis, re-verification).
  * **Dynamic Tool Context:** `agentic ai mid sem/imp_files/01_Google_ADK/agent.py` (Lines 40–95: `ToolContext` passing execution credentials, session state delta, and authorization tokens to tools).
  * **Flow Engineering:** `agentic ai mid sem/imp_files/02_CrewAI/flows.py` (Lines 25–105: Event-driven step progression with `@start` and `@listen` decorators).
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `self_healer.py`, go to Line 55 (`def autonomous_self_heal`).
* **Inbuilt IDE Navigation:** Click `[</> Inbuilt IDE]` $ightarrow$ Chip `[Act Loop Sandbox (Max 3 R]` $ightarrow$ Code jumps directly to `self_healer.py:55` and highlights the self-healing while-loop.
* **Viva Defense Answer:**
  > *"Sir, if you look at line 55 of `self_healer.py`, notice our loop termination condition: `while attempt < MAX_REFLECTIONS` where `MAX_REFLECTIONS = 3`. Without this mathematical bound, reflection agents enter infinite loops burning API tokens when encountering stubborn test failures. Here, if the 3rd patch fails, it gracefully yields a `NEEDS_REVIEW` escalation to the human engineer."*

---

### 3.4 Agentic Retrieval-Augmented Generation (Code RAG & Qdrant)
* **Handout Syllabus:** Agentic Retrieval-Augmented Generation (RAG): Designing and implementing conversational AI workflows with retrieval-augmented reasoning.
* **Mapped Course Outcome:** `CO1, CO2, CO3`
* **Where We Implemented It in Code:**
  * **AST Chunking:** `agentic ai mid sem/kavach_platform/01_KAVACH_Platform/backend/app/rag/ingest.py` (Lines 35–110: `ast.walk` segmenting code files into 1200-char blocks at class/def boundaries).
  * **Vector Embeddings & Qdrant:** `agentic ai mid sem/kavach_platform/01_KAVACH_Platform/backend/app/rag/embed_store.py` (Lines 45–130: 384-dimensional dense vectors using `all-MiniLM-L6-v2`, HNSW index).
  * **Cosine Gating:** `agentic ai mid sem/kavach_platform/01_KAVACH_Platform/backend/app/agent/orchestrator.py` (Lines 95–125: Cosine similarity threshold $\ge 0.70$).
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `embed_store.py`, press `Ctrl+G` line 45.
* **Inbuilt IDE Navigation:** Click `[</> Inbuilt IDE]` $ightarrow$ Category `Design Patterns` $ightarrow$ select `orchestrator.py` $ightarrow$ Stage 3 `CONTEXT_RETRIEVAL`.
* **Viva Defense Answer:**
  > *"Sir, standard naive RAG chunks text arbitrarily at character counts (e.g. every 500 characters), which slices Python functions in half and ruins AST parsing. Our `ingest.py` parses the AST tree first, finding function boundaries (`FunctionDef`, `AsyncFunctionDef`, `ClassDef`), and chunks code semantically so that each retrieved snippet is syntactically coherent."*

---

### 3.5 CrewAI Framework Deep Dive (Agents, Tasks, Memory, Flows)
* **Handout Syllabus:** CrewAI Framework Deep Dive: Architecture and core components, including agents, tools, memory, tasks, and crews. Workflow Automation with Flows: Designing, orchestrating, and automating agentic workflows using Flows.
* **Mapped Course Outcome:** `CO1, CO2, CO3`
* **Where We Implemented It in Code:**
  * **Stateful Flows (`@start`, `@listen`):** `agentic ai mid sem/imp_files/02_CrewAI/flows.py` (Lines 25–115: `FraudInvestigationFlow`, `@start` state instantiation, `@listen` event-driven fan-out).
  * **CrewAI Multi-Agent Team:** `agentic ai mid sem/imp_files/02_CrewAI/agents.py` (Lines 20–95: `DevSecOpsAgent`, `SecurityAuditorAgent`, `CodeSynthesizerAgent`, `QAEngineerAgent`).
  * **Task Delegation & Runner:** `agentic ai mid sem/imp_files/02_CrewAI/tasks.py` and `crew_runner.py` (Lines 15–80: Sequential vs. Hierarchical crew execution).
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `flows.py`, go to Line 32 (`class FraudInvestigationFlow`).
* **Inbuilt IDE Navigation:** Click `[</> Inbuilt IDE]` $ightarrow$ Category `CrewAI` $ightarrow$ click `flows.py`. The ASCII execution pipeline displays the `@start` $ightarrow$ Worker/Policy `@listen` $ightarrow$ Aggregation Stage.
* **Viva Defense Answer:**
  > *"Sir, if you look at line 32 of `flows.py`, we implement CrewAI Stateful Flows. Instead of a synchronous procedural call where agent A blocks while waiting for agent B, we use event signals. `@start` instantiates an immutable `FlowState`. Downstream policy agents subscribe with `@listen('investigation_started')`, executing concurrently. Finally, `finalize_verdict_and_audit()` joins the branches."*

---

### 3.6 Google Agent Development Kit (ADK) Deep Dive (8-Hook Callbacks, Coordinator, Memory)
* **Handout Syllabus:** Google ADK Deep Dive: Architecture, core components, and development workflow. Agent Fundamentals: Agent (`LlmAgent`) class, agent lifecycle, and capabilities. Tools and Function Calling, State, Sessions, and Memory. Event-Driven Architecture, Agent Orchestration (Coordinator agents, sub-agents, task delegation), Callbacks (Model, agent, and tool callbacks).
* **Mapped Course Outcome:** `CO1, CO2, CO3`
* **Where We Implemented It in Code:**
  * **The 8 Canonical ADK Callbacks:** `agentic ai mid sem/imp_files/01_Google_ADK/callbacks.py` (Lines 35–140:
    1. `before_agent_callback`
    2. `after_agent_callback`
    3. `before_model_callback`
    4. `after_model_callback`
    5. `on_model_error_callback`
    6. `before_tool_callback`
    7. `after_tool_callback`
    8. `on_tool_error_callback`).
  * **ADK Coordinator & Sub-Agents:** `agentic ai mid sem/imp_files/01_Google_ADK/coordinator.py` (Lines 25–95: Hierarchical coordinator delegating to triage and security agents).
  * **ADK Memory & Session State:** `agentic ai mid sem/imp_files/01_Google_ADK/memory.py` (Lines 20–75: Transient state vs. Persistent long-term memory store).
  * **ADK Medical Triage Application:** `agentic ai mid sem/imp_files/01_Google_ADK/medical_triage.py` (Lines 30–110: Real-world emergency triage workflow implementing Google ADK).
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `callbacks.py`, press `Ctrl+G` line 35 (`def get_adk_callbacks`).
* **Inbuilt IDE Navigation:** Click `[</> Inbuilt IDE]` $ightarrow$ Category `Google ADK` $ightarrow$ Click `callbacks.py`.
* **Viva Defense Answer:**
  > *"Sir, Google ADK specifies 3 execution phases: Agent Lifecycle, LLM Interaction, and Tool Execution. In `callbacks.py` at line 35, our `get_adk_callbacks()` function returns handlers for all 8 lifecycle interceptors. In `before_model_callback`, we intercept the prompt and run high-entropy credential detection. In `before_tool_callback`, we verify the AST sandbox permissions. If a policy violation occurs, the callback aborts execution immediately without touching the model."*

---

### 3.7 Emerging Protocols (Model Context Protocol / MCP & Agent-to-Agent / A2A)
* **Handout Syllabus:** Model Context Protocol (MCP): Agent-to-tool communication and tool interoperability. Agent-to-Agent (A2A) Protocol: Communication, collaboration, and coordination among AI agents.
* **Mapped Course Outcome:** `CO1, CO2, CO3`
* **Where We Implemented It in Code:**
  * **FastMCP Server:** `agentic ai mid sem/imp_files/05_Protocols_MCP_And_A2A/mcp_server.py` (Lines 25–110: Exposes `kavach_scan_code`, `kavach_verify_pypi`, `kavach_check_aadhaar` as standard MCP tools over JSON-RPC 2.0).
  * **MCP Client:** `agentic ai mid sem/imp_files/05_Protocols_MCP_And_A2A/mcp_client.py` (Lines 20–85: Dynamic tool discovery and schema negotiation).
  * **A2A Interop Protocol:** `agentic ai mid sem/imp_files/05_Protocols_MCP_And_A2A/a2a_protocol.py` and `a2a_interop_bridge.py` (Lines 30–120: Standardized JSON envelope containing `sender_id`, `receiver_id`, `conversation_id`, `action_intent`, and SHA3-512 cryptographic payload hash).
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `mcp_server.py`, press `Enter`.
* **Inbuilt IDE Navigation:** Click `[</> Inbuilt IDE]` $ightarrow$ Category `Protocols` $ightarrow$ select `mcp_server.py` or `a2a_protocol.py`.
* **Viva Defense Answer:**
  > *"Sir, rather than writing proprietary agent APIs, we adopted the open Anthropic Model Context Protocol (MCP). In `mcp_server.py`, our FastMCP server exposes security guardrails as tools. Any external IDE, Claude Desktop, or autonomous agent can discover our tools dynamically via JSON-RPC. For inter-agent messaging, `a2a_protocol.py` implements Google's Agent2Agent specification, ensuring tamper-evident message envelopes."*

---

### 3.8 Guardrails, Cyber Safety & Package Firewall (Slopsquatting, Verhoeff, Entropy)
* **Handout Syllabus:** Guardrails and Safety: Designing secure, reliable, and responsible agentic applications. Data Security and Privacy: Deploying open local LLMs for secure and privacy-preserving AI applications.
* **Mapped Course Outcome:** `CO2, CO5`
* **Where We Implemented It in Code:**
  * **Dihedral Group $D_5$ Verhoeff Checksum:** `agentic ai mid sem/imp_files/03_Guardrails_And_Security/detector.py` (Lines 40–120: `validate_verhoeff()` implementing multiplication table $d(i,j)$ and permutation table $p(i,j)$ for 12-digit Indian Aadhaar validation).
  * **Shannon Entropy Analysis ($H \ge 4.5$):** `agentic ai mid sem/imp_files/03_Guardrails_And_Security/secret_detector.py` (Lines 35–95: `calculate_shannon_entropy()` detecting AWS keys, JWTs, and API credentials).
  * **Statutory DPDP Act 2023 Token Vault:** `agentic ai mid sem/imp_files/03_Guardrails_And_Security/token_vault.py` (Lines 25–90: Ephemeral non-invertible UUIDv4 masking and safe in-memory rehydration).
  * **AST Slopsquatting & Package Firewall:** `agentic ai mid sem/imp_files/03_Guardrails_And_Security/package_firewall.py` (Lines 30–110: `PackageFirewall` intercepting `ast.Import` and checking PyPI live via LRU(1024) cache).
  * **Dynamic Token Budget Guardrail:** `agentic ai mid sem/imp_files/03_Guardrails_And_Security/budget_guardrail.py` (Lines 20–75: Hard token consumption ceiling).
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `package_firewall.py`, press `Ctrl+G` line 45 (`def verify_package`).
* **Inbuilt IDE Navigation:** Click `[</> Inbuilt IDE]` $ightarrow$ Category `Guardrails` $ightarrow$ select `package_firewall.py` or `token_vault.py`.
* **Viva Defense Answer:**
  > *"Sir, if an agent hallucinates `import fastapi_jwt_vault_security`, a naive platform runs `pip install` and gets infected. In `package_firewall.py` line 45, our AST parser extracts every imported module name before code writes to disk. We check Python's standard library first (0 ms), then our in-memory LRU cache, and finally query the PyPI registry. An HTTP 404 response blocks the package immediately, stopping supply-chain slopsquatting with 100% accuracy."*

---

### 3.9 Data Security & Privacy (Air-Gapped Local LLM vs Public Cloud)
* **Handout Syllabus:** Deploying open local LLMs for secure and privacy-preserving AI applications.
* **Mapped Course Outcome:** `CO1, CO2`
* **Where We Implemented It in Code:**
  * **Dual Privacy Router:** `agentic ai mid sem/kavach_platform/01_KAVACH_Platform/backend/app/generation/llm_client.py` (Lines 45–130: Inspects classification score from Sentinel Gate; if sensitive data or corporate IP is detected, routes to air-gapped `http://localhost:11434` running Ollama `qwen2.5-coder:7b`; if clean, routes to Gemini 2.5 / Groq).
  * **Adapter Implementations:** `PRJ-IV &AgenticAi Final Work/adapters/ollama_adapter.py` and `gemini_adapter.py`.
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `llm_client.py`, go to Line 52 (`def route_llm_request`).
* **Viva Defense Answer:**
  > *"Sir, sending customer financial records or unreleased proprietary code to external APIs violates the DPDP Act 2023. In `llm_client.py`, we implement dual privacy routing: sanitized requests utilize high-speed cloud APIs, but any payload flagged with sensitive context automatically diverts to our locally hosted, air-gapped Ollama instance, ensuring zero packet transmission outside the local machine."*

---

### 3.10 Multimodal Agent Capabilities (Whisper v3 Audio & Visual Injections)
* **Handout Syllabus:** Multimodal Agent Design: Building intelligent agents that understand and reason over text, audio, images, and video.
* **Mapped Course Outcome:** `CO3`
* **Where We Implemented It in Code:**
  * **Voice / Audio Speech-to-Text:** `agentic ai mid sem/kavach_platform/01_KAVACH_Platform/backend/app/main.py` (Lines 240–280: `/api/voice/transcribe` endpoint utilizing Groq Whisper-large-v3).
  * **Visual Prompt Injection Audit:** `agentic ai mid sem/kavach_platform/01_KAVACH_Platform/backend/app/security/multimodal_vision.py` (Lines 30–95: OCR and adversarial perturbation analysis on uploaded architecture screenshots and documents).
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `multimodal_vision.py`, press `Enter`.
* **Inbuilt IDE Navigation:** Accessible in `01_KAVACH_Platform/backend/app/security/multimodal_vision.py`.
* **Viva Defense Answer:**
  > *"Sir, multimodal agents must defend against visual prompt injections—such as text hidden in an image background with low-contrast font saying 'Ignore previous instructions'. In `multimodal_vision.py`, we preprocess images with contrast normalization and OCR sanitization before forwarding them to multi-modal vision LLMs."*

---

### 3.11 Agent Evaluation & Benchmarking (Grounded Metrics, Red-Team 19 Vectors)
* **Handout Syllabus:** Agent Evaluation: Performance assessment, benchmarking, and iterative improvement.
* **Mapped Course Outcome:** `CO1, CO2`
* **Where We Implemented It in Code:**
  * **Automated Metrics Pipeline:** `agentic ai mid sem/imp_files/07_Observability_And_SSOT_Metrics/generate_metrics.py` (Lines 45–320: Dynamically executes test suites, calculates F1 score, precision, recall, and writes `METRICS.json`).
  * **V1 vs Held-Out V2 Evaluator:** `agentic ai mid sem/kavach_platform/01_KAVACH_Platform/backend/app/security/evaluator_v2.py` (Lines 35–115: 50-case baseline vs 45-case held-out distractor dataset).
  * **19-Vector Red-Team Attack Simulator:** `agentic ai mid sem/kavach_platform/01_KAVACH_Platform/backend/app/security/cyber_attack_simulator.py` (Lines 40–180: Tests Trojan Source, SSRF, Slopsquatting, Zero-Width Steganography, Multi-Hop Taint).
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `generate_metrics.py`, press `Ctrl+G` line 92 (`def get_endpoint_metrics`).
* **Inbuilt IDE Navigation:** Click `[</> Inbuilt IDE]` $ightarrow$ Category `Observability` $ightarrow$ select `generate_metrics.py`.
* **Viva Defense Answer:**
  > *"Sir, we never hardcode metrics. Line 45 of `generate_metrics.py` dynamically extracts the git commit hash, iterates over all 142 FastAPI endpoints, runs the test runner, measures 30-iteration latency percentiles (median 0.02 ms), and records them in `METRICS.json` directly from hardware."*

---

### 3.12 Monitoring & Observability (Telemetry, SSE, SHA3-512 Merkle Ledger)
* **Handout Syllabus:** Monitoring and Observability: Logging, tracing, debugging, and runtime monitoring.
* **Mapped Course Outcome:** `CO2`
* **Where We Implemented It in Code:**
  * **Cryptographic Merkle Ledger:** `agentic ai mid sem/kavach_platform/01_KAVACH_Platform/backend/app/security/merkle_ledger.py` (Lines 25–110: NIST FIPS 202 SHA3-512 leaf hashing, tamper-evident audit chain).
  * **Unified Results Hub:** `agentic ai mid sem/imp_files/07_Observability_And_SSOT_Metrics/results_hub.py` (Lines 30–125: SQLite WAL mode persistence, disk mirroring in `regulatory_audit_log.csv`).
  * **Real-Time Telemetry Streaming:** `agentic ai mid sem/kavach_platform/01_KAVACH_Platform/backend/app/main.py` (Lines 180–225: `/api/telemetry/stream` Server-Sent Events / SSE endpoint).
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `results_hub.py`, press `Enter`.
* **Inbuilt IDE Navigation:** Click `[</> Inbuilt IDE]` $ightarrow$ Category `Observability` $ightarrow$ select `results_hub.py`.
* **Viva Defense Answer:**
  > *"Sir, if an adversary tampers with audit logs, standard databases have no integrity check. In `merkle_ledger.py`, every transaction event is hashed using SHA3-512 and chained to the previous block hash. If a single byte in the ledger is altered, the entire Merkle root recalculation fails, providing mathematical proof of tampering."*

---

### 3.13 Production Deployment (Docker, Kubernetes, Render, 1-Click Launchers)
* **Handout Syllabus:** Deployment: Packaging, deployment strategies, and production considerations.
* **Mapped Course Outcome:** `CO1`
* **Where We Implemented It in Code:**
  * **Containerization:** `agentic ai mid sem/kavach_platform/Dockerfile` and `docker-compose.yml`.
  * **Kubernetes Manifests:** `agentic ai mid sem/kavach_platform/k8s/` (`deployment.yaml`, `service.yaml`, `ingress.yaml`).
  * **Terraform Infrastructure:** `agentic ai mid sem/kavach_platform/terraform/` (`main.tf`, `alb.tf`, `ecs.tf`).
  * **1-Click Launchers:** `agentic ai mid sem/run_midsem.bat` and `PRJ-IV &AgenticAi Final Work/run_all_services.bat`.
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `Dockerfile` or `run_all_services.bat`.
* **Viva Defense Answer:**
  > *"Sir, we provide complete production deployment artifacts: multi-stage Docker builds, Kubernetes manifests for horizontal pod autoscaling, AWS ECS Fargate Terraform scripts, and native 1-click batch scripts for offline examiner demonstrations."*

---

### 3.14 Industry Domains & Use Cases (Bharat Core Banking SAGA ACID & DevOps)
* **Handout Syllabus:** Industry Use Cases: Designing end-to-end agentic solutions and complex multi-agent workflows for customer support, healthcare, finance, software engineering, automated coding, debugging, and execution.
* **Mapped Course Outcome:** `CO1, CO2, CO3`
* **Where We Implemented It in Code:**
  * **Bharat Core Banking Engine:** `agentic ai mid sem/imp_files/06_Bharat_Core_Banking/core_banking.py` and `banking_server.py` (Customer KYC, deposits, transfers, account balances).
  * **Distributed SAGA Orchestrator:** `agentic ai mid sem/imp_files/06_Bharat_Core_Banking/advanced_banking_engines.py` (Lines 45–140: Multi-step distributed transactions with ACID atomicity and automatic backward compensation).
  * **RBI Financial Shield:** `agentic ai mid sem/imp_files/06_Bharat_Core_Banking/kavach_banking_shield.py` (Lines 30–115: High-value HITL quarantine for transactions $\ge$ ₹50,000, Maker-Checker admin approvals, memo prompt injection sanitization).
* **VS Code Navigation Shortcut:** Press `Ctrl+P`, type `core_banking.py` or `kavach_banking_shield.py`, go to Line 45 (`def process_transaction_with_shield`).
* **Inbuilt IDE Navigation:** Click `[</> Inbuilt IDE]` $ightarrow$ Category `Core Banking` $ightarrow$ select `core_banking.py` or `banking_server.py`.
* **Viva Defense Answer:**
  > *"Sir, we applied Agentic AI directly to mission-critical banking. If an AI agent executes a transfer and the ledger stage fails, naive systems leave the balance debited. Our distributed SAGA coordinator in `advanced_banking_engines.py` executes compensatory rollback transactions, restoring account balances to an atomic state in compliance with RBI guidelines."*

---

## 4. TWO-WAY NAVIGATION GUIDE (HOW TO DEMONSTRATE & SHOW THE CODE)

### 4.1 Path A: Inside the Inbuilt Web IDE (`</> Inbuilt IDE`)
Both platform websites (Port 8000 and Port 8001) include a floating button **`</> Inbuilt IDE`** positioned directly above the floating action buttons:

1. **Open the Website:** Navigate to `http://localhost:8000/` (MidSem) or `http://localhost:8001/` (Final Platform).
2. **Launch IDE Modal:** Click the dark navy pill button: **`</> Inbuilt IDE`** (top-right or bottom-right).
3. **Explore by Course Category:** Click on any category filter at the top:
   * `All` | `Google ADK` | `CrewAI` | `Guardrails` | `Design Patterns` | `Protocols` | `Core Banking` | `Observability`
4. **Use Quick Open Search (`Ctrl+P`):**
   * Click the search bar or press `Ctrl+P`.
   * Type any keyword: e.g. `crew ai`, `adk`, `verhoeff`, `self heal`, `react`, `mcp`, `banking`.
   * Press `Enter` to navigate to that file instantly.
5. **View the Live Architecture Flowchart:**
   * On the right panel, click the tab: **`Architecture Flowchart & System Design`**.
   * View the complete ASCII execution pipeline, step-by-step stages, "Why We Chose This Approach", banking domain relevance, and viva oral defense questions!

---

### 4.2 Path B: Directly in VS Code (Shortcuts, File Paths & Highlighting)

If the professor asks: *"Open VS Code and show me where this code is implemented on your laptop!"*, use this exact lookup table:

| If Professor Asks To See... | Press `Ctrl+P` in VS Code and Type | Jump to Line (`Ctrl+G`) | Exact Code Symbol to Highlight | Key Verbal Talking Point |
| :--- | :--- | :---: | :--- | :--- |
| **Google ADK 8 Callbacks** | `callbacks.py` | **Line 35** | `def get_adk_callbacks():` | *"Sir, here are all 8 hooks intercepting Agent, Model, and Tool lifecycles without framework bloat."* |
| **CrewAI Stateful Flows** | `flows.py` | **Line 32** | `class FraudInvestigationFlow(Flow):` | *"Here is the `@start` and `@listen` event-driven multi-agent fan-out architecture."* |
| **Aadhaar Verhoeff Checksum** | `detector.py` | **Line 45** | `def validate_verhoeff(num: str):` | *"Dihedral $D_5$ permutation group validation eliminating arbitrary 12-digit false positives."* |
| **High-Entropy Secret Gate** | `secret_detector.py` | **Line 38** | `def calculate_shannon_entropy(s):` | *"Calculates $H(X) = -\sum p_i \log_2 p_i$. Strings with $H > 4.5$ and length $\ge 16$ are blocked."* |
| **Self-Healing ReAct Sandbox** | `self_healer.py` | **Line 55** | `def autonomous_self_heal(...):` | *"Ephemeral sandbox with a strict mathematical limit of $N \le 3$ reflection attempts."* |
| **Package Slopsquatting** | `package_firewall.py` | **Line 45** | `class PackageFirewall:` | *"AST parser extracts imports and queries live PyPI; 404 response blocks execution."* |
| **Graph-of-Thoughts (GoT)** | `graph_of_thought.py` | **Line 30** | `class GraphOfThoughts:` | *"Dynamic DAG decomposition using Kahn's topological sort theorem to eliminate deadlocks."* |
| **Model Context Protocol** | `mcp_server.py` | **Line 30** | `class FastMCPServer:` | *"Standard JSON-RPC 2.0 interface exposing security tools to external AI agents."* |
| **Bharat Core Bank SAGA** | `advanced_banking_engines.py` | **Line 60** | `class SagaCoordinator:` | *"Atomic multi-step transaction manager with automatic backward compensation rollback."* |
| **Measured SSOT Metrics** | `generate_metrics.py` | **Line 45** | `def generate_all_metrics():` | *"Introspects hardware via `ctypes`, counts endpoints dynamically, and writes `METRICS.json`."* |

---

## 5. The 9 Defensive Stages & Subsystems (Detailed Engineering Architecture)

### Stage 1: Sentinel Pre-Execution Gatekeeper & Zero-Knowledge Token Vault
* **Primary Source Code:** `imp_files/03_Guardrails_And_Security/` (`detector.py`, `secret_detector.py`, `token_vault.py`).
* **Verhoeff Algorithm:** Validates 12-digit Indian Aadhaar numbers using the dihedral group $D_5$ (multiplication table $d$ and inverse permutation table $p$).
* **Shannon Entropy:** Computes character entropy $H(X) = -\sum p_i \log_2 p_i$. Tokens exceeding $H(X) > 4.5$ with length $\ge 16$ are flagged as secrets (AWS keys, OpenAI/Gemini tokens, JWTs).
* **Token Vault:** Substitutes sensitive tokens with ephemeral UUIDv4 masks. Median latency: **0.02 ms**.

### Stage 2: Agentic Code RAG Engine (Qdrant & Dense Embeddings)
* **Primary Source Code:** `kavach_platform/01_KAVACH_Platform/backend/app/rag/` (`ingest.py`, `embed_store.py`).
* **Semantic AST Chunking:** 1200-character segments respecting function/class boundaries.
* **Vector Store:** 384-dimensional dense vectors via `all-MiniLM-L6-v2` in Qdrant with HNSW index.
* **Fact-Grounded Cosine Gating:** Matches incoming developer queries against code chunks with $\cos(	heta) \ge 0.70$.

### Stage 3: AST Dependency Graph & Blast-Radius Engine
* **Primary Source Code:** `kavach_platform/01_KAVACH_Platform/backend/app/impact/` (`dependency_graph.py`, `analyzer.py`).
* **Static AST Dependency Graph:** Parses `ast.parse` across the whole repository without execution.
* **Transitive Reachability Blast Radius Score:**
  $$B(v) = rac{|	ext{Reach}(v)|}{|V| - 1}$$
  Scores above $B(v) > 0.40$ mandate human-in-the-loop review.

### Stage 4: Supply-Chain Slopsquatting & Package Hallucination Firewall
* **Primary Source Code:** `imp_files/03_Guardrails_And_Security/package_firewall.py`.
* **Static Import Interception:** Intercepts `import <pkg>` nodes in AST before code writes to disk.
* **Tiered Verification:** Standard Library (0 ms) $ightarrow$ LRU Cache (capacity 1024) $ightarrow$ Live PyPI REST query (`https://pypi.org/pypi/<pkg>/json`). 404 response halts execution with exit code 1. Interception rate: **100.0%**.

### Stage 5: Autonomous Bounded ReAct Sandbox & Self-Healing Loop
* **Primary Source Code:** `imp_files/04_Agentic_Design_Patterns/` (`react_engine.py`, `self_healer.py`).
* **Ephemeral Subprocess Sandbox:** Runs candidate code modifications in isolated `pytest` with a 5.0-second CPU watchdog.
* **Bounded Reflection ($N \le 3$):** Feeds compiler errors and stack traces into the reflection prompt. Strictly capped at 3 cycles to prevent infinite token waste.

### Stage 6: Cyber Defense & Red-Teaming Engine (34 Security Modules)
* **Primary Source Code Directory:** `kavach_platform/01_KAVACH_Platform/backend/app/security/` (35 security engines).
* **Modules:** `ssrf_shield.py`, `steganography_shield.py` (Zero-Width Space removal), `polyglot_firewall.py`, `obfuscation_detector.py` (Base64/homoglyph lookalikes), `injection_shield.py` (OWASP LLM01:2025), `merkle_ledger.py` (SHA3-512 chain).
* **Red-Team Benchmark:** 19/19 adversarial attack vectors blocked (**100.0% interception rate**).

### Stage 7: Multi-Agent Swarms & Protocol Layer (ADK, CrewAI, MCP, A2A)
* **Primary Source Code:** `imp_files/01_Google_ADK/`, `02_CrewAI/`, `05_Protocols_MCP_And_A2A/`.
* **ADK 8-Hook Callbacks:** Intercepts before/after Agent, Model, and Tool execution.
* **CrewAI Stateful Flows:** Dynamic `@start` and `@listen` workflow automation.
* **Protocols:** FastMCP JSON-RPC server and A2A standardized message envelopes.

### Stage 8: Bharat Commercial Core Banking System (`bharat_core_banking/`)
* **Primary Source Code:** `PRJ-IV &AgenticAi Final Work/bharat_core_banking/` and `imp_files/06_Bharat_Core_Banking/`.
* **RBI High-Value HITL Escrow:** Transactions exceeding **₹50,000.00** are quarantined in escrow requiring statutory Maker-Checker approval.
* **Distributed SAGA Orchestrator:** Multi-step transactions with ACID transactional atomicity and backward compensation rollback.
* **Basel III Compliance:** Real-time Capital Adequacy Ratio ($	ext{CAR} \ge 11.5\%$) and Liquidity Coverage Ratio ($	ext{LCR} \ge 100\%$).

### Stage 9: Unified Results Cockpit & Cryptographic Telemetry (`results_hub.py`)
* **Primary Source Code:** `imp_files/07_Observability_And_SSOT_Metrics/results_hub.py`.
* **Cryptographic Storage:** SQLite Write-Ahead Logging (WAL) and NIST FIPS 202 SHA3-512 Merkle leaf hashes for tamper evidence.

---

## 6. Single Source of Truth (SSOT) Measured Metrics & Verification Reality

All figures below are generated by `generate_metrics.py` and recorded in `METRICS.json`:

* **Host Environment:** Windows 11 (AMD64, 20 Logical Cores, 15.75 GB RAM, Python 3.14.7).
* **Deterministic Verification Suites:** **300 / 300 PASSING** (100% pass rate).
  1. `test_kavach_100_suite.py`: 100/100 PASS
  2. `test_banking_100_suite.py`: 100/100 PASS
  3. `test_unified_100_suite.py`: 100/100 PASS
* **Full Repository Pytest Inventory:** **641 / 641 Total Passing Tests**.
* **Registered REST API Endpoints:** **142 Endpoints** across KAVACH Core (120), Bharat Banking (15), and Results Hub (7).
* **Evaluator Performance:**
  * Baseline V1 (50 cases): Precision 100%, Recall 100%, F1 1.000.
  * Held-Out V2 (45 cases): Precision 89.3%, Recall 100%, F1 94.3% (3 false positives on order/SKU strings like `BLK-9876543210` honestly documented).
* **Latency Benchmarks (30 Runs):** PII Detector median **0.02 ms**; Secret Detector median **0.02 ms**; End-to-end Agent Workflow median **334.41 ms**.

---

## 7. Official University Evaluation Matrix (CSE3101: 30 Marks) & Student Submissions

### 7.1 Section A: Evaluation Criteria Breakdown (Phase-2: 30 Marks Total)

| Rubric Code | Evaluation Criteria | Max Marks | Target / Score | Implementation Reality & Measured Grounding Proof | Key Verification Evidence |
| :---: | :--- | :---: | :---: | :--- | :--- |
| **C6** | **Progress vs. Plan** | **5** | **5 / 5** | • Planned 6 lifecycle stages $ightarrow$ All 6 actively operational in orchestrator.<br>• 16-Week Agile Milestone Schedule with explicit Planned vs. Actual tracking.<br>• Documented Slip Analysis (SLIP-01 to SLIP-04) explaining technical adaptations.<br>• Honest requirement tracking: **11 Met, 2 Partial, 4 Deferred with written plan**. | `02_UPDATED_PROJECT_PLAN.md`<br>Chapter 1 of WIP Report |
| **C7** | **Technical Understanding** | **5** | **5 / 5** | • Deterministic FSM orchestrator replacing unconstrained LLM loops.<br>• Dihedral $D_5$ Verhoeff checksum algorithm for 12-digit Indian Aadhaar validation.<br>• Shannon entropy ($H(X) > 4.5$) for zero-parameter API secret detection.<br>• Transitive reachability blast-radius score $B(v) = rac{|	ext{Reach}(v)|}{|V|-1}$ via static AST parsing.<br>• PyPI LRU(1024) package hallucination firewall.<br>• SAGA distributed transaction coordinator with backward ACID compensations. | `VIVA_CODE_MAP.md`<br>Chapter 3 of WIP Report |
| **C8** | **Requirements Met Till Now with Actual Approach** | **10** | **10 / 10** | • **11 of 17 Core Requirements MET 100%** with working code.<br>• **2 Requirements PARTIAL** (Deployment configs complete, voice STT operational).<br>• **4 Requirements DEFERRED** to Phase 3 with written architectural roadmaps.<br>• **300 / 300 Deterministic Tests Passing** across 3 dedicated master suites.<br>• **641 / 641 Total Repository Tests Passing** across 18 test files.<br>• **142 Registered REST Endpoints** live and callable. | `docs/METRICS.md`<br>Chapter 2 of WIP Report |
| **C9** | **Documentation (Working)** | **5** | **5 / 5** | • Single Source of Truth architecture (`docs/METRICS.json` generated from code).<br>• `CLAIMS_LEDGER.csv` mapping all claims to verification scripts.<br>• Complete 86KB `FINAL_SYNOPSIS_REPORT.md` capstone specification.<br>• IEEE SecDev / COMPSAC conference research publication draft with LaTeX bundles.<br>• Automated daily 04:00 UTC CI/CD telemetry audit via GitHub Actions. | `docs/METRICS.json`<br>Chapter 4 of WIP Report |
| **C10** | **Individual Contribution (Viva)** | **5** | **5 / 5** | • Rigorous role rotation satisfying Page 7 of Course Handout.<br>• **Dhruv Jain (230532):** Lead Architect & Developer — FSM orchestrator, security engine, banking shield, MCP/A2A, RAG, AST graph.<br>• **Hemant Goyal:** Testing support, dependency setup, documentation audit, AST blast radius lead in Phase 2.<br>• **Rajat Yadav:** Demo coordination, presentation decks, QA assistance, voice input & UI telemetry. | `03_WORK_IN_PROGRESS_REPORT.md`<br>Chapter 5 of WIP Report |
| **TOTAL** | **Phase-2 Capstone Evaluation** | **30** | **30 / 30** | **Fully Verified & Defendable with 1-Command Live Code Execution (`run_midsem.bat`)** | |

---

### 7.2 The 17-Requirement Mid-Sem Audit Ledger (Chapter 2 Traceability)

| # | Requirement / Objective | Mapped CO | Measurable Code Evidence / Actual Approach | Mid-Sem Status |
| :---: | :--- | :---: | :--- | :---: |
| **R1** | Multi-agent orchestration | CO1 | FSM orchestrator (6 active stages) + ADK coordinator + CrewAI team | **MET** |
| **R2** | Privacy-preserving local LLM generation | CO2 | Dual-engine routing (cloud Gemini / air-gapped local Ollama) + token vault | **MET** |
| **R3** | Deterministic pre-execution security gate | CO1, CO2 | Entropy ($H > 4.5$) + Verhoeff $D_5$ + policy engine; V1 F1 1.00, held-out V2 F1 0.943 | **MET** *(Limitation noted)* |
| **R4** | MCP interoperability | CO3 | Anthropic MCP server and client over JSON-RPC 2.0 | **MET** |
| **R5** | Agent-to-agent communication | CO3 | Google A2A standardized message protocol | **MET** |
| **R6** | Change-impact awareness | CO1, CO3 | Static AST dependency graph, $B(v)$ blast-radius score, human review above 0.40 | **MET** |
| **R7** | Agentic Code RAG | CO1 | Qdrant vector database, AST-aware chunks, cosine $\ge 0.70$ gating | **MET** |
| **R8** | Bounded reflection sandbox | CO1 | Ephemeral sandbox self-healer with CPU watchdog, $N \le 3$ reflection cycles | **MET** |
| **R9** | Guardrails and cyber safety | CO2 | Prompt injection, SSRF, steganography, obfuscation, taint shields; 19/19 attacks blocked | **MET** |
| **R10** | Agent evaluation & benchmarking | CO1, CO2 | V1 and V2 evaluators, 15-vector red-team suite, 30-run component latency benchmarks | **MET** |
| **R11** | Monitoring and observability | CO2 | Glassmorphic dashboards, SSE telemetry, SHA3-512 Merkle ledger, daily CI heartbeat | **MET** |
| **R12** | Production deployment | CO1 | Dockerfile, K8s manifests, Terraform AWS ECS, Render, Cloud Run, HF Spaces | **PARTIAL** |
| **R13** | Multimodal agent capabilities | CO3 | Groq Whisper v3 voice input, visual prompt injection image audit | **PARTIAL** |
| **R14** | Test-gen & build-and-test stages live | CO1 | Enums defined in `state.py`; execution currently passthrough | **DEFERRED** *(Phase 3 Roadmap)* |
| **R15** | Persistent database run history | CO1 | High-throughput in-memory run store today; PostgreSQL migration planned | **DEFERRED** *(Phase 3 Roadmap)* |
| **R16** | GitHub PR Guardian bot | CO3 | Standalone CLI gate and CI heartbeat operational; GitHub webhook bot planned | **DEFERRED** *(Phase 3 Roadmap)* |
| **R17** | Held-out false-positive fix | CO2 | Planned with independent held-out V3 set of $\ge 40$ cases written first | **DEFERRED** *(Phase 3 Roadmap)* |

---

## 8. Faculty Examiner Viva Defense Script (Dr. Shaikh & Mr. Tiwari)

#### Q1: "Why do you have 4 requirements marked as 'Deferred' in your report?"
> **Verbatim Answer:**  
> *"Respected Sirs, in accordance with Rubric C6 (Progress vs. Plan) and industry Agile practices, Phase 2 represents the mid-term milestone at Week 8. Our primary objective for Mid-Sem was to establish the verified core governance pipeline: the 6-stage finite-state machine, the 34 security modules, RAG context retrieval, AST blast-radius analysis, and our Bharat Banking demonstration—all backed by 641 passing tests and 142 live endpoints.*  
> *The 4 deferred items—such as migrating our current in-memory run store to PostgreSQL, wiring the GitHub PR webhook bot, and refining the 10-digit SKU regex patterns against a fresh V3 dataset—are our planned Phase-3 deliverables for the final 40% capstone evaluation as detailed in our 16-week project schedule."*

#### Q2: "Did you use external libraries like CrewAI or Google ADK?"
> **Verbatim Answer:**  
> *"Sir, we implemented clean, native in-repo architectural models following the official specifications (`imp_files/02_CrewAI/` for CrewAI stateful flows, and `imp_files/01_Google_ADK/` for Google ADK 8-hook callbacks). This intentional architectural choice ensures complete cross-platform stability on Python 3.14 without reliance on fragile external C-extensions, while maintaining exact structural compliance."*

#### Q3: "Why does the Held-Out V2 evaluation show an F1 of 0.943 instead of 1.00?"
> **Verbatim Answer:**  
> *"Sir, on our initial V1 test corpus, KAVACH achieves a 100% F1 score. However, following 'The One Principle' that measured reality is the source of truth, we evaluated KAVACH against an independent held-out V2 corpus of 45 fresh cases containing realistic distractors.*  
> *Our sensitivity and recall remained a perfect 100%—zero sensitive tokens leaked. Three false positives occurred on 10-digit order tracking codes (e.g. `BLK-9876543210`) because the trailing 10 digits match mobile number sequences. Rather than rushing an ad-hoc regex fix that could cause regressions right before evaluation, we honestly report 89.3% precision and have scheduled prefix-boundary disambiguation for Phase 3 with a dedicated 40-case V3 test suite."*

#### Q4: "What is your measured latency overhead for deterministic security checks?"
> **Verbatim Answer:**  
> *"Our deterministic security scanners—the Verhoeff Aadhaar validator and Shannon entropy secret detector—execute in a median time of just **0.02 milliseconds** (20 microseconds), which is less than 0.01% of total pipeline latency. The entire end-to-end agent workflow completes in a median of **334.41 milliseconds**, well below the 1.5-second industry threshold."*

#### Q5: "How do you prove these metrics are not hardcoded?"
> **Verbatim Answer:**  
> *"All numbers are generated dynamically by executing `python generate_metrics.py`. The script inspects the running Python interpreter, counts FastAPI route registrations dynamically, executes the test runners, and writes the JSON output stamped with the exact git commit hash."*

---

## 9. Operational Guide: How to Run, Test, and Verify Everything

### 9.1 Launching the Applications (1-Click)
1. **MidSem Work (Port 8000):**
   ```powershell
   cd "agentic ai mid sem"
   .un_midsem.bat
   ```
   Visit: `http://localhost:8000/`

2. **Final Project (All 3 Services: 8001, 8002, 8003):**
   ```powershell
   cd "PRJ-IV &AgenticAi Final Work"
   .un_all_services.bat
   ```
   - Master Platform: `http://localhost:8001/`
   - Bharat Core Bank Portal: `http://localhost:8002/`
   - Live Agent Swarm: `http://localhost:8003/`

### 9.2 Running Test Suites
```powershell
# 1. Run 300 Master Deterministic Tests:
pytest "agentic ai mid sem/kavach_platform/01_KAVACH_Platform/tests/test_kavach_100_suite.py" -v
pytest "agentic ai mid sem/kavach_platform/02_Banking_and_Results_Dashboard/implementation_banks/test_banking_100_suite.py" -v
pytest "agentic ai mid sem/kavach_platform/02_Banking_and_Results_Dashboard/tests_unified/test_unified_100_suite.py" -v

# 2. Run Full 641 Repository Pytest Inventory:
pytest "agentic ai mid sem/kavach_platform"
```

---

## 10. Deliberately Deferred Items, Scope Discipline & Phase 3 Roadmap

When continuing development into Phase 3 (End-Term 40% Capstone), adhere to the following roadmap:
1. **Prefix-Boundary Disambiguation for 10-Digit Alphanumeric Strings:** Introduce regex negative lookbehinds in `patterns.py` to prevent SKU/tracking codes like `BLK-9876543210` from triggering mobile phone rules, validated against an independent 40-case V3 test corpus.
2. **Production PostgreSQL Async Persistence:** Migrate the in-memory run store in `state.py` to async SQLAlchemy / PostgreSQL.
3. **Active Pipeline Enums:** Connect `TEST_GENERATION` and `BUILD_AND_TEST` enum states in `state.py` directly into the orchestrator loop.
4. **GitHub PR Guardian Bot:** Connect `ci_security_gate.py` to a GitHub Webhook handler for automatic PR commenting.

---
*Authored by Dhruv Jain (230532) · BML Munjal University · Verified Single Source of Truth.*
