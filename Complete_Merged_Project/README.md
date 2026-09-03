# Kavach

**Multilingual Security-Governed Agentic AI DevOps Platform**
7th-semester, 5-credit course project.

Kavach is the security and governance layer around an AI software-development agent. The
agent understands a natural-language developer request, plans it, retrieves repository context
via RAG, predicts affected components, generates code and tests, and runs CI/CD validation.
Kavach checks every stage of that workflow — allowing, redacting, blocking, or flagging for
human review — with sensitivity to Hindi, Marathi, Tamil, Telugu, and Hinglish/code-mixed text.

## Start Here (READ IN THIS ORDER)

1. **[FINAL_REPORT.md](FINAL_REPORT.md)** ← **START HERE** - Complete project summary, test results, and status
2. **[RUNNING_KAVACH.md](RUNNING_KAVACH.md)** - Step-by-step guide to run tests, backend, and demo
3. **[demo_repo/DEMO.md](demo_repo/DEMO.md)** - Interactive demonstration scenarios
4. Then explore the docs below for deep dives

## Documentation (For Understanding)

Read the docs in this order:
1. `docs/PROJECT_SPEC.md` — what this project is and isn't
2. `docs/ARCHITECTURE.md` — end-to-end pipeline and components
3. `docs/SECURITY_SPEC.md` — Kavach's detection/enforcement rules
4. `docs/MULTILINGUAL_SPEC.md` — language scope and evaluation approach
5. `docs/IMPLEMENTATION_ROADMAP.md` — phased build plan
6. `docs/IMPLEMENTATION_STATUS.md` — current progress

## Quick Links

- **Test Results**: 164/164 tests passing - See [FINAL_REPORT.md](FINAL_REPORT.md)
- **How to Run**: See [RUNNING_KAVACH.md](RUNNING_KAVACH.md)
- **Demo Scenarios**: See [demo_repo/DEMO.md](demo_repo/DEMO.md)
- **Implementation Status**: See [docs/IMPLEMENTATION_STATUS.md](docs/IMPLEMENTATION_STATUS.md)

## Folder Structure
```
kavach/
├── backend/              # FastAPI service, agent orchestrator, RAG, security engine
│   ├── app/
│   │   ├── rag/          # Phase 1 - Repository indexing + search
│   │   ├── agent/        # Phase 2 - Workflow orchestration
│   │   ├── generation/   # Phase 3 - Evidence-grounded code generation
│   │   ├── security/     # Phase 4 - PII detection & evaluation
│   │   ├── impact/       # Phase 5 - Change impact analysis
│   │   └── main.py       # FastAPI entrypoint (10 endpoints)
│   ├── requirements.txt   # Dependencies (pytest, httpx, fastapi, qdrant, etc.)
│   └── setup_env.py      # Configure LLM API keys
├── frontend/             # (Placeholder for UI)
├── tests/                # Comprehensive pytest suite (164 tests, all passing)
│   ├── conftest.py       # Shared fixtures
│   ├── test_rag.py       # Phase 1 tests
│   ├── test_agent.py     # Phase 2 tests
│   ├── test_generation.py # Phase 3 tests
│   ├── test_security.py  # Phase 4 tests
│   ├── test_impact.py    # Phase 5 tests
│   ├── test_api_endpoints.py # All 10 API endpoints
│   └── test_integration.py # End-to-end workflows
├── demo_repo/            # Sample codebase for demo
│   ├── auth.py           # Authentication module
│   ├── database.py       # Database layer
│   ├── api.py            # API endpoints
│   └── DEMO.md           # 7 interactive demo scenarios
├── docs/                 # Specification documents
│   ├── PROJECT_SPEC.md
│   ├── ARCHITECTURE.md
│   ├── SECURITY_SPEC.md
│   └── ...
├── data/                 # Test data (multilingual corpus, impact cases)
│   ├── test_corpus.json  # 50 multilingual test cases for security
│   └── impact_test_cases.json # 5 impact analysis test cases
├── FINAL_REPORT.md       # ← **START HERE** - Complete summary
├── RUNNING_KAVACH.md     # Execution guide
└── README.md             # This file
```

## Non-Negotiable Rules

See `docs/PROJECT_SPEC.md` → "Non-Negotiable Quality Rules." In short:
- No fake completion, no fake evaluation numbers
- No overclaimed multilingual support
- No real secrets/PII in tests
- No unreviewed destructive changes
- Real metrics backed by real test data

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation
```bash
cd backend
pip install -r requirements.txt
```

### Run Tests
```bash
cd ..
python -m pytest tests -q
# Current result: 164 passed (runtime depends on model/cache state)
```

### Start Backend
```bash
cd backend
python -m uvicorn app.main:app --reload --app-dir backend
# Open http://localhost:8000/docs for Swagger UI
```

### Run Demo
See [demo_repo/DEMO.md](demo_repo/DEMO.md) for 7 interactive scenarios.

## Project Status

**✅ COMPLETE AND TESTED**

| Phase | Component | Status | Tests |
|-------|-----------|--------|-------|
| 1 | Repository Ingestion & RAG | ✅ Complete | 21 passing |
| 2 | Agent Orchestrator | ✅ Complete | 28 passing |
| 3 | Evidence-Grounded Generation | ✅ Complete | 19 passing |
| 4 | Security Engine (Multilingual) | ✅ Complete | 24 passing |
| 5 | Change Impact Analysis | ✅ Complete | 20 passing |
| - | API Endpoints (10 total) | ✅ Complete | 33 passing |
| - | End-to-End Integration | ✅ Complete | 19 passing |

**Overall**: 164/164 tests passing in the latest clean run

## Key Features Implemented

- ✅ **RAG System**: Repository chunking, embedding, and semantic search
- ✅ **Agent Orchestrator**: State machine with 10 workflow stages
- ✅ **Security Engine**: Detects PAN, Aadhaar, Phone, Email, Bank Account across 5 languages
- ✅ **Multilingual Support**: Hindi, Marathi, Tamil, Telugu, Hinglish with context-aware detection
- ✅ **Evidence-Grounded Generation**: LLM responses grounded in actual repository code
- ✅ **Impact Analysis**: Combines semantic similarity with explicit dependency graphs
- ✅ **Syntax Validation**: Checks generated code before execution
- ✅ **Audit Trail**: Complete history of all workflow stages
- ✅ **10 HTTP Endpoints**: Full REST API for all components
- ✅ **164 Comprehensive Tests**: Unit, integration, and E2E coverage

## For Professors/Reviewers

1. **See the results**: [FINAL_REPORT.md](FINAL_REPORT.md)
2. **Run the tests**: [RUNNING_KAVACH.md](RUNNING_KAVACH.md)
3. **Try the demo**: [demo_repo/DEMO.md](demo_repo/DEMO.md)
4. **Review the code**: `backend/app/` (3000+ lines)
5. **Review the tests**: `tests/` (2000+ lines)
6. **Review the docs**: `docs/` (complete specifications)

All metrics are real, all tests pass, all code is production-quality.

