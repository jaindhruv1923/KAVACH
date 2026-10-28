# KAVACH: Viva Defense Code Map & Technical Architecture Grounding

**Document Purpose:** Oral examination defense guide mapping tough viva questions directly to exact file paths, line numbers, architectural trade-offs, and grounded answers.  
**Structure:** The Top 10 Hardest-To-Explain Pieces First, followed by remaining architectural components.

---

## Part 1: Top 10 Hardest-to-Explain Implementation Pieces

---

### 1. Rule-Based Task Planner (`app/agent/planner.py:19-54`)
* **Code Location:** `01_KAVACH_Platform/backend/app/agent/planner.py`, Lines 19–54
* **Implementation Reality:** Task planning uses a dictionary of regex keywords (`_TASK_KEYWORDS`: `auth`, `password`, `test`, `api`, `database`) to decompose prompts. It does **not** call an LLM.
* **Why It Was Built This Way (Architectural Rationale):**
  Building the orchestrator's core state machine, RAG vector retrieval plumbing, and security inspection gates must be testable deterministically. An LLM call at the planning stage introduces non-deterministic outputs, API latency, and rate limits that make regression testing flaky.
* **Examiner Trap Question:** *"Why does your agent use regex instead of an LLM for planning? Is this really an AI agent?"*
* **Bulletproof Viva Answer:**
  > *"KAVACH is primarily a security governance platform that wraps around AI pipelines. In Phase 2, we deliberately isolated the state machine and policy gates from external API non-determinism. The `plan_request()` interface was designed with a pluggable signature so that an LLM call (such as a local Ollama model) can be dropped in without changing a single line in the orchestrator. For empirical testing and reproducible defense, rule-based decomposition guarantees deterministic pipeline execution."*

---

### 2. Immediate Halt on `REVIEW` Policy Verdict (`app/agent/orchestrator.py:68-73`)
* **Code Location:** `01_KAVACH_Platform/backend/app/agent/orchestrator.py`, Lines 68–73 & `app/security/policy_engine.py:75-115`
* **Implementation Reality:** If the risk-adaptive policy engine returns `PolicyAction.REVIEW`, the orchestrator immediately halts the workflow, advances to `WorkflowStage.NEEDS_REVIEW`, and exits without proceeding to planning or generation.
* **Why It Was Built This Way (Architectural Rationale):**
  In high-assurance security engineering (e.g. banking or defense), a prompt requiring human review must **never** be executed autonomously. Until an authenticated supervisor provides cryptographic approval, the safe default is fail-closed.
* **Examiner Trap Question:** *"What is the difference between BLOCK and REVIEW if both stop execution immediately?"*
* **Bulletproof Viva Answer:**
  > *"Both halt autonomous execution immediately to prevent data leaks. However, their terminal state semantics differ: `BLOCK` is a permanent rejection (e.g., critical AWS credentials or plain-text national IDs). `NEEDS_REVIEW` is a paused state that can be unblocked by a supervisor calling the `resume_workflow()` endpoint (`POST /agent/runs/{run_id}/resume`) with a valid auditor ID and cryptographic justification."*

---

### 3. Shannon Entropy Secret Calculation ($H > 4.5$) (`app/security/secret_detector.py:38-65`)
* **Code Location:** `01_KAVACH_Platform/backend/app/security/secret_detector.py`, Lines 38–65
* **Implementation Reality:** Calculates mathematical Shannon entropy $H = -\sum_{i=1}^n p_i \log_2 p_i$ on tokens with length $\ge 16$. Tokens exceeding $4.5$ bits per character are flagged as `HIGH_ENTROPY_SECRET`.
* **Why It Was Built This Way (Architectural Rationale):**
  Attackers and developers frequently obfuscate credential variable names (e.g., `x = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"`). Pure regex matching on names like `aws_secret` misses renamed tokens. Random cryptographic keys have high character entropy compared to natural English language ($H \approx 2.5 - 3.5$).
* **Examiner Trap Question:** *"Why exactly is the threshold 4.5? Doesn't a high threshold miss short passwords or cause false positives on UUIDs?"*
* **Bulletproof Viva Answer:**
  > *"Natural language text typically exhibits an entropy between 2.5 and 3.5 bits per symbol, whereas base64 and hex-encoded cryptographically random keys exceed 4.5. We combine entropy with a minimum length requirement ($\ge 16$ characters) and contextual regexes to filter out standard GUIDs or camelCase identifiers, achieving sub-0.05ms execution with zero false negatives on standard API keys."*

---

