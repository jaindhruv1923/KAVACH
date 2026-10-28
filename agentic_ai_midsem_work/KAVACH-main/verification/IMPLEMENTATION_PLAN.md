# KAVACH: Real Agentic AI Execution Engine — Implementation Plan

**Objective:** Upgrade KAVACH from a single-pass code generation pipeline into a genuinely functional, end-to-end Agentic AI platform with an iterative ReAct execution loop, real tool registry, multi-agent coordination, permissions, sandbox containment, and live frontend observability.

---

## 1. Architectural Strategy & Ground Rules

1. **Preserve Existing Strengths:**
   - Retain all sub-millisecond pre-execution guardrails (`detect_pii`, `detect_secrets`, `inspect_prompt_safety`).
   - Retain AST change-impact analysis (`analyzer.py`) and Qdrant RAG vector retrieval (`embed_store.py`).
   - Retain Bharat Core Banking (`/bank`) and Unified Results Cockpit (`/results`).
   - Retain existing API routes and data shapes to prevent breaking existing tests.
2. **Build the Genuine Agentic Execution Engine:**
   - Replace the static single-pass execution in `app/agent/orchestrator.py` with an iterative, bounded **Agentic Execution Engine** (`AgenticReActEngine`).
   - Real, registered tools performing actual operations on the repository within an authorized workspace boundary.
   - Genuine decision step: LLM (via Gemini or Ollama) evaluates previous steps and tool observations, and outputs structured action decisions (Tool Call or Finish).
   - Strict safety bounds: Maximum iterations (e.g. 6), per-tool execution timeouts, path traversal guards (`os.path.commonpath`), allowlisted test runners (`pytest -k ...`), and Human-in-the-Loop (HITL) approval gates for file writes/patches.
   - Deterministic Fallback: When offline or unconfigured, execute a deterministic heuristic plan that genuinely runs real tools (file read, tree inspect, pytest) and produces real verifiable output, explicitly labeled as `[DETERMINISTIC FALLBACK]`.
3. **Real Tool Registry (`app/agent/tools.py`):**
   - `repo_list_tree`: Inspect repository structure under permitted paths.
   - `repo_read_file`: Read permitted source code with line count and length limits.
   - `repo_search_code`: Search literal or regex patterns across permitted source files.
   - `security_scan_code`: Run PII and secret detection on text or code.
   - `ast_analyze_impact`: Analyze module imports and blast radius using AST.
   - `run_allowlisted_tests`: Run specific allowlisted pytest test suites in a subprocess with timeouts and return real stdout/stderr/exit_code.
   - `propose_code_patch`: Generate a diff or patch for review.
   - `apply_approved_patch`: Apply a patch to an authorized file with backup and permission checks (requires HITL approval).
4. **Specialized Multi-Agent Roles (`app/agent/multi_agent.py`):**
   - **Coordinator Agent:** Decomposes user goal, selects active specialist, reviews intermediate progress.
   - **Repository Inspector Agent:** Explores codebase, reads relevant files, searches function definitions.
   - **Security Auditor Agent:** Scans inputs, diffs, and generated code for PII, secrets, and indirect injection.
   - **Verification & Testing Agent:** Runs targeted test suites, parses test failures, and checks syntax validity.
5. **Observability & Frontend Streaming:**
   - Stream structured execution events: `AGENT_THOUGHT`, `TOOL_CALL`, `TOOL_OBSERVATION`, `APPROVAL_REQUIRED`, `TEST_RESULTS`, `TASK_COMPLETE`.
   - Update `app/agent/state.py` to store granular step-by-step trace objects with execution times, tool arguments, outputs, and exit codes.
   - Expose SSE endpoint `/agent/stream/{run_id}` and WebSocket/Polling endpoints.
   - Update `01_KAVACH_Platform/frontend/console.html` and `app.js` to render live interactive step traces with tool inputs and real test outputs.

---

## 2. Implementation Milestones

- [x] **Milestone 1:** Phase 1 Inspection & Course Requirements Traceability (`COURSE_REQUIREMENTS_TRACEABILITY.md`).
- [ ] **Milestone 2:** Implement Core Tool System (`app/agent/tools.py`) with input/output validation, workspace containment, and tests.
- [ ] **Milestone 3:** Implement Bounded ReAct Execution Engine (`app/agent/react_engine.py`) with real LLM tool-calling and deterministic fallback.
- [ ] **Milestone 4:** Implement Multi-Agent Roles and Coordinator (`app/agent/multi_agent.py`) with explicit delegation and observable handoffs.
- [ ] **Milestone 5:** Connect ReAct Engine to `/agent/request` and `/agent/stream/{run_id}` in `app/main.py`.
- [ ] **Milestone 6:** Integrate Human-in-the-Loop approval for write/patch operations (`/agent/approve/{run_id}`).
- [ ] **Milestone 7:** Real Multi-Modal Bug Input handling (image error screenshot analysis via Gemini vision / OCR fallback).
- [ ] **Milestone 8:** Comprehensive Automated Test Suite (`test_agentic_engine.py`) verifying real tool execution, error handling, bounded iterations, and security containment.
- [ ] **Milestone 9:** Frontend Workspace Integration in `console.html` / `app.js` displaying real execution traces and test results.
- [ ] **Milestone 10:** Update all verification audit documents, metrics, and primary README.
