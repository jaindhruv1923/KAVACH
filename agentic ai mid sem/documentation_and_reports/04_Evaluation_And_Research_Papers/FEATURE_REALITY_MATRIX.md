# KAVACH: Feature Reality Matrix & Architectural Grounding Audit

**Audit Date:** 2026-10-25  
**Audit Scope:** Full repository code inspection, call-graph tracing, and dependency verification  
**Standard:** The One Principle — Measured reality is the single source of truth.

---

## 1. Deep Call-Graph Analysis: `/agent/request`

### 1.1 Complete End-to-End Execution Flow
When a developer or client submits a `POST /agent/request` payload (`{"request_text": "..."}`), the execution path proceeds through the following deterministic sequence:

```
Client HTTP Request
   │
   ▼
[app/main.py:submit_agent_request] (Line 629)
   │ Unpacks payload.request_text and passes to orchestrator
   ▼
[app/agent/orchestrator.py:run_workflow] (Line 37)
   │
   ├──> 1. Initial State Initialization:
   │       - Creates WorkflowRun instance (app/agent/state.py:34) with unique UUID
   │       - Computes redacted request text via `app/security/audit_redaction.py:redact_text`
   │       - Initial stage: WorkflowStage.REQUEST_RECEIVED
   │
   ├──> 2. Pre-Flight Input Security Scan:
   │       - Calls `_scan(request_text)` combining `detect_pii` (app/security/detector.py:21)
   │         and `detect_secrets` (app/security/secret_detector.py:22)
   │       - Appends findings to run.security_findings
   │       - Evaluates risk matrix via `evaluate_policy` (app/security/policy_engine.py:23)
   │       - IF decision == BLOCK: advances to WorkflowStage.BLOCKED and aborts execution.
   │       - IF decision == REVIEW: advances to WorkflowStage.NEEDS_REVIEW and aborts execution.
   │
   ├──> 3. Task Planning Stage:
   │       - Advances to WorkflowStage.PLANNING
   │       - Invokes `plan_request(request_text)` (app/agent/planner.py:28)
   │       - Decomposes request into task steps using regex keyword dictionary matching.
   │
   ├──> 4. Context Retrieval (RAG) Stage:
   │       - Advances to WorkflowStage.CONTEXT_RETRIEVAL
   │       - Checks Qdrant vector database via `app/rag/embed_store.py:get_client`
   │       - If empty and outside pytest, triggers auto-ingestion of backend codebase
   │       - Runs cosine similarity search: `search(request_text, top_k=5)`
   │       - In case of client or embedder exception, catches error gracefully and logs to history.
   │
   ├──> 5. Context Security & Prompt Injection Shield:
   │       - Advances to WorkflowStage.SECURITY_CHECK
   │       - Iterates through retrieved text chunks:
   │         * Runs `inspect_prompt_safety(chunk_text)` (app/security/injection_shield.py:104)
   │         * If jailbreak / injection detected: replaces chunk text with `[SANITIZED REPO CONTEXT: ...]`
   │         * Runs `_scan()` on chunk text; redacts identified secrets/PII via `redact_text()`
   │       - If critical live credential found in context: evaluates policy; if BLOCK, aborts.
   │
   ├──> 6. Change-Impact Analysis Stage:
   │       - Advances to WorkflowStage.IMPACT_ANALYSIS
   │       - Invokes `analyze_impact(request_text, repo_root, top_k=5)` (app/impact/analyzer.py:143)
   │       - Builds AST import graphs and calculates blast radius scores across Python modules.
   │
   ├──> 7. Evidence-Grounded Generation Stage:
   │       - Advances to WorkflowStage.GENERATION
   │       - Invokes `generate_code(request_text, run.retrieved_context)` (app/generation/generator.py:45)
   │       - Formats grounding prompt with strict constraints (`build_grounded_prompt`)
   │       - Calls `call_llm(prompt)` (app/generation/llm_client.py:147)
   │       - If live Gemini key exists: queries Gemini API over HTTPS;
   │         If AIR_GAPPED_MODE: dispatches to local Ollama REST endpoint;
   │         If pytest/unconfigured: returns deterministic code stub.
   │
   ├──> 8. Output Security Gate & Syntax Validation:
   │       - Runs `_scan(generated_output)` over newly generated text.
   │       - If LLM leaked sensitive data: evaluates policy; blocks if BLOCK/REVIEW.
   │       - Runs `validate_generated_output(generated_output)` (app/generation/validator.py:179)
   │       - Parses code using Python's native `ast.parse()` to verify syntactical validity.
   │
   └──> 9. Terminal Finalization:
           - Advances to WorkflowStage.COMPLETE
           - Computes total duration in milliseconds
           - Saves run state and returns full JSON response to client.
```

---

### 1.2 Core Architectural Verification Questions

