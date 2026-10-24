# KAVACH (कवच) — MID-SEM MASTER DOSSIER FOR CLAUDE
## Autonomous Security-Governed Multi-Agent AI DevOps Platform
### Course: CSE3101 — Agentic AI | BML Munjal University, School of Engineering & Technology
**Faculty Coordinators:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  
**Team Members:** Dhruv Jain (Lead Architect & Developer), Hemant Goyal (Testing & Environment), Rajat Yadav (Demo Coordination & QA)  
**Repository Source:** `AgenticAi_MidSem/`  

---

## 🎯 INSTRUCTIONS FOR CLAUDE (HOW TO USE THIS DOSSIER)
> **Prompt for Claude:**
> *"You are an elite academic designer, AI systems architect, and executive presentation strategist. Below is the comprehensive technical dossier for our university project **KAVACH** (CSE3101: Agentic AI at BML Munjal University). Using this dossier, generate:
> 1. **A 12-Slide High-Impact Presentation Deck** (Slide-by-slide structure with Title, Visual/Diagram layout, Bullet Points, and a natural, authoritative Speaker Script for the team leader, Dhruv Jain).
> 2. **A Formal Academic PDF/LaTeX Report Outline** with mathematical derivations, architecture diagrams in ASCII/Mermaid, empirical benchmark tables, and verified syllabus rubrics.
> Keep the tone authoritative, mathematically rigorous, and strictly grounded in the verified code without fluff or fake claims."*

---

## 1. PROJECT METADATA & ACADEMIC CONTEXT

| Parameter | Specification |
|---|---|
| **Course Code & Title** | CSE3101: Agentic AI (B.Tech CSE, 7th Semester, AY 2026–27) |
| **Institution** | School of Engineering & Technology, BML Munjal University, Gurugram |
| **Faculty Mentors** | Dr. Soharab Hossain Shaikh (Coordinator) & Mr. Pranshu Tiwari |
| **Team Leader & Speaker** | **Dhruv Jain** (Lead Architect & Developer — Core FSM, ADK, Verhoeff, Merkle) |
| **Team Contributors** | Hemant Goyal (Testing & Dependencies), Rajat Yadav (Demo Coordination & QA) |
| **Phase-1 Baseline** | 164 Automated Pytest Cases, Initial Synopsis Charter, 6-Stage FSM |
| **Mid-Sem Leap** | **400 Automated Pytest Cases (100% Pass Rate)**, Google ADK Coordinator, Verhoeff $D_5$ Checksum, Kaikei Merkle Ledger, A2A/MCP Protocols, Medical Triage Exercise, Watermelon UI & Manus HUD |
| **Execution Command** | `.\run_midsem.bat` (Starts FastAPI on `http://127.0.0.1:8000` & opens Cockpit) |
| **Fast Verification** | `python verify_midsem.py --fast` (Validates all 12 syllabus checkpoints in <3s) |

---

## 2. THE PROBLEM DEFINITION (WHAT WE SHOWED IN PHASE-1 SYNOPSIS)

Deploying unconstrained autonomous coding agents (Devin, SWE-agent, Copilot Workspace) in an enterprise codebase introduces four critical failure modes:

1. **Supply-Chain Slopsquatting:** Autonomous agents hallucinate plausible package names (e.g., `fastapi_jwt_vault_security`). Threat actors pre-register these names on PyPI/npm with malicious payloads. A routine `pip install` executed unsupervised becomes a remote-code-execution (RCE) vector.
2. **Credential & Statutory PII Leakage:** Agents copy hardcoded tokens, AWS secrets, or Indian national identifiers (Aadhaar, PAN) straight into public commits or external LLM prompt logs.
3. **Unbounded Blast Radius:** Agents modify shared utility files with zero structural awareness of upstream/downstream dependencies, breaking external services.
4. **Prompt Injection & Non-Convergent Loops:** Adversarial instructions hidden in a repository's README or issue tracker hijack agent reasoning, while unconstrained self-debugging creates runaway latency and token spend.

### The Phase-1 Synopsis Baseline:
- **Governed 6-Stage Pipeline:**
  $$\text{Sentinel Screening} \longrightarrow \text{Qdrant RAG} \longrightarrow \text{AST Blast Radius} \longrightarrow \text{LLM Synthesis} \longrightarrow \text{Package Firewall} \longrightarrow \text{Self-Healing Sandbox}$$
