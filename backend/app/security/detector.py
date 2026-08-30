"""
Kavach security detection (early version — see docs/SECURITY_SPEC.md and
docs/PII_PATTERNS.md for the full intended design).

This is the regex-only starting point moved out of main.py so both the
/detect endpoint and the agent orchestrator (Phase 2) share one
implementation instead of duplicating logic. The real Phase 4 build should
replace/extend this with the hybrid regex + context-aware approach described
in PII_PATTERNS.md, plus multilingual support (MULTILINGUAL_SPEC.md).
"""

import re

PAN_PATTERN = re.compile(r"[A-Z]{5}[0-9]{4}[A-Z]{1}")
PHONE_PATTERN = re.compile(r"(\+91[\-\s]?)?[6-9]\d{9}")
EMAIL_PATTERN = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


def detect_pii(text: str) -> list[dict]:
    """
    Scan text for PAN-like, phone-like, and email patterns.
    Returns a list of finding dicts: {category, value, action}.
    """
    findings = []
    if not text:
        return findings

    for match in PAN_PATTERN.finditer(text):
        findings.append({"category": "PAN", "value": match.group(), "action": "BLOCK"})
    for match in PHONE_PATTERN.finditer(text):
        findings.append({"category": "phone_number", "value": match.group(), "action": "REDACT"})
    for match in EMAIL_PATTERN.finditer(text):
        findings.append({"category": "email", "value": match.group(), "action": "REDACT"})

    return findings
