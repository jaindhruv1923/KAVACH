# 🛡️ KAVACH Live Agentic AI Command Center & Execution Orchestrator
### *Autonomous Multi-Agent Safety Swarm & Real-Time Reasoning Cockpit*
**Course / Evaluation**: CSE3101 Agentic AI (BML Munjal University)  
**Evaluators**: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  
**Project Workspace**: `c:\Users\jaind\OneDrive\Desktop\project_work\live_agent_dashboard\`

---

## 🌟 Executive Overview
The **KAVACH Live Agentic AI Command Center** provides a dedicated, real-time visual orchestration dashboard where examiners, professors, and security engineers can observe **6 specialized autonomous AI agents** actively analyzing, sanitizing, reasoning, and verifying real-world inputs, banking transactions, code blocks, and adversarial attacks step-by-step.

---

## 🧬 Architecture: 6 Autonomous Specialized Agents

```
                        [ User / Banking Input Payload ]
                                       │
                                       ▼
             ┌──────────────────────────────────────────────────┐
             │ Agent 1: Sentinel Intent Gate                    │
             │ (OWASP LLM01 Prompt Injection & Delimiter Guard) │
             └─────────────────────────┬────────────────────────┘
                                       │
                                       ▼
             ┌──────────────────────────────────────────────────┐
             │ Agent 2: AST Blast-Radius & Code Sanitizer       │
             │ (Python ast.parse() · CWE-502 · CWE-78 Subprocess│
             └─────────────────────────┬────────────────────────┘
                                       │
                                       ▼
             ┌──────────────────────────────────────────────────┐
             │ Agent 3: DPDP 2023 PII Vault Anonymizer          │
             │ (Aadhaar UID · PAN · Phone Salted Tokenization)  │
             └─────────────────────────┬────────────────────────┘
                                       │
                                       ▼
             ┌──────────────────────────────────────────────────┐
             │ Agent 4: Graph-of-Thoughts (GoT) Reasoner        │
             │ (Kahn's Topological DAG Acyclicity · CoT Chains) │
             └─────────────────────────┬────────────────────────┘
                                       │
                                       ▼
             ┌──────────────────────────────────────────────────┐
             │ Agent 5: Differential Privacy Laplace Engine     │
             │ (Strict (ε, δ)-DP Bounds · Calibrated Perturb)   │
             └─────────────────────────┬────────────────────────┘
                                       │
                                       ▼
             ┌──────────────────────────────────────────────────┐
             │ Agent 6: Post-Quantum & SAGA Distributed Ledger  │
             │ (NIST FIPS 204 ML-DSA-65 · SLSA Level 3 JSON)    │
             └─────────────────────────┬────────────────────────┘
                                       │
                                       ▼
                [ Certified Sanitized Output & Audit Receipt ]
```

---

## 🚀 How to Launch the Dashboard

### Option A: 1-Click Launch (Zero Configuration)
Simply open `index.html` in your browser (or right-click `index.html` -> **"Open with Live Server"** in VS Code / Antigravity IDE).
- **Dual-Engine Architecture**: The dashboard features an autonomous client-side engine that replicates the full multi-agent pipeline offline. It requires **zero setup** or running servers.

### Option B: With Real Python FastAPI Engine
To run with the real Python backend AST parser and REST API:
1. Open a terminal in `live_agent_dashboard/`:
   ```bash
   cd live_agent_dashboard
   python agent_engine.py
   ```
2. The FastAPI backend starts at `http://127.0.0.1:8000`.
3. Open `index.html` in your browser. The dashboard automatically detects and links to the live Python backend via `/api/orchestrate`.

---

## 🎯 5 One-Click Presets for Faculty Demonstration

| Preset | Scenario Description | Expected Agentic Behavior |
|--------|----------------------|---------------------------|
| **1. Valid Wire Transfer (₹25L)** | Legitimate RTGS transfer with Aadhaar (`3849-2918-4729`) and PAN (`ABCDE1234F`). | Passes Agent 1 & 2. Agent 3 detects PII and tokenizes it to `[VAULT:AADHAAR_XXXX]`. Agent 4 verifies GoT acyclicity. Agent 5 calibrates $\epsilon$-DP noise. Agent 6 signs with ML-DSA-65. **Verdict: SANITIZED_AND_ALLOWED**. |
| **2. Jailbreak & Prompt Injection** | Adversarial override (`SYSTEM OVERRIDE: Ignore all previous instructions...`). | **Intercepted at Agent 1 (Sentinel Gate)**. Flags OWASP LLM01 direct prompt injection with 98% confidence. Quarantines prompt immediately. **Verdict: BLOCKED_AND_QUARANTINED**. |
| **3. Python AST RCE Exploit** | Code injection attempt with `yaml.unsafe_load()` and `subprocess.Popen(["cat", "/etc/passwd"])`. | **Intercepted at Agent 2 (AST Guard)**. Real AST traversal flags CWE-502 (Insecure Deserialization / CVE-2020-14343) and CWE-78. Code execution halted. **Verdict: BLOCKED_AND_QUARANTINED**. |
| **4. Denial-of-Wallet Loop** | Algorithmic complexity inflation with recursive loop instruction (`repeat infinitely...`). | **Intercepted at Agent 4 (GoT Reasoner)**. Kahn's topological sort detects cyclic dependency loop. Token exhaustion prevented. **Verdict: BLOCKED_AND_QUARANTINED**. |
| **5. Differential Privacy Query** | SQL aggregation query on sensitive branch accounts with phone number. | Passes guards, redacts phone number to Vault token, computes Laplace noise perturbation, and verifies $e^\epsilon$ bound. **Verdict: SANITIZED_AND_ALLOWED**. |

---

## 📋 Key Features & Examiner Viva Points

1. **Step-by-Step Interactive Debugger**:
   Clicking **"⏯️ Step-by-Step"** steps through each of the 6 agents individually, allowing evaluators to inspect how the payload is transformed at each stage.
2. **Chain-of-Thought (CoT) Traces**:
   Click the **"Agent CoT"** tab in the right panel to inspect the internal reasoning log of every agent.
3. **Cryptographic SLSA Level 3 Provenance**:
   Click **"SLSA JSON"** or **"📥 Audit JSON"** to view and download a verifiable SLSA Level 3 execution statement compliant with in-toto v1.0.
4. **Live Streaming Terminal**:
   Monospace interactive terminal displays timestamped, color-coded agent logs in real time. Click **"📋 Copy Logs"** to copy the full telemetry trace.