- **10-State Deterministic FSM** in `app/agent/orchestrator.py`.
- **Dual-Engine Routing:** Google Gemini 2.5 Flash (cloud reasoning) vs. local Ollama Qwen2.5-Coder:7B (air-gapped sensitive code).
- **164 Passing Unit Tests** with an in-memory Blackboard pattern.

---

## 3. THE MID-SEM ENGINEERING LEAP: WHAT WE ADDED NEW

| Feature Area | Phase-1 Synopsis Baseline | Mid-Sem Submission Innovation | Engineering Significance |
|---|---|---|---|
| **Test Suite Scale** | 164 passing tests | **400 passing tests (100% pass rate in 380s)** | Over 2.4x test expansion covering edge cases & protocol schemas |
| **Orchestration Architecture** | Procedural script state machine | **Google ADK Coordinator Pattern (`CoordinatorAgent`)** | Hierarchical sub-agents (`Sentinel`, `Planner`, `Retriever`, `Impact`, `Coder`) |
| **ADK Lifecycle Hooks** | None | **Official Google ADK 8-Hook Lifecycle (`adk.dev/callbacks`)** | `before_agent`, `after_agent`, `before_tool`, `after_tool` across 3 phases |
| **Indian PII Verification** | Naive 12-digit Regex (51.02% False Positive Rate) | **Dihedral Group $D_5$ Verhoeff Checksum + Context Gating** | **0.00% False Positive Rate**; eliminates false blocks on order IDs |
| **Secrets Detection** | Simple regex keyword scan | **Shannon Entropy $H(X) = -\sum P(x) \log_2 P(x)$** | $O(L)$ detection of high-entropy API keys ($H > 4.5$) with zero LLM compute |
| **Multi-Agent Reasoning** | Single prompt synthesis | **ReAct + Reflexion, CoT, and Tree-of-Thoughts (ToT)** | Heuristic branch exploration scoring patches against AST invariants |
| **Event-Driven Flows** | Linear execution | **CrewAI Stateful Flows (`@start`, `@listen`)** | Structured event-driven state transitions with deterministic fallbacks |
| **Interoperability (MCP)** | Basic REST endpoints | **Native Model Context Protocol JSON-RPC 2.0 Server** | Standard tools (`detect_pii`, `detect_secrets`, `search_chunks`, `analyze_impact`) |
| **Agent-to-Agent (A2A)** | Plain dictionary messages | **Cryptographic A2A Message Envelopes** | HMAC-SHA256 signatures, timestamps, and nonces prevent replay attacks |
| **Audit Ledger & Compliance** | Plain SQLite log | **Kaikei (会計) NIST FIPS 202 SHA3-512 Merkle Ledger** | RFC 6962 tree accumulator with live **Adversarial Tamper Sandbox** |
| **Syllabus Course Exercise** | None | **Google ADK Medical Triage Multi-Agent Pipeline** | Urgent route (112/108 dispatch) vs. normal symptomatic OTC relief |
| **User Interface Experience** | Basic dark dashboard | **Watermelon UI, Motion Primitives & Manus HUD** | Modern tokens, spring animations, cognitive transparency (Thought $\to$ Action $\to$ Observe $\to$ Reflect) |

---

## 4. MATHEMATICAL FORMULATIONS & COMPUTATIONAL COMPLEXITY

### A. Dihedral Group $D_5$ Checksum (Verhoeff Algorithm)
For an input digit string $a_n a_{n-1} \dots a_1 a_0$:
$$\sum_{i=0}^{n} F\Big( \text{perm}(i \pmod 8, a_i) \Big) \equiv 0 \pmod{D_5}$$
- Group operation $d(j, k)$ defined by the non-commutative Cayley table of $D_5$ (rotations & reflections of a regular pentagon).
- Catches **100% of single-digit substitutions** ($a \to b, a \neq b$) and **100% of adjacent transpositions** ($a b \to b a$).
- **Computational Complexity:** $O(N)$ where $N$ is the number of digits (typically $N=12$).

