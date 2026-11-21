# KAVACH Project Structure

One website, many dashboards. The main platform server (port 8001) serves the
main website and mounts every dashboard under its own path, so a single command
starts the whole project and every button works from one address.

## Start it

```
run_all_services.bat                 (Windows, recommended)
.\run_all_services.ps1               (PowerShell)
docker compose up --build            (Docker)
```

Then open http://localhost:8001/

## Where each dashboard lives

| Dashboard            | Address on the platform | Source folder                                                   |
| -------------------- | ----------------------- | --------------------------------------------------------------- |
| Main platform        | `/`                     | `kavach_platform/01_KAVACH_Platform/frontend/index.html`        |
| Live Console         | `/console`              | `kavach_platform/01_KAVACH_Platform/frontend/console.html`      |
| Mid-Sem Foundation   | `/midsem`               | `kavach_platform/01_KAVACH_Platform/frontend/midsem.html`       |
| Post-Mid-Sem Evolution | `/evolution`          | `kavach_platform/01_KAVACH_Platform/frontend/evolution.html`    |
| Real AI Agents       | `/cockpit/`             | `kavach_agent_core/cockpit.html` + `kavach_agent_core/server.py` |
| Live Agent Swarm     | `/swarm/`               | `live_agent_swarm/`                                             |
| Bharat Core Bank     | `/bharat/`              | `bharat_core_banking/`                                          |
| Banking Highway      | `/bank/`                | `kavach_platform/02_Banking_and_Results_Dashboard/implementation_banks/` |
| Motion Graphics      | `/motion/`              | `kavach_platform/motion_graphics/`                              |
| Stakeholder Guide    | `/guide`                | `kavach_platform/02_Banking_and_Results_Dashboard/animated_guide.html` |
| Mid-Sem Reports      | `/reports/`             | `kavach_platform/agentic_ai_midsem/`                            |

Inside the main website, the header tabs **Real AI Agents**, **Agent Swarm**,
**Banking Apps** and **All Dashboards** open these dashboards embedded in the
page; every dashboard also has the shared top bar to jump between them.

## Folder map

```
PRJ-IV &AgenticAi Final Work/
├── shared_ui/                     Shared top bar + design tokens used by every dashboard
│   ├── kavach-suite.css             colours (navy / blue / green / white), fonts, top bar, menu
│   └── kavach-suite.js              dashboard registry, links, top-right tools
├── kavach_platform/
│   ├── 01_KAVACH_Platform/
│   │   ├── backend/app/main.py      Unified server: main website + mounts every dashboard
│   │   ├── frontend/                Main website (index, console, midsem, evolution)
│   │   │   └── platform_theme.css     Final design layer for the main website
│   │   ├── tests/                   Platform test suite (pytest)
│   │   └── docs/                    Metrics, architecture and screenshots
│   ├── 02_Banking_and_Results_Dashboard/
│   │   ├── implementation_banks/    Banking Highway dashboard + API
│   │   ├── tests_unified/           Banking test suite
│   │   └── animated_guide.html      Stakeholder guide
│   ├── motion_graphics/             Motion graphics studio
│   ├── agentic_ai_midsem/           Mid-semester submission reports
│   └── scripts/                     Metrics + documentation generators
├── kavach_agent_core/               Real AI Agents (autonomous multi-agent cockpit)
├── live_agent_swarm/                Six-sentinel agent swarm
├── bharat_core_banking/             Bharat Core Bank A/B comparison portal
├── adapters/                        Model adapters (cloud, edge, offline)
├── documentation_and_reports/       Presentations, reports, handouts, viva material
├── scripts/                         Repository validators
├── run_all_services.bat / .ps1      One-click launchers
├── docker-compose.yml, Dockerfile   Container setup (single service on 8001)
└── README.md                        Full technical documentation
```

## Design system

All dashboards share one palette defined in `shared_ui/kavach-suite.css`:
navy `#0B1F3A` for structure, blue `#1D4ED8` for actions and links, green
`#0F7B5F` for success and live status, red only for real threats, on white and
light-grey surfaces. Text uses IBM Plex Sans, code and figures IBM Plex Mono.

## Tests

```
cd kavach_platform/01_KAVACH_Platform && python -m pytest -q tests
python -m pytest -q kavach_platform/02_Banking_and_Results_Dashboard
```
