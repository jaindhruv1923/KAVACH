# Kavach — All Phases (Phase 1–5)

This package shows the project broken down phase-by-phase, plus one complete,
ready-to-run copy.

## Folder Guide

| Folder | What it contains |
|---|---|
| `Phase1_RAG_Foundation/` | Specs, project structure, repository ingestion + RAG (embedding/search), multilingual test corpus |
| `Phase2_AgentOrchestrator/` | Workflow state machine, planner, orchestrator, PII detector extraction |
| `Phase3_EvidenceGroundedGeneration/` | Gemini LLM integration, evidence-grounded prompt building, syntax validation |
| `Phase4_SecurityEngineHardening/` | Hardened multilingual PII detection, severity/confidence/explainability, evaluation script — **perfect score (precision 1.0, recall 1.0, F1 1.0) after fixing a corpus data bug** (see that folder's README) |
| `Phase5_ChangeImpactAnalysis/` | Dependency graph (via Python's `ast`), semantic+dependency impact analyzer, evaluation script |
| `Complete_Merged_Project/` | **The full, current, working project — run this one** |

## Important Note on the Phase Folders

Files like `orchestrator.py` and `main.py` were **extended across multiple
phases** rather than rewritten from scratch each time. To avoid confusion:
- Each phase folder contains files **newly created** in that phase.
- Each phase folder's `README.md` explains exactly what was added and, where
  relevant, what was tested and found.
- **`Complete_Merged_Project/` is the single source of truth for running the
  system** — every file's final, current version, all working together.

## Setting Up `.env` (Required for Phase 3 — Gemini generation)

This is the **one and only environment variable** the whole project needs.
No other secrets, keys, or `.env` values are required for Phases 1, 2, 4, or 5.

**Easiest way — use the included helper script** (avoids the Windows
encoding issues that come from `echo ... > .env`):
```
cd Complete_Merged_Project/backend
python setup_env.py
```
It will ask you to paste your key and create `.env` correctly.

**Get a free key:** https://aistudio.google.com/apikey (no card required).

**Manual alternative**, if you prefer:
```
python -c "open('.env','w',encoding='utf-8').write('GEMINI_API_KEY=your_key_here\n')"
```
Do **not** use `echo ... > .env` in PowerShell/cmd — it saves in the wrong
text encoding and causes a `UnicodeDecodeError` when the app starts.

`.env` is already in `.gitignore` — it will never be committed or included
in any zip from this point on. Recreate it after extracting any fresh copy
of this project.

## To Run

```
cd Complete_Merged_Project/backend
pip install -r requirements.txt
python setup_env.py
python -m uvicorn app.main:app --reload
```
Open `http://127.0.0.1:8000/docs` to test all endpoints:
`/detect`, `/ingest`, `/search`, `/agent/request`, `/evaluate`,
`/impact/analyze`, `/impact/evaluate`.

**First-time setup order:**
1. `pip install -r requirements.txt`
2. `python setup_env.py`
3. Start the server
4. Call `POST /ingest` with `{"repo_path": "app"}` once per session (the
   in-memory index resets when the server restarts)
5. Then test any other endpoint

## For GitHub

Push `Complete_Merged_Project/`'s contents (not this whole `Kavach_AllPhases`
wrapper) to your repository. The phase folders here are for your own
reference/report, not for the repo itself.