#### Question 1: Where does the LLM actually decide something versus only generating text?
* **Empirical Reality:** The LLM decides **ABSOLUTELY NOTHING**.
* **Detailed Evidence:**
  1. The LLM is invoked in exactly one location: `app/generation/generator.py` line 53 (`call_llm(prompt)`).
  2. The LLM's role is strictly confined to generating plain text (code blocks and explanatory comments) based on a structured evidence prompt.
  3. All workflow branching, state transitions, security verdicts, and policy actions are made by **deterministic Python code**:
     - Pre-flight routing (BLOCK vs ALLOW vs REVIEW) is computed by deterministic boolean rules in `app/security/policy_engine.py`.
     - Planning step decomposition is computed by regular expressions in `app/agent/planner.py`.
     - Indirect prompt injection detection is computed by regex rule patterns in `app/security/injection_shield.py`.
     - Code syntax validation is evaluated by Python's built-in `ast.parse()` in `app/generation/validator.py`.
  4. There is no LLM-based reasoning agent, no self-reflection loop, and no LLM-driven control flow.

#### Question 2: Does any real tool-calling loop exist?
* **Empirical Reality:** **NO REAL TOOL-CALLING LOOP EXISTS** in the agent orchestrator.
* **Detailed Evidence:**
  1. The execution pipeline in `app/agent/orchestrator.py` is a strictly linear, single-pass pipeline (`REQUEST_RECEIVED` $\to$ `PLANNING` $\to$ `CONTEXT_RETRIEVAL` $\to$ `SECURITY_CHECK` $\to$ `IMPACT_ANALYSIS` $\to$ `GENERATION` $\to$ `COMPLETE`).
  2. The model does not emit function calls, does not receive tool outputs back, and does not iterate in a ReAct (Reason + Act) loop.
  3. While an external `app/security/prompt_variance_engine.py` file defines a `validate_tool_return_type()` helper, and `app/adk/callbacks.py` defines `before_tool_callback` hooks, these are modular unit callbacks tested in isolation; they are not wired into an autonomous LLM tool-calling cycle within `run_workflow()`.

#### Question 3: Does the agent ever change files or run tests?
* **Empirical Reality:** **NO. THE AGENT NEVER WRITES TO DISK FILES OR RUNS TESTS.**
* **Detailed Evidence:**
  1. **File Modification:** The code generated in `WorkflowRun.generation_result["generated_output"]` is returned purely as an in-memory string within the HTTP response JSON. The orchestrator never opens a workspace file with write permissions, does not write diffs, and executes no filesystem `write()` operations.
  2. **Test Execution:** In `app/agent/state.py` (lines 25–27), the stages `TEST_GENERATION`, `BUILD_AND_TEST`, and `CICD_GATE` are defined in the enum but explicitly commented as `"not implemented yet, passthrough for now"`. The orchestrator completely skips these stages and advances directly from `GENERATION` to `COMPLETE`. No subprocess invokes `pytest`, and no sandbox test harness is triggered during an `/agent/request`.

#### Question 4: Do `adk/` and `crew/` use the real `google-adk` and `crewai` libraries or are they hand-written imitations?
* **Empirical Reality:** **THEY ARE 100% HAND-WRITTEN IN-REPO IMITATIONS.**
* **Detailed Evidence:**
  1. Neither `crewai` nor `google-adk` is present in `01_KAVACH_Platform/backend/requirements.txt`.
  2. In `app/crew/agents.py`, the `CrewAgent` class is authored from scratch using pure Python, managing its own `self.tools` list and `self.memory_buffer` without importing CrewAI.
  3. In `app/adk/agent.py`, the `LlmAgent` class and `AgentLifecycleState` enum are authored from scratch without importing any Google SDK.
  4. In `app/adk/callbacks.py`, the 8-hook callback architecture (`before_agent`, `after_agent`, `before_model`, `after_model`, `on_model_error`, `before_tool`, `after_tool`, `on_tool_error`) is an in-repo emulation designed to satisfy academic syllabus requirements.
  5. Any documentation claiming external package integration is a historical claim that must be described as "in-repo architectural pattern emulation."

---

## 2. Feature Reality Matrix

The table below audits every claimed subsystem in KAVACH, comparing the promotional/documentation claims against the actual source code reality.

