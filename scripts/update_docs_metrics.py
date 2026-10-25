# Script to update documentation files to align with docs/METRICS.json SSOT

# 1. Update 01_KAVACH_Platform/README.md
with open("01_KAVACH_Platform/README.md", "r", encoding="utf-8") as f:
    r1 = f.read()

r1 = r1.replace(
    "[← Back to Master Repository README](../../README.md) &nbsp;|&nbsp; [📂 Official Assets Overview (`../`)](../README.md) &nbsp;|&nbsp; [📦 Archived Legacy Files (`../../unimportant`)](../../unimportant/README.md)",
    "[← Back to Master Repository README](../README.md) &nbsp;|&nbsp; [🏦 Banking & Results Cockpit](../02_Banking_and_Results_Dashboard/README.md) &nbsp;|&nbsp; [📚 Master Documentation Hub](../03_Documentation/README.md) &nbsp;|&nbsp; [📈 System Metrics (SSOT)](../docs/METRICS.md)"
)
r1 = r1.replace("278 test results", "300 deterministic verification tests (641 total repository tests, see docs/METRICS.md)")
r1 = r1.replace("278 tests", "300 deterministic tests (641 total repository tests)")
r1 = r1.replace("278 Tests", "300 Deterministic Tests (641 Total)")

with open("01_KAVACH_Platform/README.md", "w", encoding="utf-8") as f:
    f.write(r1)

# 2. Update 01_KAVACH_Platform/FINAL_REPORT.md
with open("01_KAVACH_Platform/FINAL_REPORT.md", "r", encoding="utf-8") as f:
    fr = f.read()

fr = fr.replace(
    "The pytest suite now contains **278 tests**, all passing with a **100% pass rate**.",
    "The project test suite verified in [`docs/METRICS.md`](../docs/METRICS.md) contains **300 deterministic verification tests** (100% pass rate) across 3 master suites, and **641 total repository tests** across 18 test files."
)
fr = fr.replace(
    "achieving a **100.0% Interception Rate**.",
    "achieving a **100.0% Interception Rate** across 19 vectors in the authored adversarial benchmark (see [`docs/METRICS.md`](../docs/METRICS.md))."
)
fr = fr.replace(
    "**Status**: ✅ FULLY OPERATIONAL & READY FOR DEMONSTRATION (278 / 278 TESTS PASSING)",
    "**Status**: ✅ FULLY OPERATIONAL & VERIFIED (300 / 300 DETERMINISTIC TESTS PASSING; 641 TOTAL REPO TESTS PASSING)"
)
fr = fr.replace("**Total Tests**: 278  \n**Passed**: 278  \n**Pass Rate**: 100%  \n**Failed**: 0",
               "**Deterministic Master Tests**: 300  \n**Total Repository Tests**: 641  \n**Passed**: 641  \n**Pass Rate**: 100%  \n**Failed**: 0  \n**Source of Truth**: [`docs/METRICS.md`](../docs/METRICS.md)")

with open("01_KAVACH_Platform/FINAL_REPORT.md", "w", encoding="utf-8") as f:
    f.write(fr)

# 3. Update 01_KAVACH_Platform/PROJECT_MAP.md
with open("01_KAVACH_Platform/PROJECT_MAP.md", "r", encoding="utf-8") as f:
    pm = f.read()

pm = pm.replace(
    "## API layer\n\n- `backend/app/main.py`: FastAPI app, routes, CORS, static dashboard serving, safe configuration status.",
    "## API layer\n\n- `backend/app/main.py`: FastAPI app, 120 registered routes (142 total unified endpoints across platform), CORS, static dashboard serving, safe configuration status (see [`docs/METRICS.md`](../docs/METRICS.md))."
)
pm = pm.replace(
    "- `backend/app/agent/orchestrator.py`: complete request lifecycle and security checkpoints.",
    "- `backend/app/agent/orchestrator.py`: complete request lifecycle across 6 active execution stages (REQUEST_RECEIVED, PLANNING, CONTEXT_RETRIEVAL, SECURITY_CHECK, IMPACT_ANALYSIS, GENERATION) and 3 terminal decision states (COMPLETE, BLOCKED, NEEDS_REVIEW)."
)

# Clarify ADK & Crew in PROJECT_MAP
adk_clarification = """### Agent Framework Implementations (ADK-Pattern & CrewAI-Pattern)

- `backend/app/adk/`: Custom ADK-pattern architectural implementation modeling Google ADK specifications (8-hook callbacks across before/after agent, model, and tool lifecycle phases, LlmAgent, coordinator, and medical triage) with zero external pip dependencies.
- `backend/app/crew/`: Custom CrewAI-pattern architectural flow runner (sequential and hierarchical multi-agent execution) with zero external pip dependencies.
"""
if "Agent Framework Implementations" not in pm:
    pm = pm.replace("### Generation and validation", adk_clarification + "\n### Generation and validation")

with open("01_KAVACH_Platform/PROJECT_MAP.md", "w", encoding="utf-8") as f:
    f.write(pm)

# 4. Update DEPLOYMENT_GUIDE.md clone url
with open("01_KAVACH_Platform/DEPLOYMENT_GUIDE.md", "r", encoding="utf-8") as f:
    dg = f.read()
dg = dg.replace("https://github.com/<your-username>/kavach.git", "https://github.com/jaindhruv1923/KAVACH.git")
with open("01_KAVACH_Platform/DEPLOYMENT_GUIDE.md", "w", encoding="utf-8") as f:
    f.write(dg)

# 5. Update 03_Documentation/02_Official_Reports_and_Synopses/KAVACH_AGENTIC_AI_MASTER_BLUEPRINT.md
blueprint_path = "03_Documentation/02_Official_Reports_and_Synopses/KAVACH_AGENTIC_AI_MASTER_BLUEPRINT.md"
with open(blueprint_path, "r", encoding="utf-8") as f:
    bp = f.read()
bp = bp.replace(
    "### 6.1 Rubric Evaluation against CSE3101 Criteria (Score: 9.6 / 10)",
    "### 6.1 Rubric Self-Assessment and Traceability Matrix against CSE3101 Criteria (Verified Empirical Baseline)"
)
with open(blueprint_path, "w", encoding="utf-8") as f:
    f.write(bp)

print("Documentation files updated successfully.")
