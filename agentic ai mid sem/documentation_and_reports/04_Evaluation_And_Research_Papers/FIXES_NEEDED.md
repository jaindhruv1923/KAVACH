# KAVACH: Post-Verification Fixes & Remediation Ledger

**Audit Date:** 2026-10-25  
**Audit Scope:** Prioritized list of identified code bugs, exception handling vulnerabilities, collection errors, and documentation misalignments.  
**Standard:** Every fix is categorized by severity and grounded in measured evidence.

---

## 1. High Priority: Code Bugs & Test Collection Errors

### FIX-01: Root-Level Pytest Collection Failure on Legacy Scratch Scripts
* **Severity:** **HIGH**
* **Location:** `03_Documentation/Archived_Legacy_Materials/04_Scratch_and_OneOff_Scripts/`
* **Problem:** Files named `test_verify_frontend.py`, `test_verify_motion_design.py`, and `test_verify_terminal_results.py` reside inside documentation archives. When pytest runs from the repository root, it automatically collects these files, causing collection crashes due to missing UI test drivers.
* **Remediation:** 
  1. Add `norecursedirs = 03_Documentation*` in root `pytest.ini`.
  2. Rename archival scratch scripts from `test_*.py` to `verify_*.py` so pytest ignores them during discovery.

### FIX-02: UnicodeDecodeError in `test_results.txt`
* **Severity:** **HIGH**
* **Location:** `01_KAVACH_Platform/artifacts/reports/test_results.txt`
* **Problem:** Pytest attempts to inspect this text file during root collection, throwing `UnicodeDecodeError: 'charmap' codec can't decode byte 0x8f in position 24867`.
* **Remediation:** Ensure pytest ignores `artifacts/` by adding `artifacts` to `norecursedirs` in `pytest.ini`.

### FIX-03: Unhandled `ValueError` in Domain API Endpoints
* **Severity:** **HIGH (VERIFIED FIXED ON CORRECTIONS BRANCH)**
* **Location:** `01_KAVACH_Platform/backend/app/main.py`, Lines 74–82
* **Problem:** Inbound domain validation errors (e.g. invalid GitHub URLs, negative balance transfers) raised standard Python `ValueError`, which uncaught returned `HTTP 500 Internal Server Error`.
* **Remediation:** Added global exception handler:
  ```python
  @app.exception_handler(ValueError)
  async def value_error_handler(request: Request, exc: ValueError):
      return JSONResponse(status_code=400, content={"error": "Bad Request", "detail": str(exc)})
  ```

### FIX-04: Pydantic V2 Deprecation Warnings on Field `example`
* **Severity:** **MEDIUM**
* **Location:** `02_Banking_and_Results_Dashboard/implementation_banks/server.py`, Lines 190–225
* **Problem:** Over 20 routes use `Field(..., example=...)`, which emits runtime warnings: `PydanticDeprecatedSince20: Using extra keyword arguments on Field is deprecated and will be removed in V3.0`.
* **Remediation:** Migrate all occurrences to `Field(..., json_schema_extra={"example": ...})`.

---

## 2. Medium Priority: Documentation Grounding & Alignment

### FIX-05: Remove Unverifiable "Evaluation Score 9.6/10" Badges
* **Severity:** **MEDIUM (VERIFIED FIXED ON CORRECTIONS BRANCH)**
* **Location:** `README.md` and `01_KAVACH_Platform/README.md`
* **Problem:** Subjective evaluation badges (e.g. `Evaluation Score: 9.6/10`, `Production Ready`) were asserted without an empirical test rubric.
* **Remediation:** Replaced with links to `docs/METRICS.md` and grounded test pass metrics (100% pass rate on 300 deterministic verification tests).

### FIX-06: Resolve 106 Broken Asset Links to `important/kavach/...`
* **Severity:** **MEDIUM (VERIFIED FIXED ON CORRECTIONS BRANCH)**
* **Location:** `README.md`
* **Problem:** 106 image and documentation markdown links referenced an obsolete development directory `important/kavach/...`, returning 404 errors.
* **Remediation:** Rewrote all 106 links to point to active relative paths under `01_KAVACH_Platform/...`.

### FIX-07: Update Git Clone URL from Placeholder
* **Severity:** **LOW (VERIFIED FIXED ON CORRECTIONS BRANCH)**
* **Location:** `README.md`
* **Problem:** Clone snippet displayed `https://github.com/your-username/kavach.git`.
* **Remediation:** Updated to active repository URL: `https://github.com/jaindhruv1923/KAVACH.git`.

### FIX-08: Explicitly Label `adk/` and `crew/` as Native Architectural Emulations
* **Severity:** **MEDIUM**
* **Location:** `03_Documentation/` and System Architecture Guides
* **Problem:** Text implied that external pip packages `crewai` and `google-adk` were imported dependencies, which fails audit inspection.
* **Remediation:** Formally relabel as "in-repo architectural pattern emulations" adhering to the specifications without external dependency bloat.

---

## 3. Low Priority: Architectural Enhancements (Roadmap)

### FIX-09: Context Disambiguation Heuristic for Numeric IDs
* **Severity:** **LOW**
* **Location:** `01_KAVACH_Platform/backend/app/security/detector.py`
* **Problem:** 3 false positives occurred during held-out evaluation on 10-digit order numbers (`BLK-9876543210`) and SKU codes (`9988776655`) because they matched mobile phone regexes.
* **Remediation:** Add negative lookbehind heuristics for known prefix tokens (e.g., `(?<!(BLK-|TR-|SKU-))[6-9]\d{9}`) while preserving 100% recall on sensitive personal identifiers.

### FIX-10: Asynchronous Cold-Start Vector Store Pre-Warming
* **Severity:** **LOW**
* **Location:** `01_KAVACH_Platform/backend/app/impact/analyzer.py`
* **Problem:** Cold start of `analyze_impact` takes ~34 seconds due to synchronous neural model loading.
* **Remediation:** Run repository ingestion and model loading in a background worker thread upon application boot so the endpoint responds in sub-50ms immediately.
