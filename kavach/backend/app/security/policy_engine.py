"""
Risk-adaptive, action-aware policy engine (Part 2 — addresses Limitation #4:
"Binary Decisions Need Risk-Adaptive and Action-Aware Policy").

Before: a single finding with action=BLOCK immediately stopped the
workflow, regardless of how sensitive the *requested action* itself was.
After: the policy combines (a) the sensitivity of what was found and
(b) the risk of what the developer is asking the agent to *do* with it,
into one risk score, before deciding ALLOW / REVIEW / BLOCK / REDACT.

This does not replace security/detector.py or secret_detector.py — it
consumes their findings as input. Detection and decision remain separate
concerns, as the limitations document recommends.
"""

from enum import Enum


class PolicyAction(str, Enum):
    ALLOW = "ALLOW"
    REDACT = "REDACT"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


# Action-risk classification: what is the developer asking the agent to DO.
# This is a starting, deliberately small keyword-based classifier — see
# KAVACH_LIMITATIONS.md for why a fuller intent classifier is out of scope
# for this pass.
HIGH_RISK_ACTION_KEYWORDS = [
    "delete", "drop table", "truncate", "remove all", "wipe", "destroy",
    "rm -rf", "format", "purge",
]
MEDIUM_RISK_ACTION_KEYWORDS = [
    "modify", "update", "change", "alter", "migrate", "deploy", "write to",
    "overwrite",
]
# Anything not matching either list defaults to LOW (e.g. "explain",
# "add a new endpoint", "show me").

SEVERITY_WEIGHTS = {"critical": 1.0, "high": 0.8, "medium": 0.5, "low": 0.2}
ACTION_WEIGHTS = {"high": 0.9, "medium": 0.5, "low": 0.1}


def classify_action_risk(request_text: str) -> str:
    """Classify the requested action's inherent risk: high/medium/low."""
    lower = request_text.lower()
    if any(kw in lower for kw in HIGH_RISK_ACTION_KEYWORDS):
        return "high"
    if any(kw in lower for kw in MEDIUM_RISK_ACTION_KEYWORDS):
        return "medium"
    return "low"


def compute_risk_score(findings: list[dict], action_risk: str) -> float:
    """
    Combine data-sensitivity risk and action risk into one score, 0.0-1.0.
    A high-severity finding on a low-risk action ("explain this PAN
    format") scores lower than the same finding on a high-risk action
    ("delete records matching this PAN") — this is the "action-aware"
    part the limitations document asks for.
    """
    if not findings:
        data_risk = 0.0
    else:
        # Use the single highest-severity finding as the data-risk signal —
        # one critical finding matters more than many low-severity ones.
        data_risk = max(SEVERITY_WEIGHTS.get(f.get("severity", "low"), 0.2) for f in findings)

    action_weight = ACTION_WEIGHTS.get(action_risk, 0.1)

    # Weighted combination: data sensitivity matters more than action risk
    # alone (a low-risk action on a critical secret is still dangerous),
    # but action risk amplifies it rather than being purely additive.
    combined = data_risk * (0.7 + 0.3 * action_weight)
    return round(min(combined, 1.0), 3)


def decide_policy_action(risk_score: float, findings: list[dict]) -> PolicyAction:
    """
    Map a risk score to a policy action. Thresholds are a starting,
    documented default — see KAVACH_LIMITATIONS.md for why these are not
    yet calibrated against a labeled risk dataset.
    """
    has_credential = any(f.get("category") == "credential" for f in findings)

    if has_credential or risk_score >= 0.75:
        return PolicyAction.BLOCK
    if risk_score >= 0.45:
        return PolicyAction.REVIEW
    if risk_score >= 0.15:
        return PolicyAction.REDACT
    return PolicyAction.ALLOW


def evaluate_policy(request_text: str, findings: list[dict]) -> dict:
    """
    Full policy evaluation: classify action risk, combine with data risk,
    decide an action, and return an explainable decision object.
    """
    action_risk = classify_action_risk(request_text)
    risk_score = compute_risk_score(findings, action_risk)
    decision = decide_policy_action(risk_score, findings)

    return {
        "decision": decision.value,
        "risk_score": risk_score,
        "action_risk_classification": action_risk,
        "data_findings_count": len(findings),
        "highest_severity": max((f.get("severity", "low") for f in findings), default="none",
                                  key=lambda s: SEVERITY_WEIGHTS.get(s, 0)),
        "explanation": _build_explanation(decision, action_risk, findings),
    }


def _build_explanation(decision: PolicyAction, action_risk: str, findings: list[dict]) -> str:
    if decision == PolicyAction.ALLOW:
        return "No significant sensitive-data or high-risk-action signal detected."
    categories = sorted(set(f.get("category", "unknown") for f in findings))
    cat_str = ", ".join(categories) if categories else "none"
    return (
        f"Decision={decision.value} based on detected categories [{cat_str}] "
        f"combined with a '{action_risk}'-risk requested action."
    )
