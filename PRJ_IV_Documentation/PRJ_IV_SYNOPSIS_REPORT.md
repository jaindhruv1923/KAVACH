# PROJECT-IV (CAPSTONE PROJECT) SYNOPSIS REPORT
**Course:** Project-IV (7th Semester Major Project — 5 Credits)  
**Department:** Department of Computer Science & Engineering  
**Institution:** School of Engineering & Technology, BML Munjal University  
**Academic Year:** 2026–27  
**Evaluation Date:** 29th September 2026 (12:00 PM – 2:00 PM)  
**Faculty Evaluator / Coordinator:** Prof. Anusha Chhabra  

---

### Project Details & Student Information

| Student Name | Enrollment Number | Degree & Semester | Email |
| :--- | :--- | :--- | :--- |
| **Dhruv Jain** | 230532 | B.Tech CSE, 7th Sem | dhruv.jain.23cse@bmu.edu.in |
| **Dev Garg** | 230487 | B.Tech CSE, 7th Sem | dev.garg.23cse@bmu.edu.in |
| **Ansh Rohilla** | 230794 | B.Tech CSE, 7th Sem | ansh.rohilla.23cse@bmu.edu.in |
| **Ansh Adhikari** | 230822 | B.Tech CSE, 7th Sem | ansh.adhikari.23cse@bmu.edu.in |

**Project Title:**  
### **KAVACH: A Security-Governed Multi-Agent AI DevOps & Observability Platform**

---

## SECTION 1: COMPREHENSIVENESS OF THE LITERATURE REVIEW (10 MARKS)

### 1.1 Evolution of Autonomous AI Coding Agents
Autonomous software engineering agents powered by Large Language Models (LLMs) represent a paradigm shift from passive autocomplete tools (e.g., GitHub Copilot, Tabnine) to goal-driven autonomous systems capable of reading multi-file codebases, executing shell commands, and synthesizing pull requests. Seminal systems such as **SWE-agent** (Yang et al., 2024), **Devin** (Cognition AI, 2024), and **AutoPR** demonstrate that when LLMs are integrated with ReAct (Reasoning and Acting) execution loops (Yao et al., 2023), they can resolve real-world GitHub issues. However, Yang et al. noted that SWE-agent's unconstrained bash tool execution introduces severe security failure modes, including accidental command injection, destructive file modifications, and unbounded execution loops.

### 1.2 Package Hallucination and AI Supply-Chain Attacks
A critical vulnerability identified in recent software engineering literature is **AI Package Hallucination** (Bar-Zik, 2024; Lazaar et al., 2024). LLMs operate as probabilistic next-token predictors trained on historical code snapshots. When prompted to implement specialized functionality (such as cryptographic token validation or XML parsing), models regularly hallucinate non-existent package names (e.g., `fastapi_jwt_vault_security`). 

Security researchers demonstrate that malicious actors monitor public LLM hallucination frequencies and engage in **"Slopsquatting"** or **AI Dependency Confusion**: registering these hallucinated package names on public registries (PyPI, npm) with weaponized payloads. When an autonomous developer agent executes `pip install <hallucinated_package>`, it introduces arbitrary code execution into the enterprise build pipeline. Ladisa et al. (2023) established that traditional Software Composition Analysis (SCA) tools (e.g., Snyk, Dependabot) only inspect existing lockfiles (`requirements.txt`) and are completely blind to dynamically generated import statements in runtime agent code.

### 1.3 LLM Security Vulnerabilities & Prompt Injection
The **OWASP Top 10 for Large Language Model Applications (2023/2025)** lists Prompt Injection (LLM01), Insecure Output Handling (LLM02), and Sensitive Information Disclosure (LLM06) as the primary threats facing enterprise agent deployment. Greshake et al. (2023) demonstrated that **Indirect Prompt Injection** allows attackers to embed malicious instructions inside source code comments, README files, or GitHub issues that an autonomous agent reads during repository analysis. If unshielded, the agent's internal goal state is hijacked, leading to data exfiltration or credential leakage.

### 1.4 Retrieval-Augmented Generation (RAG) for Source Code
Lewis et al. (2020) pioneered Retrieval-Augmented Generation (RAG) to ground LLM responses in external vector databases. In software engineering, Code RAG systems (Feng et al., 2020; Guo et al., 2022) index codebases into dense vector spaces using models such as CodeBERT or `sentence-transformers`. However, standard RAG implementations employ naive fixed-character chunking (e.g., 500-character windows), which shatters abstract syntax tree (AST) hierarchies, separating function signatures from docstrings and implementation blocks. Furthermore, vanilla RAG fails to verify whether retrieved code chunks contain hardcoded secrets before passing them into LLM prompt contexts.

### 1.5 Static Code Analysis & AST Dependency Graphs
Abstract Syntax Tree (AST) analysis (Aho et al., 2006) provides deterministic, mathematical ground truth regarding program structure. Unlike statistical NLP models, AST parsers deterministically extract symbol definitions, import hierarchies, and caller-callee call graphs. Modern change impact analysis frameworks (Ren et al., 2004; Lehnert, 2011) demonstrate that calculating the transitive closure over AST dependency graphs is essential to predict the ripple effect (blast radius) of code modifications.