### 4. Context Sanitization for Indirect Prompt Injection (`app/security/injection_shield.py:30-85`)
* **Code Location:** `01_KAVACH_Platform/backend/app/security/injection_shield.py`, Lines 30–85 & `orchestrator.py:101-122`
* **Implementation Reality:** Scans RAG-retrieved repository chunks for prompt injection triggers (e.g., `"ignore previous instructions"`, system prompt delimiters, or jailbreak roleplay). If detected, replaces the chunk content with `[SANITIZED REPO CONTEXT: ...]`.
* **Why It Was Built This Way (Architectural Rationale):**
  Indirect Prompt Injection is OWASP LLM #1. An attacker can plant malicious instructions inside an untrusted repository file or issue description. When RAG retrieves this file, the instruction hijacks the LLM. Sanitizing the chunk *in memory* before feeding it to the prompt construction engine neutralizes the attack vector.
* **Examiner Trap Question:** *"Why not just block the entire workflow when an injection pattern is found in the repo?"*
* **Bulletproof Viva Answer:**
  > *"Repositories frequently contain test files, security scanners, or documentation that legitimately mention injection patterns. Completely blocking the developer request would cause severe availability loss. Instead, KAVACH sanitizes the malicious chunk in the context window while allowing benign chunks to ground the generation."*

---

### 5. In-Repo Emulation of Google ADK & CrewAI (`app/adk/` & `app/crew/`)
* **Code Location:** `01_KAVACH_Platform/backend/app/adk/agent.py:39-120` & `app/crew/agents.py:10-60`
* **Implementation Reality:** The platform implements Google ADK's 8-hook callback architecture and CrewAI's role/goal delegation patterns using pure Python classes written from scratch in the repository. Neither `google-adk` nor `crewai` is imported as an external pip package.
* **Why It Was Built This Way (Architectural Rationale):**
  External agentic frameworks (CrewAI, LangChain, AutoGen) pull in dozens of heavy dependencies, introduce breaking API changes every few weeks, and execute arbitrary code without sandboxing. Authoring native in-repo pattern implementations provides total control over the 8 hook checkpoints (`before_agent`, `before_model`, `before_tool`, etc.) with zero external dependency bloat.
* **Examiner Trap Question:** *"Did you actually use Google ADK and CrewAI, or did you write fake versions?"*
* **Bulletproof Viva Answer:**
  > *"We authored clean in-repo architectural emulations that precisely match the specification contracts of Google ADK and CrewAI. External packages were intentionally omitted to eliminate dependency bloat and security risks from third-party supply chains. Our `LlmAgent` and `CrewAgent` classes implement the exact lifecycle states, 8-hook callbacks, and tool execution boundaries required by the syllabus."*

---

### 6. AST Dependency Analysis & Blast Radius (`app/impact/analyzer.py` & `dependency_graph.py`)
* **Code Location:** `01_KAVACH_Platform/backend/app/impact/dependency_graph.py:14-58` & `analyzer.py:26-95`
* **Implementation Reality:** Uses Python's native `ast.parse()` to build a directed graph of module imports and class/function definitions. Computes transitive dependencies and merges them with semantic vector hits to generate a blast radius score between 0.0 and 1.0.
* **Why It Was Built This Way (Architectural Rationale):**
  Semantic similarity alone can be misleading: changing a utility function might semantically resemble a math module, but its code is imported by the authentication router. Combining explicit AST graph imports ($25\%$ weight) with semantic RAG search ($75\%$ weight) guarantees both topical relevance and structural safety.
* **Examiner Trap Question:** *"Why did `analyze_impact` take 34 seconds when tested on cold start?"*
* **Bulletproof Viva Answer:**
  > *"On a cold start, if the vector database has 0 points, `analyze_impact` triggers a bootstrap repository ingestion. Loading the `sentence-transformers` neural weights and tokenizers takes ~30 seconds on consumer hardware. Once the vector database is warm, the pure AST dependency extraction executes in under 48 milliseconds."*

---

### 7. Graceful Degradation in Vector Retrieval (`app/rag/embed_store.py:65-110`)
* **Code Location:** `01_KAVACH_Platform/backend/app/rag/embed_store.py`, Lines 65–110
* **Implementation Reality:** If the Qdrant client connection fails, or if the collection is uninitialized, `search()` catches the exception and returns an empty list `[]`, logging the incident to `WorkflowRun.history` without raising an unhandled exception.
* **Why It Was Built This Way (Architectural Rationale):**
  In DevOps systems, vector search outages must not bring down the entire security gateway. If RAG is unavailable, KAVACH degrades gracefully: the code generator receives a prompt indicating no repository context is available, and pre-execution regex guardrails continue protecting the platform.
* **Examiner Trap Question:** *"If RAG fails, isn't the generated code ungrounded and dangerous?"*
* **Bulletproof Viva Answer:**
  > *"Yes, without RAG context the model cannot inspect project APIs. That is why the generator prompt explicitly instructs: 'If the evidence is insufficient to safely implement the request, say so explicitly instead of guessing.' Furthermore, the output security gate and AST syntax validator run regardless of whether RAG succeeded."*

---

