"""
Kavach security detection engine.

Detects sensitive PII and identifiers:
  - PAN (Permanent Account Number)
  - Aadhaar / National ID (12-digit formatted or unformatted validated with Verhoeff checksum)
  - Phone numbers (10 digits)
  - Email addresses
  - Bank account numbers & generic sensitive numeric identifiers (9-18 digits)
"""

import re
from app.security.patterns import (
    PAN_PATTERN,
    AADHAAR_PATTERN,
    PHONE_PATTERN,
    EMAIL_PATTERN,
    GENERIC_LONG_DIGITS,
    BANK_ACCOUNT_CONTEXT_WORDS,
    AADHAAR_CONTEXT_WORDS,
    PAN_CONTEXT_WORDS,
    _has_nearby_context,
)
from app.security.verhoeff import validate_aadhaar_candidate

# Severity + default action per category
SEVERITY_MAP = {
    "PAN": {"severity": "high", "action": "BLOCK"},
    "Aadhaar-like": {"severity": "high", "action": "BLOCK"},
    "bank_account": {"severity": "high", "action": "BLOCK"},
    "possible_id": {"severity": "low", "action": "REDACT"},
    "sensitive_number": {"severity": "low", "action": "REDACT"},
    "phone_number": {"severity": "medium", "action": "REDACT"},
    "email": {"severity": "medium", "action": "REDACT"},
}


def _make_finding(category: str, value: str, confidence: float, reason: str) -> dict:
    meta = SEVERITY_MAP.get(category, {"severity": "high", "action": "BLOCK"})
    return {
        "category": category,
        "value": value,
        "action": meta["action"],
        "severity": meta["severity"],
        "confidence": round(confidence, 2),
        "reason": reason,
    }


def detect_pii(text: str) -> list[dict]:
    """
    Scan text for PAN, Aadhaar-like, phone, email, bank-account, and sensitive numeric patterns.
    Returns a list of finding dicts: {category, value, action, severity, confidence, reason}.
    """
    findings = []
    if not text:
        return findings

    # --- PAN: 5 letters + 4 digits + 1 letter ---
    for match in PAN_PATTERN.finditer(text):
        has_context = _has_nearby_context(text, match.start(), match.end(), PAN_CONTEXT_WORDS)
        confidence = 0.95 if has_context else 0.85
        reason = (
            "Matches PAN format (5 letters + 4 digits + 1 letter)"
            + (", with PAN context nearby" if has_context else "")
        )
        findings.append(_make_finding("PAN", match.group(), confidence, reason))

    # --- Aadhaar-like / 12-digit candidate ---
    for match in AADHAAR_PATTERN.finditer(text):
        val = match.group()
        # Ensure it is a 12-digit number (formatted or plain)
        digits_only = re.sub(r"\D", "", val)
        if len(digits_only) == 12:
            has_bank_ctx = _has_nearby_context(text, match.start(), match.end(), BANK_ACCOUNT_CONTEXT_WORDS)
            if has_bank_ctx:
                findings.append(_make_finding(
                    "bank_account", val, 0.90,
                    f"12-digit number with bank/account context: {val}"
                ))
                continue

            has_context = _has_nearby_context(text, match.start(), match.end(), AADHAAR_CONTEXT_WORDS)
            v_res = validate_aadhaar_candidate(val)

            if v_res["is_valid_aadhaar"]:
                if has_context:
                    findings.append(_make_finding(
                        "Aadhaar-like", val, 0.98,
                        f"12-digit verified national identifier (Aadhaar format with valid Verhoeff checksum: {val}), with identity context nearby"
                    ))
                else:
                    # 12-digit candidate satisfies Verhoeff, but lacks identity context
                    # Categorize as low-confidence possible_id (REDACT, not hard BLOCK)
                    findings.append(_make_finding(
                        "possible_id", val, 0.60,
                        f"12-digit candidate with valid Verhoeff checksum, but lacking identity context (possible ID): {val}"
                    ))
            elif has_context:
                # 12 digits near identity context, but failed Verhoeff checksum or invalid leading 0/1
                # Clearly label as low-confidence possible ID; DO NOT trigger hard BLOCK.
                findings.append(_make_finding(
                    "possible_id", val, 0.40,
                    f"Possible ID candidate with identity context, but failed Aadhaar validation: {v_res['reject_reason']} ({val})"
                ))
            else:
                # Random 12-digit number (order number, tracking number, timestamp) with NO identity context and NO valid Verhoeff.
                # Do NOT flag as Aadhaar-like!
                pass

    # --- Phone number: 10 digits (with optional +91) ---
    for match in PHONE_PATTERN.finditer(text):
        val = match.group()
        # Avoid double-counting if part of an already detected entity
        if any(val in f["value"] for f in findings):
            continue
        findings.append(_make_finding(
            "phone_number", val, 0.85,
            f"Matches mobile phone number format: {val}"
        ))

    # --- Email: standard format ---
    for match in EMAIL_PATTERN.finditer(text):
        findings.append(_make_finding("email", match.group(), 0.95, "Matches email address format"))

    # --- Generic Long Digits / Sensitive numbers / Bank accounts (9-18 digits) ---
    for match in GENERIC_LONG_DIGITS.finditer(text):
        val = match.group()
        digits_only = re.sub(r"\D", "", val)

        # Skip if this digit sequence was already claimed by Aadhaar or phone above
        already_claimed = any(
            digits_only == re.sub(r"\D", "", f["value"]) or val in f["value"] or f["value"] in val
            for f in findings
        )
        if already_claimed:
            continue

        has_aadhaar_ctx = _has_nearby_context(text, match.start(), match.end(), AADHAAR_CONTEXT_WORDS)
        has_bank_ctx = _has_nearby_context(text, match.start(), match.end(), BANK_ACCOUNT_CONTEXT_WORDS)

        if has_aadhaar_ctx:
            if len(digits_only) == 12:
                v_res = validate_aadhaar_candidate(val)
                if v_res["is_valid_aadhaar"]:
                    findings.append(_make_finding(
                        "Aadhaar-like", val, 0.95,
                        f"Verified Aadhaar national identifier (valid Verhoeff checksum): {val}"
                    ))
                else:
                    findings.append(_make_finding(
                        "possible_id", val, 0.40,
                        f"Possible ID candidate with identity context, but failed Aadhaar validation: {v_res['reject_reason']} ({val})"
                    ))
            else:
                findings.append(_make_finding(
                    "possible_id", val, 0.40,
                    f"Possible ID candidate near identity context ({len(digits_only)} digits): {val}"
                ))
        elif has_bank_ctx:
            findings.append(_make_finding(
                "bank_account", val, 0.85,
                f"9-18 digit number with bank/account context: {val}"
            ))
        else:
            findings.append(_make_finding(
                "sensitive_number", val, 0.50,
                f"Numeric identifier sequence: {val}"
            ))

    return findings