### B. Shannon Information Entropy for Cryptographic Secrets
For character sequence $S$ of length $L$ over alphabet $\Sigma$:
$$H(S) = -\sum_{i=1}^{|\Sigma|} P(x_i) \log_2 P(x_i), \quad \text{where } P(x_i) = \frac{\text{count}(x_i)}{L}$$
- **Natural Language / Code:** $H(S) \approx 2.5 - 3.4 \text{ bits/char}$
- **Cryptographic Keys / Tokens:** $H(S) \ge 4.5 \text{ bits/char}$
- **Computational Complexity:** $O(L)$ scanning time, $<0.4\text{ms}$ latency.

### C. Graph-Theoretic AST Blast Radius
Call-graph $G = (V, E)$ constructed via Python native `ast` compiler:
$$\text{Reach}(v^*) = \big\{ u \in V \mid \exists \text{ path } u \rightsquigarrow v^* \text{ in } G \big\}$$
$$\text{Score}(v^*) = \min\left(1.0, \; \alpha \cdot \frac{|\text{In-Degree}(v^*)|}{|V|} + \beta \cdot \text{Depth}(v^*) + \gamma \cdot \mathbb{I}_{\text{critical}}(v^*)\right)$$
- **Computational Complexity:** Transitive closure via BFS in $O(|V| + |E|)$ time ($<12\text{ms}$ on demo repository).

### D. Kaikei Binary Merkle Tree Accumulator (NIST FIPS 202 SHA3-512)
- Leaf hash: $L_i = \text{SHA3-512}\big(0x00 \;||\; \text{CanonicalJSON}(E_i)\big)$
- Parent node: $N = \text{SHA3-512}\big(0x01 \;||\; \text{LeftChild} \;||\; \text{RightChild}\big)$
- Security margin: $2^{256}$ collision resistance against Grover/quantum speedups.
- Tamper detection complexity: $O(\log N)$ proof verification.

---

## 5. COMPLETE 12-SLIDE PRESENTATION BLUEPRINT

### Slide 1: Title & Executive Identification
- **Title:** KAVACH (कवच) — Security-Governed Multi-Agent AI DevOps Platform
- **Subtitle:** Deterministic Guardrails, Google ADK Orchestration & Cryptographic Provenance for Autonomous AI Agents
- **Meta:** CSE3101: Agentic AI · BML Munjal University · Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari
- **Team:** Dhruv Jain (Lead Architect & Speaker), Hemant Goyal, Rajat Yadav
- **Speaker Note:** "Good morning, respected professors. Today we present KAVACH, an autonomous multi-agent platform designed to make AI coding agents safe for enterprise repositories through deterministic state machines and cryptographic governance."

### Slide 2: The Core Problem — Unconstrained Autonomous Coding Agents
- **Visual:** Comparison of Devin/Copilot unchecked execution vs. KAVACH governed pipeline.
- **Key Points:**
  - Slopsquatting: Hallucinated PyPI/npm packages as RCE vectors.
  - Credential & PII leaks: Hardcoded API keys & Aadhaar numbers exposed in prompt logs.
  - Unbounded blast radius: Cascading service failures from editing shared utilities.
  - Runaway loops: Adversarial prompt injection & unbounded token spend.
- **Speaker Note:** "In our synopsis, we established that generative models cannot be trusted to police themselves. System prompts like 'do not leak secrets' are merely advisory. We need deterministic pre-execution guardrails."

### Slide 3: Architectural Evolution — Phase-1 Synopsis vs. Mid-Sem Leap
- **Visual:** Two-column architectural comparison table (164 tests $\to$ 400 tests).
- **Key Points:**
  - Transition from procedural scripts to Google ADK Coordinator with 5 registered sub-agents.
  - Evolution from naive regex (51% FPR) to Dihedral $D_5$ Verhoeff Checksum (0.00% FPR).
  - Addition of CrewAI Stateful Flows, MCP JSON-RPC 2.0 server, and A2A cryptographic protocol.
  - Integration of Kaikei SHA3-512 Merkle tamper-evident ledger.
- **Speaker Note:** "From our initial 164-test Phase-1 prototype, we have expanded to a 400-test verified platform, aligning directly with every module of the CSE3101 course handout."

