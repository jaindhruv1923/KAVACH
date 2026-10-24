# KAVACH — CrewAI & Google ADK Architecture, Structure & Implementation Dossier
**CSE3101: Agentic AI — Mid-Sem Evaluation & Defense Reference**  
**Faculty Evaluators:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  
**Student:** Dhruv Jain | Department of Computer Science & Engineering, BML Munjal University  

---

## 1. Executive Summary & Verification Status

| Component | Standard / Framework | File Location | Test Suite Verification |
| :--- | :--- | :--- | :--- |
| **CrewAI Agents & Crews** | CrewAI Framework (Module 3) | [`backend/app/crew/agents.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/crew/agents.py) | **100% Pass** (`test_crewai_specialized_agents`, `test_crewai_crew_execution`) |
| **CrewAI Stateful Flows** | `@start`, `@listen`, `@router` | [`backend/app/crew/flows.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/crew/flows.py) | **100% Pass** (`test_crewai_flows_stateful_automation`) |
| **Google ADK Core** | Google Agent Development Kit (`adk.dev`) | [`backend/app/adk/agent.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/adk/agent.py) | **100% Pass** (`test_adk_agent_lifecycle_and_tools`) |
| **Google ADK Callbacks** | 8-Hook Points & 8 Canonical Patterns | [`backend/app/adk/callbacks.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/adk/callbacks.py) | **100% Pass** (`test_adk_all_eight_hook_points`, Patterns 01–08) |
| **Medical Triage Pipeline** | CSE3101 course exercise (not part of the banking platform) | [`backend/app/adk/medical_triage.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/adk/medical_triage.py) | **100% Pass** (`test_medical_triage_high_urgency_cardiac_emergency`, etc.) |
| **A2A Interoperability** | Google Agent2Agent (A2A) Protocol v1.0 | [`backend/app/a2a/bus.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/a2a/bus.py) | **100% Pass** (`test_a2a_multi_agent_consensus`, ADK $\leftrightarrow$ CrewAI) |

---

## 2. Structure 1: CrewAI Framework & Stateful Flows

### A. Architectural Concept
CrewAI orchestrates autonomous agents that assume specific roles, collaborate in structured teams (*Crews*), and execute state-driven business processes (*Flows*).

### B. Core Classes & Structure in KAVACH
Located in [`backend/app/crew/`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/crew/):

1. **`CrewAgent` ([`agents.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/crew/agents.py)):**
   - Each agent defines `role`, `goal`, `backstory`, `tools`, and `memory` (`memory_buffer`).
   - 5 specialized personas implemented:
     - **Sentinel Agent (`create_sentinel_agent`):** Audits prompts for PII, API tokens, and prompt injections.
     - **Retriever Agent (`create_retriever_agent`):** Searches Qdrant vector database for relevant code chunks.
     - **Blast Radius Analyst (`create_blast_radius_agent`):** Performs AST dependency and impact analysis.
     - **Coder Agent (`create_coder_agent`):** Synthesizes patches adhering to security policy.
     - **Supervisor Agent (`create_supervisor_agent`):** Oversees hierarchical crew execution.

2. **`CrewTask` and `Crew` ([`tasks.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/crew/tasks.py), [`crew_runner.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/crew/crew_runner.py)):**
   - Defines sequential or hierarchical execution chains with context propagation between tasks.

3. **`CrewAI Stateful Flows` ([`flows.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/crew/flows.py)):**
   - Uses method decorators to construct event-driven directed acyclic graphs (DAGs):
     - `@start`: Declares the entrypoint step of the flow.
     - `@listen("<step_name>")`: Triggers automatically when `<step_name>` finishes.
     - `@router("<step_name>")`: Conditionally branches state based on dynamic criteria.

### C. Concrete Flow Implementation: `KavachDevOpsFlow`
```python
class KavachDevOpsFlow(BaseFlow):
    @start
    def audit_incoming_request(self):
        """Step 1: Scans developer prompt for PII, credentials, or injections."""
        findings = detect_pii(prompt) + detect_secrets(prompt)
        self.state["security_findings"] = findings
        self.state["is_safe"] = len(findings) == 0
        return {"findings_count": len(findings), "is_safe": self.state["is_safe"]}

    @listen("audit_incoming_request")
    def synthesize_and_validate_patch(self):
        """Step 2: Synthesizes patch & verifies dependencies via PyPI firewall."""
        pkg_result = verify_code_dependencies(code_snippet)
        self.state["package_verification"] = pkg_result
        return pkg_result

    @listen("synthesize_and_validate_patch")
    def generate_attestation_and_sbom(self):
        """Step 3: Emits Cryptographic CycloneDX SBOM and provenance attestation."""
        sbom = generate_cryptographic_sbom(repo_name=repo_name, version="2.4.0")
        self.state["cyclonedx_sbom"] = sbom
        return {"sbom_serial": sbom.get("serialNumber"), "status": "COMPLETED"}
```

