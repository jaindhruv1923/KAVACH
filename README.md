# CSE3101: Agentic AI & PRJ-IV Dual Capstone Repository
**BML Munjal University — School of Engineering & Technology**  
**Student:** Dhruv Jain  
**Instructors:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  

---

## Workspace Layout & Repository Organization

This repository is strictly partitioned into two independent, production-grade workspaces with zero clutter:

```
Ageentic&PRJ-IV/
│
├── 📂 "agentic ai mid sem"/                      <-- CSE3101 Agentic AI Mid-Semester Submission
│   ├── 📂 kavach_platform/                        <-- Unified KAVACH MidSem Platform (Port 8000)
│   ├── 📂 imp_files/                              <-- 7 Curated Syllabus Code Modules (ADK, CrewAI, Guardrails, Patterns, MCP)
│   ├── 📂 documentation_and_reports/              <-- Consolidated MidSem Documentation, Flowcharts & Research
│   │   ├── 📂 01_Submission_Documents_And_Reports/
│   │   ├── 📂 02_Presentations_And_Viva_Defense/
│   │   ├── 📂 03_Architecture_And_Flowcharts/
│   │   ├── 📂 04_Evaluation_And_Research_Papers/
│   │   └── 📦 Archived_Legacy_Materials.zip
│   ├── 📜 run_midsem.bat                          <-- 1-Click Platform Launcher (Port 8000)
│   ├── 📜 run_live_cloud_tunnel.bat               <-- 1-Click Public Cloud Tunnel
│   └── 📜 README.md                               <-- MidSem Technical & Architecture Overview
│
└── 📂 "PRJ-IV &AgenticAi Final Work"/             <-- PRJ-IV & Agentic AI Final Capstone Project
    ├── 📂 kavach_platform/                        <-- Production KAVACH Agentic Defense Platform (Port 8001)
    ├── 📂 bharat_core_banking/                    <-- Bharat Core Bank Web Portal (Port 8002)
    ├── 📂 live_agent_swarm/                       <-- Real-Time Multi-Agent Swarm Simulation Engine (Port 8003)
    ├── 📂 documentation_and_reports/              <-- Consolidated Final Documentation, Presentations & Rubrics
    │   ├── 📂 01_Presentations_And_Reports/       <-- Master PPTX (16 Slides), Defense Outline & Video Scripts
    │   └── 📂 02_Course_Handouts_And_Rubrics/     <-- Handout Mappings, Rubric Alignments & Viva Questions
    ├── 📂 adapters/                               <-- Framework and Model Protocol Adapters
    ├── 📂 scripts/                                <-- Automated Validation & Verification Suites
    ├── 📜 run_all_services.bat                    <-- 1-Click Launch All 3 Services (8001, 8002, 8003)
    ├── 📜 run_live_cloud_tunnel.bat               <-- 1-Click Public Live Cloud Tunnel
    └── 📜 README.md                               <-- PRJ-IV Architecture & Mathematical Specification
```

---

## Service & Port Allocation Matrix

| Service / Component | Workspace Directory | Port | Key Capabilities |
| :--- | :--- | :--- | :--- |
| **MidSem KAVACH Platform** | `agentic ai mid sem/kavach_platform` | **8000** | Interactive Console, Inbuilt IDE, Academic Flowcharts, DPDP Token Vault |
| **Final KAVACH Platform** | `PRJ-IV &AgenticAi Final Work/kavach_platform` | **8001** | Production Unified Security Gateway, FastMCP & A2A, Inbuilt IDE |
| **Bharat Core Bank Portal** | `PRJ-IV &AgenticAi Final Work/bharat_core_banking` | **8002** | Real-time Banking Transactions, Statement Verification, SAGA Rollback |
| **Live Agent Swarm Engine** | `PRJ-IV &AgenticAi Final Work/live_agent_swarm` | **8003** | 6-Agent Swarm Simulation, Sentinel Gate, Entropy Analyzer, GoT Reasoner |

---

## Quick Launch Instructions

### 1. Launch Mid-Semester Work
Double click `run_midsem.bat` inside `agentic ai mid sem/` or run:
```powershell
cd "agentic ai mid sem"
.\run_midsem.bat
```
Visit: **`http://localhost:8000/`**

### 2. Launch Final Project Work (All 3 Services)
Double click `run_all_services.bat` inside `PRJ-IV &AgenticAi Final Work/` or run:
```powershell
cd "PRJ-IV &AgenticAi Final Work"
.\run_all_services.bat
```
- Master Security Platform: **`http://localhost:8001/`**
- Bharat Core Bank Portal: **`http://localhost:8002/`**
- Live Multi-Agent Swarm Engine: **`http://localhost:8003/`**

---

## Inbuilt IDE & Academic Explainer

Both platforms include an embedded **`</> Inbuilt IDE`** button located right above the floating action buttons:
- Full hierarchical code explorer matching course modules
- One-click navigation and code highlighting (e.g., CrewAI, ADK Callbacks, Verhoeff D5, Self-Healer)
- Live Architecture Flowchart tab with pipeline diagrams, execution stages, approach justifications, and viva defense answers.