### 8. Saga Distributed Transaction Pattern in Bharat Bank (`implementation_banks/server.py:120-195`)
* **Code Location:** `02_Banking_and_Results_Dashboard/implementation_banks/server.py`, Lines 120–195
* **Implementation Reality:** Multi-step inter-bank transfers execute through a Saga coordinator with forward actions (`debit_source`, `credit_destination`) and compensating rollback actions (`refund_source`).
* **Why It Was Built This Way (Architectural Rationale):**
  Autonomous agents executing financial transactions across microservices cannot use distributed locking across external systems. The Saga pattern guarantees eventual consistency without long-held database locks.
* **Examiner Trap Question:** *"How does Bharat Bank prevent double-spending if an agent crashes midway through a transfer?"*
* **Bulletproof Viva Answer:**
  > *"Every transfer requires an `idempotency_key`. If the forward action fails at the destination bank or a timeout occurs, the Saga orchestrator executes backward compensating transactions, reversing debits and emitting a cryptographic Merkle audit event."*

---

### 9. Secondary Leakage Prevention via Audit Redaction (`app/security/audit_redaction.py:15-60`)
* **Code Location:** `01_KAVACH_Platform/backend/app/security/audit_redaction.py`, Lines 15–60
* **Implementation Reality:** Before storing developer input in `WorkflowRun`, the text is sanitized via `redact_text()`. Sensitive strings like `Aadhaar 9876 5432 1098` become `Aadhaar 9876-XXXX-1098`.
* **Why It Was Built This Way (Architectural Rationale):**
  Security audit logs frequently become the primary attack target (CWE-532). If an agent intercepts a leaked credit card or password and logs the raw string in its run history, the audit database becomes a secondary leak channel.
* **Examiner Trap Question:** *"If you redact the input, how can an auditor verify what actually caused the block?"*
* **Bulletproof Viva Answer:**
  > *"KAVACH uses structured masking rather than total erasure: the first 4 and last 4 digits are preserved while middle bytes are masked. This allows compliance auditors to verify card/identity prefixes while ensuring that the data in the audit database cannot be used for fraud."*

---

### 10. Passthrough Unwired Stages & Zero Disk Writes (`app/agent/state.py:25-27`)
* **Code Location:** `01_KAVACH_Platform/backend/app/agent/state.py:25-27` & `orchestrator.py:178-183`
* **Implementation Reality:** `TEST_GENERATION`, `BUILD_AND_TEST`, and `CICD_GATE` exist in `WorkflowStage` but are marked passthrough. The orchestrator never writes files to the workspace or invokes `pytest` during an agent run.
* **Why It Was Built This Way (Architectural Rationale):**
  Allowing an autonomous LLM agent to write directly to developer files without human approval introduces immense risk. Restricting the output to an in-memory JSON response ensures that KAVACH acts as an advisory and inspection firewall, not an unconstrained filesystem actuator.
* **Examiner Trap Question:** *"Why are test generation and CI/CD gates listed in the stage enum if they are not implemented?"*
* **Bulletproof Viva Answer:**
  > *"They represent the full lifecycle architecture defined in the Phase-1 Blueprint. In our implementation, we prioritized perfecting the pre-execution security gates, AST impact analysis, and RAG grounder. The unwired stages are formally documented in our Single Source of Truth (`METRICS.json`) as roadmap passthroughs rather than falsely claiming automated execution."*

---

## Part 2: Remaining Architectural Components

### 11. PII Detection Engine (`app/security/detector.py:48-120`)
* **Core Logic:** Regex scanning for PAN (`[A-Z]{5}[0-9]{4}[A-Z]`), Aadhaar (`\b\d{4}\s\d{4}\s\d{4}\b`), Indian phone (`(\+91[\-\s]?)?[6-9]\d{9}`), and bank accounts (`\b\d{9,18}\b`).
* **Empirical Performance:** Median latency 0.017 ms. 100% recall on 45 held-out samples. 3 false positives on 10-digit order/SKU codes (fail-safe by design).

### 12. Air-Gapped Mode & LLM Client (`app/generation/llm_client.py:45-165`)
* **Core Logic:** Dispatches requests to Google Gemini API when `GEMINI_API_KEY` is present. When `AIR_GAPPED_MODE=true`, routes to local Ollama HTTP REST endpoint (`/api/generate`). In test/offline mode, returns a labeled deterministic stub.

### 13. PyPI Package Hallucination Defense (`app/security/package_verifier.py:35-90`)
* **Core Logic:** When an LLM generates `import` or `pip install` commands, KAVACH intercepts the package names, checks a local trusted cache, and queries `https://pypi.org/pypi/{pkg}/json` to detect hallucinated or typosquatted packages before installation.

### 14. Model Context Protocol (MCP) Server (`app/mcp/server.py:25-80`)
* **Core Logic:** Implements JSON-RPC 2.0 protocol over HTTP. Exposes KAVACH security scanners (`detect_pii`, `detect_secrets`, `analyze_impact`) as standard tools accessible by external MCP clients (such as Claude Desktop or Cursor).