---

## 3. Structure 2: Google ADK (Agent Development Kit) & Callbacks

### A. Architectural Concept
Google ADK (`adk.dev`) standardizes agent lifecycle states, tool registration, session state management, and an **8-hook callback architecture** across 3 distinct phases.

### B. Core Classes & Structure in KAVACH
Located in [`backend/app/adk/`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/adk/):

1. **`LlmAgent` & Lifecycle States ([`agent.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/adk/agent.py)):**
   - States: `INITIALIZED` $\rightarrow$ `PLANNING` $\rightarrow$ `EXECUTING_TOOL` $\rightarrow$ `REFLECTING` $\rightarrow$ `COMPLETED` / `FAILED`.

2. **3 Phases & 8 Hook Points ([`callbacks.py`](file:///c:/Users/jaind/Desktop/universty_work/PRJ-IV%20Work%20&%20Agentic%20AI/AgenticAi_MidSem/backend/app/adk/callbacks.py)):**
   - **Phase 1: Agent Lifecycle**
     1. `before_agent_callback`: Intercepts and transforms initial user query or enforces entry guardrails.
     2. `after_agent_callback`: Validates final output, produces audit trails, and seals response.
   - **Phase 2: LLM Interaction**
     3. `before_model_callback`: Enforces DPDP Act tokenization, cost limits, and prompt sanitization.
     4. `after_model_callback`: Performs output schema validation and hallucinations inspection.
     5. `on_model_error_callback`: Intercepts rate limits (HTTP 429) and initiates graceful fallbacks.
   - **Phase 3: Tool Execution**
     6. `before_tool_callback`: Evaluates RBAC permissions and dynamic credentials before calling external tools.
     7. `after_tool_callback`: Sanitizes tool return payloads and updates `context.state_delta`.
     8. `on_tool_error_callback`: Captures external tool exceptions without crashing agent thread.

3. **8 Canonical Design Patterns (`adk.dev/callbacks`):**
   - Pattern 01: Guardrails & Policy Enforcement
   - Pattern 02: Dynamic State Management (`StateProxy` $\rightarrow$ `state_delta`)
   - Pattern 03: Structured Logging & Observability
   - Pattern 04: Semantic Response Caching
   - Pattern 05: Request & Response Modification
   - Pattern 06: Conditional Step Skipping
   - Pattern 07: Tool-Specific Actions (`request_credential`, `skip_summarization`)
   - Pattern 08: Artifact Handling (`save_artifact`, `load_artifact`)

---

## 4. Structure 3: The Medical Triage Multi-Agent Pipeline (Google ADK — CSE3101 course exercise (not part of the banking platform))

Direct implementation of the Professor's Reference Architecture for CSE3101 (isolated course exercise, not part of the banking platform):

```
[ User Query / Symptoms ]
           │
           ▼
[ Root Guardrail: block_sensitive ] ──(Triggered)──► Return: "Request blocked by safety policy"
           │ (Clean)
           ▼
[ triage_agent ] ──► Extracts symptoms & assigns baseline score
           │
           ▼
[ triage_after callback ] ──► Evaluates urgency into state["urgency"] ("HIGH" vs "NORMAL")
           │
     ┌─────┴────────────────────────────────────────────────────────┐
     │                                                              │
     ▼ (Urgency == HIGH)                                            ▼ (Urgency == NORMAL)
[ emergency_agent ] (Gate: only_if_urgent)          [ persona_agent ] (Gate: only_if_normal)
 • Immediately calls 112 / 108                       • Collects patient age, allergies, vitals
 • Safe first-aid steps while waiting                               │
 • Strictly NO medicine dispensed                                   ▼
                                                    [ medicine_agent ]
                                                     • Tavily Web Search for approved OTC remedies
                                                     • Recommends symptomatic care (e.g., Paracetamol)
```

### Shared Session State Keys
- `state["triage"]`: Structured symptom summary and triage score.
- `state["urgency"]`: Routing decision (`HIGH` vs `NORMAL`).
- `state["persona"]`: Patient age, chronic conditions, and allergy flags.
- `state["medicine_options"]`: Approved OTC options with safety warnings.

---

## 5. Structure 4: Cross-Framework Collaboration (ADK $\leftrightarrow$ CrewAI Bridge)

Google ADK and CrewAI operate collaboratively through the **Google Agent2Agent (A2A) Protocol v1.0**:
1. **Google ADK (`adk.coordinator.py`):** Acts as the high-level Planner / Coordinator holding user session context and orchestrating lifecycle hooks.
2. **CrewAI (`crew.agents.py`):** Acts as the specialized Execution Squad running deep audits and code validation.
3. **A2A Bus (`a2a.bus.py`):** Dispatches JSON-RPC 2.0 messages encapsulated with SHA-256 cryptographic signatures.
4. **Pydantic Serialization:** Final deliverables are structured via Pydantic models and emitted into Markdown, Table, or JSON format.

---

## 6. How to Demonstrate in UI & CLI

### A. In Browser UI (`http://127.0.0.1:8000`)
1. **Google ADK Medical Triage Modal:**
   - Click **`Medical Triage`** in the top navbar.
   - Choose between **"Chest Pain & Cardiac Emergency"** (routes to 112/108 via `emergency_agent`) or **"Mild Headache & Fever"** (routes to OTC Paracetamol via `persona_agent` + `medicine_agent`).
2. **Professor Review Standardization (11/11):**
   - Click **`Professor Review (11/11)`** in the top navbar.
   - Select Tab **`3, 6, 7. A2A ADK <-> CrewAI`** to run cross-framework task delegation.
   - Select Tab **`4, 5. Patterns & Callbacks`** to view all 8 ADK Callback Hook Points.
3. **Comic Cloud Explainers (ELI5):**
   - Click **`Comic Explainers (ELI5)`** in the top navbar to see animated visual cards for Topics 3, 4, 5, and 6.

### B. In Terminal / CLI
```powershell
# 1. Run Complete Mid-Sem Evaluation (12/12 checkpoints)
python verify_midsem.py --fast

# 2. Run Google ADK & CrewAI Dedicated Test Suite (50/50 tests passing)
python -m pytest tests/test_adk_callbacks_and_triage.py tests/test_syllabus_advanced_modules.py -v
```

---

## 7. Viva / Examiner Q&A Cheat Sheet

**Q1: Did you use CrewAI in your project?**  
*Answer:*  
"Yes. We implemented the CrewAI framework in `backend/app/crew/`. We defined 5 specialized `CrewAgent` personas with explicit goals, backstories, tools, and memory buffers. Furthermore, we implemented **CrewAI Stateful Flows** using `@start`, `@listen`, and `@router` in `flows.py` (`KavachDevOpsFlow`) to automate pre-audit, dependency verification, and SLSA Level-3 CycloneDX SBOM generation."

**Q2: Did you use Google ADK in your project?**  
*Answer:*  
"Yes. In `backend/app/adk/`, we implemented Google Agent Development Kit core specifications including the `LlmAgent` lifecycle state machine (`INITIALIZED` through `COMPLETED`). Crucially, we implemented the **8-Hook Callback architecture** across 3 phases (Agent, Model, Tool) and demonstrated all 8 canonical ADK design patterns from `adk.dev/callbacks`."

**Q3: What is the structure of your Google ADK Medical Triage Pipeline?**  
*Answer:*  
"The pipeline in `backend/app/adk/medical_triage.py` starts with a root guardrail (`block_sensitive`). User queries proceed to the `TriageAgent` which updates `state['triage']`. The `triage_after` callback determines urgency into `state['urgency']`. If `HIGH`, it gates to the `EmergencyAgent` which calls 112/108 and provides safe waiting instructions while strictly forbidding medication. If `NORMAL`, it gates to `NormalFlow`, running the `PersonaAgent` for patient details followed by `MedicineAgent` for Tavily OTC search."

**Q4: How do Google ADK and CrewAI interact?**  
*Answer:*  
"We bridged them using the **Google Agent2Agent (A2A) Protocol v1.0** (`backend/app/a2a/`). Google ADK serves as the macro-coordinator and session holder, delegating specialized audit subtasks to a CrewAI crew via SHA-256 signed message packets, returning Pydantic-validated governance reports."
