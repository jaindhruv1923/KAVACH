# KAVACH Capstone Cloud Deployment Guide
### Multi-Service Agentic AI Architecture (Ports 8000, 8050, 8090)
**Complies with Point 11 of Professor Pranshu Tiwari's Project Review Requirements**

---

## 1. Architectural Topology Overview

The KAVACH platform is containerized as a decoupled, multi-service zero-trust microservice mesh:

```mermaid
graph TD
    Client[Browser / Evaluator Cockpit] --> Ingress[Reverse Proxy / Cloud Ingress]
    
    subgraph Multi-Service Cloud Mesh
        Ingress -->|Port 8000| S1[KAVACH DevSecOps & Governance Platform]
        Ingress -->|Port 8050| S2[Bharat Core Banking Highway]
        Ingress -->|Port 8090| S3[Unified Operations & Results Cockpit]
        
        S1 <-->|Agent-to-Agent A2A Protocol| S2
        S1 -->|Telemetry Stream & Merkle Leaf| S3
        S2 -->|ACID Audit Records| S3
        
        S1 -.->|MCP Tools: Web, DB, AST, Calc| MCP[Model Context Protocol Engine]
    end
```

| Service | Port | Description | Health Check Probe |
| :--- | :--- | :--- | :--- |
| **`kavach-platform`** | `8000` | Zero-Trust AI DevOps, Google ADK & CrewAI Orchestration, MCP Server | `GET http://localhost:8000/health` |
| **`bharat-core-banking`** | `8050` | Bharat Core Banking Highway, ACID SAGA rollback, RBI HITL escrow | `GET http://localhost:8050/api/bank/accounts` |
| **`results-cockpit`** | `8090` | Unified Telemetry, NIST SHA3-512 DPDP Merkle Ledger, Live Stream | `GET http://localhost:8090/api/results/summary` |

---

## 2. Docker Compose Deployment (Local & Cloud VM)

The root repository contains a production-ready [`docker-compose.yml`](../docker-compose.yml).

### Step 1: Build & Launch Multi-Service Mesh
```bash
# Build images and start all 3 services in detached mode
docker compose up -d --build
```

### Step 2: Verify Service Status & Health Probes
```bash
docker compose ps
```
*Expected Output:*
```text
NAME                     STATUS              PORTS
bharat-banking-highway   Up (healthy)        0.0.0.0:8050->8050/tcp
kavach-platform-engine   Up (healthy)        0.0.0.0:8000->8000/tcp
kavach-results-hub       Up (healthy)        0.0.0.0:8090->8090/tcp
```

### Step 3: Inspect Logs
```bash
# Stream aggregated logs across all three services
docker compose logs -f
```

---

## 3. Render.com Deployment (1-Click Web Services)

Render supports multi-service deployments via `render.yaml`.

### `render.yaml` Configuration
```yaml
services:
  # 1. KAVACH Platform Engine
  - type: web
    name: kavach-platform
    env: python
    region: singapore
    plan: free
    buildCommand: pip install -r 01_KAVACH_Platform/backend/requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT --app-dir 01_KAVACH_Platform/backend
    envVars:
      - key: PYTHONUNBUFFERED
        value: 1
      - key: KAVACH_OFFLINE
        value: 1

  # 2. Bharat Core Banking Highway
  - type: web
    name: bharat-banking
    env: python
    region: singapore
    plan: free
    buildCommand: pip install -r 02_Banking_and_Results_Dashboard/implementation_banks/requirements.txt
    startCommand: python -m uvicorn implementation_banks.server:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHONUNBUFFERED
        value: 1
      - key: PYTHONPATH
        value: 02_Banking_and_Results_Dashboard

  # 3. Unified Results Cockpit
  - type: web
    name: results-cockpit
    env: python
    region: singapore
    plan: free
    buildCommand: pip install -r 02_Banking_and_Results_Dashboard/results_dashboard/requirements.txt
    startCommand: python -m uvicorn results_hub:app --app-dir 02_Banking_and_Results_Dashboard/results_dashboard --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHONUNBUFFERED
        value: 1
```

---

## 4. Railway.app Deployment

1. Fork or push repository to GitHub.
2. In Railway Dashboard, click **New Project** &rarr; **Deploy from GitHub repo**.
3. Create 3 services inside the same project canvas:
   - **Service 1 (KAVACH)**: Root directory: `/`, Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT --app-dir 01_KAVACH_Platform/backend`
   - **Service 2 (Banking)**: Root directory: `/`, Start Command: `python -m uvicorn implementation_banks.server:app --host 0.0.0.0 --port $PORT`
   - **Service 3 (Cockpit)**: Root directory: `/`, Start Command: `python -m uvicorn results_hub:app --app-dir 02_Banking_and_Results_Dashboard/results_dashboard --host 0.0.0.0 --port $PORT`
4. Set Environment Variable `PORT` on each service (automatically mapped by Railway).

---

## 5. AWS ECS / Fargate Deployment

### Architecture on AWS
- **VPC & Subnets**: Public subnets with Application Load Balancer (ALB).
- **ALB Path-Based Routing**:
  - `/*` &rarr; KAVACH Platform Target Group (`kavach-platform:8000`)
  - `/api/bank/*` &rarr; Bharat Bank Target Group (`bharat-core-banking:8050`)
  - `/results/*` &rarr; Results Cockpit Target Group (`results-cockpit:8090`)
- **Task Definition**: Multi-container ECS Task using `docker-compose.yml` or AWS CloudFormation.

---

## 6. Verification & Automated Test Run

Once deployed, verify that all 11 standardization requirements pass on the live cloud host:

```bash
# Execute Live End-to-End Integration Verification Suite
python verification/live_e2e_integration_test.py

# Execute Focused Security & Containment Checks
python verification/focused_check.py

# Execute 32 Dedicated Agentic ReAct & Tool Verification Tests
pytest 01_KAVACH_Platform/tests/test_agent_tools.py 01_KAVACH_Platform/tests/test_react_engine.py 01_KAVACH_Platform/tests/test_agentic_api.py 01_KAVACH_Platform/tests/test_multimodal_vision.py 01_KAVACH_Platform/tests/test_mcp_protocol.py -v

# Execute Full Test Suite (494 tests)
pytest 01_KAVACH_Platform/tests/ -q
```

All suites pass deterministically with **100% success rate**.
