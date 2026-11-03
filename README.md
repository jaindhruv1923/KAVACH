# CSE3101: Agentic AI & PRJ-IV Dual Capstone Repository
**BML Munjal University — School of Engineering & Technology**  
**Student:** Dhruv Jain  
**Instructors:** Dr. Soharab Hossain Shaikh & Mr. Pranshu Tiwari  

---

## Workspace Layout & Repository Organization

This repository is strictly partitioned into two independent, production-grade workspaces:

```
Ageentic&PRJ-IV/
│
├── 📂 "agentic ai mid sem"/                  <-- CSE3101 Agentic AI Mid-Semester Submission & Codebase
│   ├── 📂 KAVACH-main/                        <-- Unified KAVACH MidSem Platform (Port 8000)
│   ├── 📂 imp_files/                          <-- 7 Curated Syllabus Showcases (ADK, CrewAI, Guardrails, Patterns, MCP)
│   ├── 📂 documentation_and_reports/          <-- Categorized Project Documentation & Academic Artifacts
│   │   ├── 📂 01_MidSem_Submission_Docs/      <-- Synopsis, Project Plan, Progress Report, Coverage Matrix
│   │   ├── 📂 02_Course_Handout_And_Guides/   <-- Problem Statement, Code Demo Guides, Reference Docs
│   │   └── 📂 03_Presentation_And_Viva/       <-- MidSem Presentation Script & Oral Defense Notes
│   ├── 📜 run_midsem.bat                      <-- 1-Click Platform Launcher (Port 8000)
│   ├── 📜 run_live_cloud_tunnel.bat           <-- 1-Click Public Cloud Tunnel
│   └── 📜 README.md                           <-- MidSem Technical & Architecture Overview
│
└── 📂 "PRJ-IV &AgenticAi Final Work"/         <-- PRJ-IV & Agentic AI Final Capstone Project
    ├── 📂 kavach_platform/                    <-- Production KAVACH Agentic Defense Platform (Port 8001)
    ├── 📂 applications_work/                  <-- Bharat Core Bank Web Portal (Port 8002)
    ├── 📂 live_agent_dashboard/               <-- Real-Time Multi-Agent Swarm Simulation Engine (Port 8003)
    ├── 📂 presentation_and_reports/           <-- Master PPTX, Defense Scripts, and Progress Reports
    ├── 📂 adapters/                           <-- Framework and Model Protocol Adapters
    ├── 📂 course_documents/                   <-- Handout Mappings, Viva Rubrics & Questions
    ├── 📂 scripts/                            <-- Automated Validation & Verification Suites
    ├── 📜 run_all_services.bat                <-- 1-Click Launch All 3 Services (8001, 8002, 8003)
    ├── 📜 run_live_cloud_tunnel.bat           <-- 1-Click Public Live Cloud Tunnel
    └── 📜 README.md                           <-- PRJ-IV Final Project Architecture & Mathematical Specification
```

---

## Service & Port Allocation Matrix

| Service / Component | Workspace Directory | Port | Key Capabilities |
| :--- | :--- | :--- | :--- |
| **MidSem KAVACH Platform** | `agentic ai mid sem/KAVACH-main` | **8000** | Interactive Console, Inbuilt IDE, Academic Flowcharts, DPDP Token Vault |
| **Final KAVACH Platform** | `PRJ-IV &AgenticAi Final Work/kavach_platform` | **8001** | Production Unified Security Gateway, FastMCP & A2A, Inbuilt IDE |
| **Bharat Core Bank Portal** | `PRJ-IV &AgenticAi Final Work/applications_work` | **8002** | Real-time Banking Transactions, Statement Verification, SAGA Rollback |
| **Live Agent Swarm Engine** | `PRJ-IV &AgenticAi Final Work/live_agent_dashboard` | **8003** | 6-Agent Swarm Simulation, Sentinel Gate, Entropy Analyzer, GoT Reasoner |

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
- Master Platform: **`http://localhost:8001/`**
- Bharat Core Bank: **`http://localhost:8002/`**
- Live Multi-Agent Swarm: **`http://localhost:8003/`**

---

## Inbuilt IDE & Academic Explainer

Both platforms include an embedded **`</> Inbuilt IDE`** button located right above the floating action buttons:
- Full hierarchical code explorer matching course modules
- One-click navigation and code highlighting (e.g., CrewAI, ADK Callbacks, Verhoeff D5, Self-Healer)
- Live Architecture Flowchart tab with pipeline diagrams, execution stages, approach justifications, and viva defense answers.
