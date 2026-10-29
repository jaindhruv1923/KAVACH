# PRJ4 — Agentic AI Final Project: KAVACH Ecosystem

**Security-Governed Autonomous Agentic AI DevOps Platform with Zero-Trust Guardrails**  
*Instructors: Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari | CSE3101 Agentic AI | BML Munjal University*  
*Developer: Dhruv Jain*

---

## 1. Directory Structure

This final project repository is organized into three clean operational hubs, course documentation, and unified orchestration launchers:

```text
PRJ4_AG_AI_Final_Project/
├── 01_kavach_platform/             # Master KAVACH Zero-Trust DevSecOps Platform
│   ├── 01_KAVACH_Platform/         # FastAPI Backend, Frontend Dashboard, Security Gates
│   ├── 02_Banking_and_Results_Dashboard/ # Core Banking Engine & Unified Results Hub
│   ├── 03_Documentation/           # Technical Architecture & Evaluation Evidence
│   └── run_kavach.ps1              # Platform-specific launcher
│
├── 02_live_agent_dashboard/        # Autonomous Multi-Agent Safety Swarm Engine (Port 8000)
│   ├── agent_engine.py             # 6-Agent Autonomous Orchestrator (FastAPI Daemon)
│   ├── index.html                  # Swarm Visualizer & Telemetry Cockpit
│   ├── dashboard.css               # Enterprise Clean Light Design System
│   ├── dashboard.js                # Live Stream Logger & Test Matrix Hooks
│   └── test_matrix.py              # 7-Attack Automated Verification Harness
│
├── 03_applications_work/           # Bharat Core Bank A/B Comparative SecOps Portal (Port 8002)
│   ├── server.py                   # A/B Simulation Engine: Without KAVACH vs With KAVACH
│   ├── index.html                  # 3-Phase Progression Narrative UI
│   ├── style.css                   # Enterprise Clean Light Design System
│   └── app.js                      # Dual-State Ledger & Statutory Impact Visualizer
│
├── course_documents/               # Official Course Handout & MidSem Reference Documents
├── run_all_services.bat            # One-click Master Launcher for All 3 Services
├── run_all_services.ps1            # PowerShell Unified Launcher
└── README.md                       # This Guide
```

---

## 2. Port Architecture & Service Endpoints

| Service Name | Port | Endpoint URL | Role in Defense & Evaluation |
| :--- | :---: | :--- | :--- |
| **KAVACH Master Platform** | `8001` | `http://localhost:8001/` | **Master Control Hub**: Operates all 3 pathways (Earlier v1.0, Improvised v3.0, Academic Weapon 10 Frontiers), 30/30 Review Hub, and navigation links. |
| **KAVACH Live Agent Swarm** | `8000` | `http://localhost:8000/` | **Autonomous Swarm Engine**: Executes 6 specialized agents (Sentinel, AST, DPDP Vault, GoT Reasoner, DP Laplace, NIST ML-DSA). |
| **Bharat Core Bank Applications** | `8002` | `http://localhost:8002/` | **Empirical Comparative Lab**: Proves real-world necessity by pitting raw LLMs (*₹50L drained, PII exfiltrated*) against KAVACH (*100% protected*). |
| **Bharat Core Banking Highway** | `8001` | `http://localhost:8001/bank/` | **Integrated Banking Highway**: Internal banking service mounted directly inside the main platform. |

---

## 3. Quick Start

Double-click `run_all_services.bat` or run:
```powershell
.\run_all_services.ps1
```
This automatically boots all three microservices and opens the master browser to `http://localhost:8001/`.
