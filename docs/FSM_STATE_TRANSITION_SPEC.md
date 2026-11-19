# KAVACH: 10-Stage Deterministic FSM State Transition Specification

## 1. State Invariants
- `INGESTION` -> `TRIAGE` -> `RAG_RETRIEVAL` -> `PLANNING` -> `POLICY_CHECK` -> `EXECUTION` -> `GUARDRAIL` -> `VERIFICATION` -> `AUDIT` -> `OUTPUT`

## 2. Safety Bounds
- Circuit breaker trips on any stage latency exceeding 200ms.
- Full AST traversal before shell execution.
- Cryptographic SHA-256 ledger recording for state compliance.