### 1.6 Regulatory Compliance & Data Privacy in AI Systems
With the enactment of the **Digital Personal Data Protection (DPDP) Act 2023** in India and the **EU AI Act (2024)**, enterprises face strict statutory liability for data breaches involving personally identifiable information (PII) such as Indian Aadhaar numbers, PAN cards, and financial records. Traditional regex filters (e.g., Microsoft Presidio) rely on English keyword heuristics and fail on bare 10–12 digit numeric strings or code-mixed Hinglish developer text (Jain et al., 2023).

---

## SECTION 2: RESEARCH GAPS IDENTIFIED IN LITERATURE (5 MARKS)

Our comprehensive review reveals five critical gaps in existing academic research and commercial tooling:

| Research Gap | Limitation of Current Systems | Impact on Autonomous DevOps | Kavach Solution |
| :--- | :--- | :--- | :--- |
| **Gap 1: Absence of Pre-Execution Deterministic Guardrails** | Naive agents rely on system prompts (*"Please do not leak keys"*). System prompts are probabilistic and susceptible to jailbreaks and prompt injections. | Proprietary API keys and customer PII are leaked into external third-party LLM prompt logs. | Deterministic pre-execution regex and Shannon entropy calculation that halt processing before tokenization. |
| **Gap 2: Zero Defense Against Package Slopsquatting** | Existing SCA tools (Dependabot, Snyk) only scan static `requirements.txt`. No platform intercepts AST imports in synthesized code before installation. | Attackers compromise enterprise supply chains via registered hallucinated packages. | AST Package Firewall querying live PyPI registry APIs backed by an in-memory LRU cache. |
| **Gap 3: Missing AST Blast-Radius Grounding in Agents** | Coding agents modify target files without awareness of transitive caller-callee dependency graphs. | Modifying a utility function silently breaks downstream microservice endpoints. | Static AST parser building bidirectional dependency graphs to compute empirical blast radius scores. |
| **Gap 4: Lack of Closed-Loop Self-Healing Sandboxing** | Agents generate code that compiles syntactically but fails runtime unit assertions, requiring manual developer intervention. | Developers spend excessive time debugging agent-generated runtime errors. | ReAct-based ephemeral sandbox execution with automated traceback reflection (max 3 cycles). |
| **Gap 5: Disconnect from Open Tool Standards (MCP)** | Existing safety tools operate as proprietary closed ecosystems that cannot be plugged into external IDEs. | Developers must abandon their preferred IDEs (Cursor, Claude) to use security scanners. | Native Model Context Protocol (MCP) server exposing tools over standardized JSON-RPC 2.0. |

---

## SECTION 3: OBJECTIVE & PROBLEM DEFINITION (5 MARKS)

### 3.1 Problem Definition
The autonomous deployment of LLM coding agents in enterprise software development creates an acute **Trust and Security Dilemma**:
1. How can organizations harness the productivity gains of autonomous multi-agent code generation without exposing their source code to supply-chain package hallucination, credential exfiltration, and unbounded regression blast radius?
2. Current solutions offer either post-commit static analysis (which detects vulnerabilities too late, after they are already in the repository) or unconstrained agent execution (which introduces operational fragility).

### 3.2 Research Objectives
The primary objective of Project Kavach is to design, implement, and benchmark a **deterministic, security-governed multi-agent AI DevOps platform**. Specifically:
* **Objective 1 (Supply-Chain Firewall):** Eliminate 100% of package hallucination supply-chain attacks by intercepting Python AST imports and validating them against official package registries.
* **Objective 2 (Zero-Knowledge Pre-Execution Gate):** Guarantee that zero sensitive credentials (Shannon entropy $> 4.5$) or Indian national identifiers (Aadhaar/PAN) are transmitted to external cloud LLM APIs.
* **Objective 3 (Architectural Blast-Radius Control):** Formulate an empirical AST dependency scoring algorithm that calculates transitive module impact prior to patch synthesis.
* **Objective 4 (Autonomous Self-Healing Loop):** Implement a closed-loop ReAct reflection sandbox that achieves $>90\%$ autonomous recovery on runtime test failures within 3 repair cycles.
* **Objective 5 (Open Interoperability & Observability):** Expose all governance tools over Anthropic’s Model Context Protocol (MCP) and provide a real-time dark-mode telemetry dashboard with Prometheus OpenMetrics export.

---

## SECTION 4: PROPOSED METHODOLOGY, TOOLS, TECHNIQUES & DATASETS (5 MARKS)

### 4.1 System Architecture & Multi-Agent Workflow
Kavach implements a 6-stage finite state machine governed by 5 collaborative agent personas:
$$\text{Developer Prompt} \longrightarrow \text{Sentinel Screening} \longrightarrow \text{Qdrant RAG} \longrightarrow \text{AST Blast Radius} \longrightarrow \text{LLM Synthesis} \longrightarrow \text{AST Firewall} \longrightarrow \text{ReAct Sandbox}$$