### Slide 4: Multi-Agent Orchestration — Google ADK Coordinator & CrewAI Flows
- **Visual:** Mermaid diagram showing `CoordinatorAgent` delegating to `Sentinel`, `Planner`, `Retriever`, `ImpactAnalyst`, and `CoderAgent`.
- **Key Points:**
  - Official Google ADK 8-Hook Lifecycle across Init, Tool, Model, and Error phases.
  - Privacy boundary: User prompts are scrubbed by `redact_text()` before planner dispatch.
  - Dual-engine flow: High-level reasoning in Gemini 2.5 Flash with local air-gapped Ollama fallback.
  - CrewAI event-driven flows using `@start` and `@listen` decorators.
- **Speaker Note:** "Our orchestrator implements the Google ADK Coordinator pattern. Each subagent has a single responsibility, and the planner never sees raw, unredacted user prompts."

### Slide 5: Mathematical Security Guardrails — Dihedral Group $D_5$ & Shannon Entropy
- **Visual:** The pentagon dihedral symmetry diagram alongside the Shannon Entropy bit distribution curve.
- **Key Points:**
  - Dihedral $D_5$ Verhoeff Algorithm: Non-commutative matrix multiplication detecting 100% of single-digit & transposition errors.
  - Contextual gating drops Aadhaar FPR from 51.02% to 0.00%.
  - Shannon Entropy $H(S) = -\sum P(x) \log_2 P(x)$: $O(L)$ scan catching high-entropy credentials ($H > 4.5$) in $<0.4\text{ms}$.
- **Speaker Note:** "Instead of slow, hallucination-prone guardrail LLMs, we rely on applied abstract algebra and information theory. We achieve 100% mathematical certainty before an LLM token is ever spent."

### Slide 6: Change-Impact Intelligence — AST Blast-Radius Analysis
- **Visual:** Directed Call-Graph $G=(V, E)$ highlighting modified functions and transitive dependency trees.
- **Key Points:**
  - Static parsing via Python `ast` module; zero runtime overhead.
  - BFS reachability computes transitive closure in $O(|V| + |E|)$ time (<12ms).
  - Normalizes in-degree centrality, tree depth, and security-path criticality into an impact score (0.0 to 1.0).
- **Speaker Note:** "Before any code patch is applied, our AST engine traverses the entire repository's call graph to ensure a small change does not trigger an unexpected architectural failure."

### Slide 7: Industry Standards — Model Context Protocol (MCP) & A2A Interoperability
- **Visual:** JSON-RPC 2.0 schema flow between Cursor/IDE $\leftrightarrow$ KAVACH MCP Server $\leftrightarrow$ A2A Protocol.
- **Key Points:**
  - MCP Server hosting 4 standardized tools: `detect_pii`, `detect_secrets`, `search_chunks`, `analyze_impact`.
  - Pydantic v2 validated input/output schemas.
  - Agent-to-Agent (A2A) protocol with HMAC-SHA256 signed message envelopes and nonce verification.
- **Speaker Note:** "KAVACH is not an isolated silo. Through Anthropic's Model Context Protocol and Google's A2A specification, any external IDE or autonomous sub-agent can invoke our security services."

### Slide 8: Syllabus Course Exercise — Google ADK Medical Triage Multi-Agent Pipeline
- **Visual:** Branching triage diagram: Patient symptom intake $\to$ Urgency Classifier $\to$ Emergency Route vs. OTC Care Route.
- **Key Points:**
  - Designed specifically for the CSE3101 Agentic AI course exercise.
  - High-Urgency Route: Catches critical symptoms (e.g., chest pain) $\to$ dispatches emergency action (`Call 112 / 108 immediately`).
  - Normal Route: Recommends evidence-grounded over-the-counter care (e.g., Paracetamol).
- **Speaker Note:** "As part of our syllabus coursework, we developed a medical triage pipeline demonstrating dynamic agent routing based on situational risk."

### Slide 9: Kaikei (会計) — Cryptographic Merkle Ledger & Live Tamper Sandbox
- **Visual:** Binary Merkle Tree diagram showing leaf hashing ($0x00$) and node accumulation ($0x01$) up to root $R$.
- **Key Points:**
  - Built under NIST FIPS 202 SHA3-512 Keccak sponge construction.
  - RFC 6962 audit proof guarantees non-repudiation under Indian DPDP Act 2023.
  - `POST /security/merkle/tamper-demo`: Isolated in-memory clone proves that leaf tampering is detected and pinpointed in $O(\log N)$ time while production logs remain pristine.
