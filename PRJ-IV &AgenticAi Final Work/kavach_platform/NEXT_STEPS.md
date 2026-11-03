# NEXT STEPS (Deliberately Deferred Scope)

**Stage**: CORRECTION (Post Verification Audit)  
**Repository**: KAVACH (`https://github.com/jaindhruv1923/KAVACH.git`)  
**Principle**: Measured reality is the source of truth. Scope discipline maintained strictly under the ~1 hour rule.

---

The following items were identified during the audit or correction stage and **deliberately deferred** to maintain strict scope discipline, avoid unverified claims, and adhere to Hard Rule 1, 2, and 7:

## 1. Detector Refinement for 10-Digit Alphanumeric False Positives (Held-Out V2)
- **Observation**: In `data/held_out_eval_v2.json`, 3 false positives occurred on alphanumeric tracking codes and SKU strings (`BLK-9876543210`, `TR-4455667788`, `SKU 9988776655`) because the 10-digit number matches phone or sensitive numeric sequence patterns after hyphens or whitespace.
- **Why Deferred**: Hard Rule 2 requires that detector improvements be made only in separate commits with a newly created held-out v3 set (at least 40 fresh cases) written before touching any detector. Rather than rushing pattern tweaks that could induce regressions, the 89.3% precision / 100% recall on V2 is reported honestly with full disclosure.
- **Next Action**: Introduce prefix-boundary disambiguation in `patterns.py` to check for order/SKU prefix patterns before tagging mobile phone numbers, validated against a new V3 held-out evaluation set.

## 2. Production PostgreSQL Database Persistence
- **Observation**: `state.py` uses an in-memory run store, while `persistent_store.py` provides an ACID SQLite store with WAL mode. Full enterprise deployment with PostgreSQL is specified in `docs/DATABASE_SPEC.md`.
- **Why Deferred**: Provisioning and validating a production PostgreSQL cluster takes >1 hour, introduces external network dependencies, and would break standalone local execution (`run_all.bat`).
- **Next Action**: Add a database driver toggle (`DATABASE_URL=postgresql://...`) with SQLAlchemy / asyncpg migrations in Alembic.

## 3. Real External Third-Party Library Integration (`google-adk` & `crewai`)
- **Observation**: The repository currently contains custom architectural implementations (`app/adk/` and `app/crew/`) that faithfully mirror the Google ADK 8-hook callback structure and CrewAI sequential/hierarchical flow patterns without pip dependencies.
- **Why Deferred**: Pulling in full heavy framework dependencies (`crewai`, `google-adk`) increases repository size, introduces deep dependency conflicts on Python 3.14, and takes >1 hour to configure.
- **Next Action**: Keep the clean, fast in-repo ADK-pattern and CrewAI-pattern engines as the default reference architecture, and provide optional plugin adapters for users who want to run live CrewAI agents with LangChain.

## 4. Full ReAct Sandbox Tool-Execution Loop with Containerized MicroVMs
- **Observation**: The self-healing loop in `self_healer.py` validates syntax and runs AST-based assertions, but does not spin up isolated Firecracker microVMs or Docker containers for untrusted execution.
- **Why Deferred**: Containerized execution environments require elevated host privileges and platform-specific daemons (Docker Desktop on Windows), exceeding local standalone constraints.
- **Next Action**: Integrate with gVisor / Docker SDK for Python to run containerized sandbox execution when Docker is available.
