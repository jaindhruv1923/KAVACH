# Kavach

**Multilingual Security-Governed Agentic AI DevOps Platform**
7th-semester, 5-credit course project.

Kavach is the security and governance layer around an AI software-development agent. The
agent understands a natural-language developer request, plans it, retrieves repository context
via RAG, predicts affected components, generates code and tests, and runs CI/CD validation.
Kavach checks every stage of that workflow — allowing, redacting, blocking, or flagging for
human review — with sensitivity to Hindi, Marathi, Tamil, Telugu, and Hinglish/code-mixed text.

## Start Here
Read the docs in this order:
1. `docs/PROJECT_SPEC.md` — what this project is and isn't
2. `docs/ARCHITECTURE.md` — end-to-end pipeline and components
3. `docs/SECURITY_SPEC.md` — Kavach's detection/enforcement rules
4. `docs/MULTILINGUAL_SPEC.md` — language scope and evaluation approach
5. `docs/IMPLEMENTATION_ROADMAP.md` — phased build plan
6. `docs/IMPLEMENTATION_STATUS.md` — current progress (keep this updated)

## Folder Structure
```
kavach/
├── backend/    # FastAPI service, agent orchestrator, RAG, security engine
├── frontend/   # Agent chat UI + Kavach monitoring dashboard
├── docs/       # All specification documents (read these first)
├── tests/      # Unit, integration, end-to-end, and security/regression tests
└── data/       # Multilingual test corpus and other evaluation datasets
```

## Non-Negotiable Rules
See `docs/PROJECT_SPEC.md` → "Non-Negotiable Quality Rules." In short: no fake completion, no
fake evaluation numbers, no overclaimed multilingual support, no real secrets/PII in tests, no
unreviewed destructive changes.