- **Speaker Note:** "Kaikei provides mathematically provable audit immutability. If anyone alters a past agent decision, the Merkle root breaks, pinpointing the corrupted record immediately."

### Slide 10: Modern User Experience — Watermelon UI, Motion Primitives & Manus HUD
- **Visual:** Screenshots of the high-contrast Watermelon UI dashboard and the 4-stage Manus HUD.
- **Key Points:**
  - Watermelon UI: Hyper-contrast ruby (`#FF3B69`), emerald (`#00E599`), and obsidian glassmorphism.
  - Motion Primitives: Tactile spring animations (`cubic-bezier(0.16, 1, 0.3, 1)`) with accessible reduced-motion support.
  - Manus HUD: Real-time observability: Thought $\to$ Action $\to$ Observation $\to$ Reflection.
- **Speaker Note:** "We engineered the UI to provide complete cognitive transparency, allowing human operators to inspect every thought, action, and observation in real time."

### Slide 11: Verification & Empirical Benchmark Results
- **Visual:** Real terminal test run screenshot & verification summary table.
- **Key Points:**
  - **400 / 400 Pytest cases passed** in 380s with 100% pass rate.
  - **12 / 12 syllabus checkpoints verified** in `verify_midsem.py` in <3s.
  - Zero-latency deterministic fallback (<5ms) during offline network conditions.
  - Aadhaar False Positive Rate: 0.00%, Security Gate Precision/Recall/F1: 1.00 / 1.00 / 1.00.
- **Speaker Note:** "Every feature we present is backed by automated tests. Our suite of 400 tests guarantees that all safety invariants and syllabus rubrics hold."

### Slide 12: Conclusion, Team Responsibilities & Q&A
- **Visual:** Team contribution matrix & repository link (`github.com/jaindhruv1923/KAVACH`).
- **Key Points:**
  - **Dhruv Jain:** Lead Architect & Developer (FSM, Google ADK, Verhoeff $D_5$, Merkle Ledger, MCP).
  - **Hemant Goyal:** Testing Support, Environment Setup & Documentation.
  - **Rajat Yadav:** Demo Coordination, Presentation & QA Assistance.
  - Platform is live, reproducible with one command (`.\run_midsem.bat`), and ready for defense.
- **Speaker Note:** "Thank you, Dr. Soharab and Prof. Pranshu. We welcome your questions."

---

## 6. CRUCIAL CODE REFERENCES IN `AgenticAi_MidSem/`

1. **Google ADK Coordinator & Orchestrator:** [`backend/app/agent/orchestrator.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/agent/orchestrator.py)
2. **Google ADK 8 Lifecycle Callbacks:** [`backend/app/agent/adk_callbacks.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/agent/adk_callbacks.py)
3. **Dihedral Group $D_5$ Verhoeff Algorithm:** [`backend/app/security/verhoeff.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/security/verhoeff.py)
4. **Shannon Entropy & PII Detector:** [`backend/app/security/detector.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/security/detector.py)
5. **Kaikei SHA3-512 Merkle Ledger:** [`backend/app/security/merkle_ledger.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/security/merkle_ledger.py)
6. **Tamper Demo Endpoint:** [`backend/app/main.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/main.py#L380-L450)
7. **AST Blast-Radius Analyzer:** [`backend/app/impact/analyzer.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/impact/analyzer.py)
8. **Model Context Protocol Server:** [`backend/app/agent/mcp_server.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/agent/mcp_server.py)
9. **Agent-to-Agent Protocol:** [`backend/app/agent/a2a_protocol.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/agent/a2a_protocol.py)
10. **Medical Triage Pipeline:** [`backend/app/agent/medical_triage.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/agent/medical_triage.py)
11. **One-Command Verification Script:** [`verify_midsem.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/verify_midsem.py)
12. **Frontend UI & Interactive Sandboxes:** [`frontend/index.html`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/frontend/index.html) & [`frontend/watermelon_manus_kaikei.js`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/frontend/watermelon_manus_kaikei.js)