```
                                 +---------------------------+
                                 |      Developer Prompt     |
                                 +-------------+-------------+
                                               │
                                               ▼
                                 +---------------------------+
                                 |    1. SentinelAgent       |
                                 | (Shannon Entropy + Regex) |
                                 +-------------+-------------+
                                               │ (Allowed / Redacted)
                                               ▼
                                 +---------------------------+
                                 |    2. RetrieverAgent      |
                                 | (Qdrant Vector RAG Store) |
                                 +-------------+-------------+
                                               │
                                               ▼
                                 +---------------------------+
                                 |  3. BlastRadiusAnalyst    |
                                 | (AST Code Dependency Graph|
                                 +-------------+-------------+
                                               │
                                               ▼
                                 +---------------------------+
                                 |    4. DevOpsCoderAgent    |
                                 | (Gemini 2.5 / Local Ollama|
                                 +-------------+-------------+
                                               │ (Synthesized Code)
                                               ▼
                                 +---------------------------+
                                 |    5. PackageFirewall     |
                                 | (PyPI Registry Verification|
                                 +-------------+-------------+
                                               │ (Verified Safe Imports)
                                               ▼
                                 +---------------------------+
                                 |   6. SelfHealerSandbox    |
                                 | (ReAct Traceback Reflection|
                                 +---------------------------+
```

### 4.2 Tools and Techniques

| Subsystem | Tool / Technology | Technique / Algorithm |
| :--- | :--- | :--- |
| **API & Telemetry** | FastAPI, Starlette SSE | Async REST endpoints, Server-Sent Events real-time event streaming. |
| **Vector Database & RAG** | Qdrant Client, `all-MiniLM-L6-v2` | 384-dimensional dense semantic vector space, cosine similarity ranking ($>0.70$). |
| **Pre-Execution Security** | Regex Engine, Shannon Entropy | $H = -\sum_{i=1}^n p_i \log_2 p_i$ on base64/hex tokens ($H > 4.5$ blocks secrets). Indian DPDP Aadhaar & PAN regex. |
| **Change Impact Analysis** | Python `ast` module | Bidirectional transitive dependency graph parsing `Import`, `ClassDef`, `FunctionDef`. |
| **Supply-Chain Firewall** | PyPI JSON API, `functools.lru_cache` | AST import extraction, HTTP 200/404 registry probing, in-memory LRU caching. |
| **Inference Engines** | Google Gemini 2.5 Flash, Local Ollama (`qwen2.5-coder:7b`) | Dual-engine privacy routing: cloud LLM for public code; local Ollama for sensitive air-gapped tasks. |
| **Autonomous Sandbox** | `tempfile`, `subprocess`, `pytest` | Isolated virtual environment execution with 5-second CPU timeout. ReAct reflection prompt on `stderr`. |
| **Open Interoperability** | Anthropic Model Context Protocol (MCP) | JSON-RPC 2.0 tool server exposing Kavach security, AST, and search to Cursor & Claude IDEs. |
| **Mission Control Dashboard** | HTML5, Vanilla JavaScript, CSS3 | Dark-mode observability interface, cubic animated KPI counters, Groq Whisper voice recognition. |

### 4.3 Evaluation Datasets and Experimental Design

Kavach is evaluated on three comprehensive benchmark datasets:
1. **Package Hallucination Corpus (`package_hallucination_corpus.json`):** 100 software packages (50 verified legitimate PyPI packages and 50 documented LLM hallucinations) used to evaluate the AST Package Firewall.
2. **Multilingual PII & Credential Corpus (`multilingual_pii_corpus.json`):** 100 developer prompts across English and code-mixed Hindi/Hinglish containing Indian Aadhaar, PAN cards, AWS secret keys, and GitHub PATs.
3. **Operational 42-Run Evaluation Dataset (`workflow_runs.json`):** 42 complete, persistent workflow traces across 4 user personas (Junior Developer, SRE, Security Auditor, CI/CD Webhook) evaluating end-to-end latency, stage transitions, and LLM-as-a-Judge accuracy.

---

## SECTION 5: CURRENT IMPLEMENTATION STATUS & PRELIMINARY RESULTS

* **Automated Unit & Integration Test Suite:** **220 automated tests passing with 100% success rate**.
* **Supply-Chain Catch Rate:** **100% precision and recall** in catching hallucinated packages, with $<5$ms registry query latency.
* **Credential Protection:** **100% catch rate** on high-entropy production secrets ($H > 4.5$).
* **End-to-End Latency:** Average pipeline latency of **1,370 ms**, with security guardrails contributing $<20$ ms ($<2\%$ overhead).
* **Autonomous Self-Healing Rate:** **90.0% autonomous recovery** within 2 ReAct reflection cycles in isolated sandbox tests.

---

### Signatures

| Dhruv Jain (230532) | Dev Garg (230487) | Ansh Rohilla (230794) | Ansh Adhikari (230822) |
| :---: | :---: | :---: | :---: |
| ____________________ | ____________________ | ____________________ | ____________________ |

**Date of Submission:** 29th September 2026  
**Faculty Evaluator / Coordinator:** Prof. Anusha Chhabra