| Subsystem / Feature | Claimed Capability | Actual Code Reality | Grounding File & Function | Reality Status |
| :--- | :--- | :--- | :--- | :---: |
| **Pre-Flight PII Detection** | Real-time Indian national identifier and contact detection | High-speed regex detection for PAN, Aadhaar, phone numbers, bank accounts, and email addresses. Sub-millisecond latency (median 0.017 ms). | `app/security/detector.py:detect_pii` | **IMPLEMENTED (Native)** |
| **High-Entropy Secret Detection** | Mathematical Shannon entropy and pattern matching for credentials | Calculates Shannon entropy ($H > 4.5$) on candidate tokens and matches AWS, GitHub, Slack, and private keys. Median latency 0.019 ms. | `app/security/secret_detector.py:detect_secrets` | **IMPLEMENTED (Native)** |
| **Risk-Adaptive Policy Engine** | Dynamic enterprise policy grading with granular action matrices | Evaluates input context, entity type, and credential severity against `PolicyAction.ALLOW`, `BLOCK`, `REVIEW`. Treats `REVIEW` as immediate halt due to pending supervisor endpoint. | `app/security/policy_engine.py:evaluate_policy` | **IMPLEMENTED (Rule-Based)** |
| **Audit Log Redaction** | Secondary data leak prevention in audit logs | Redacts sensitive tokens with structured masks (e.g. `9876-XXXX-1098`) before storing in `WorkflowRun.redacted_request_text`. | `app/security/audit_redaction.py:redact_text` | **IMPLEMENTED (Native)** |
| **Indirect Prompt Injection Shield** | Defense against adversarial prompt manipulation | Regex patterns detecting instruction override, delimiters, and role-play jailbreaks. Sanitizes retrieved context chunks inline. | `app/security/injection_shield.py:inspect_prompt_safety` | **IMPLEMENTED (Rule-Based)** |
| **Agent Task Decomposition** | Autonomous multi-step planning | Naive regex dictionary matching on keywords (`auth`, `password`, `test`, `api`, `database`). No LLM planning or autonomous goal expansion. | `app/agent/planner.py:plan_request` | **SIMULATED (Rule-Based)** |
| **RAG Context Retrieval** | Vector repository search grounded in embeddings | Qdrant client vector store using `sentence-transformers` embeddings (`all-MiniLM-L6-v2`). Gracefully degrades to empty context if Qdrant fails. | `app/rag/embed_store.py:search` | **IMPLEMENTED (Native)** |
| **AST Change Impact Analysis** | Code blast radius calculation | Static analysis parsing Python AST imports, computing dependent module sets, and calculating blast radius score (0.0 to 1.0). | `app/impact/analyzer.py:analyze_impact` | **IMPLEMENTED (Native)** |
| **Code Generation** | Evidence-grounded generation | Assembles evidence into a strict system prompt; queries Gemini API via HTTPS or Ollama locally; falls back to static template stub in test/offline mode. | `app/generation/generator.py:generate_code` | **IMPLEMENTED (Hybrid / Stub)** |
| **Syntax Validation** | Verification of generated code | Parses code text using `ast.parse()`; reports syntax error lines and extracts valid code blocks. | `app/generation/validator.py:validate_generated_output` | **IMPLEMENTED (Native)** |
| **Test Generation & CICD** | Automated test creation and sandboxed test execution | Stages `TEST_GENERATION`, `BUILD_AND_TEST`, and `CICD_GATE` exist in enum but have zero implementation in `run_workflow()`. | `app/agent/orchestrator.py` & `app/agent/state.py` | **PASSTHROUGH / UNWIRED** |
| **Google ADK Framework** | Integration with official Google Agent Development Kit | Custom Python classes implementing the 8-hook callback pattern, lifecycle states, and tool contexts. Zero imports from Google libraries. | `app/adk/agent.py:LlmAgent` & `callbacks.py` | **EMULATION (In-Repo)** |
| **CrewAI Multi-Agent System** | CrewAI agent collaboration with role delegation | Custom Python classes defining `CrewAgent`, `CrewTask`, and sequential runner. Zero imports from `crewai` library. | `app/crew/agents.py:CrewAgent` & `crew_runner.py` | **EMULATION (In-Repo)** |
| **Bharat Core Banking Gateway** | Core banking simulation with time-lock escrow | FastAPI sub-application mounted at `/bank` with 15 routes, Saga compensations, CBDC minting, and time-lock escrow with clawback. | `02_Banking_and_Results_Dashboard/implementation_banks/server.py` | **IMPLEMENTED (Native)** |
| **Results Telemetry Cockpit** | Centralized audit and test results dashboard | FastAPI sub-application mounted at `/results` with 7 routes, in-memory event bus, debounced file flushing, and CSV/JSON exports. | `02_Banking_and_Results_Dashboard/results_dashboard/hub.py` | **IMPLEMENTED (Native)** |
| **MicroVM Sandboxing** | Firecracker / gVisor isolated microVM execution | Pure in-process mock execution and subprocess containment with execution time caps. No actual virtualization or kernel sandboxing. | `app/security/sandbox_monitor.py` | **SIMULATED (In-Process)** |

---

## 3. Key Conclusions for Defense and Documentation
1. **The System is a Deterministic Security Governance Layer:** KAVACH's primary strength is not autonomous generative agents, but high-speed, sub-millisecond deterministic inspection gates (PII, secrets, prompt injection, and AST blast radius).
2. **Transparency Wins:** Acknowledging that `adk/` and `crew/` are clean architectural emulations and that `planner.py` uses rule-based decomposition demonstrates rigorous engineering honesty rather than fraudulent claims.
3. **Safe by Default:** Because the agent never modifies repository files or triggers uncontained shell commands, KAVACH inherently prevents catastrophic unauthorized code modifications.
