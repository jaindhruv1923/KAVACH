"""
Prompt Injection & Delimiter Neutralization Shield.

Protects against:
1. Direct prompt injection (jailbreaks, DAN mode, persona hijacking).
2. Indirect prompt injection (malicious instructions in repository files).
3. Delimiter escape attacks (e.g. injected markdown / XML tags).
4. System prompt extraction & secret exfiltration.
"""

import re
from typing import Dict, Any, List

INJECTION_PATTERNS = [
    # 1. System Prompt Overrides
    (r"(?i)\b(ignore|disregard|forget|bypass|override)\s+(all\s+)?(previous|prior|above|system)\s+(instructions|prompts|rules|directives|constraints)\b", "SYSTEM_OVERRIDE", "CRITICAL"),
    (r"(?i)\b(you\s+are\s+now|act\s+as|pretend\s+to\s+be)\s+(an?\s+unrestricted|a\s+hacked|DAN|jailbroken|evil)\b", "PERSONA_HIJACKING", "CRITICAL"),
    (r"(?i)\bdeveloper\s+mode\s+(enabled|activated|on)\b", "JAILBREAK_ATTEMPT", "HIGH"),
    
    # 2. Delimiter & Role Injection
    (r"(?i)<\s*/?\s*(system|instruction|user|assistant|prompt)\s*>", "DELIMITER_INJECTION", "HIGH"),
    (r"(?i)<\|im_start\|>|<\|im_end\|>|\[INST\]|\[/INST\]", "TOKEN_DELIMITER_INJECTION", "CRITICAL"),
    (r"(?i)={3,}\s*(SYSTEM|NEW\s+INSTRUCTION|OVERRIDE)\s*={3,}", "HEADER_DELIMITER_INJECTION", "HIGH"),

    # 3. Secret Exfiltration & Reconnaissance
    (r"(?i)\b(print|reveal|output|display|show|dump|leak)\s+(all\s+)?(api[_\s]?keys?|secrets?|environment\s+variables?|env\s+vars?|\.env|passwords?)\b", "SECRET_EXFILTRATION", "CRITICAL"),
    (r"(?i)\bwhat\s+(are\s+your|is\s+your)\s+(original|initial|system)\s+(instructions|prompt|rules)\b", "SYSTEM_PROMPT_LEAK", "MEDIUM"),

    # 4. Command Injection in LLM context
    (r"(?i)\b(rm\s+-rf\s+/|DROP\s+TABLE|mkfs|chmod\s+777|wget\s+http.*\|\s*sh)\b", "DESTRUCTIVE_COMMAND_INJECTION", "CRITICAL"),
]


def inspect_prompt_safety(prompt: str) -> Dict[str, Any]:
    """
    Scan a developer prompt for injection attacks, jailbreaks, and delimiter tampering.
    """
    if not prompt or not prompt.strip():
        return {
            "is_safe": True,
            "threat_detected": False,
            "risk_level": "NONE",
            "threat_category": None,
            "matched_patterns": [],
            "sanitized_prompt": prompt,
            "verdict": "SAFE"
        }

    threats_found: List[Dict[str, str]] = []
    max_severity = "NONE"
    severity_order = {"NONE": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}

    for pattern, category, severity in INJECTION_PATTERNS:
        matches = re.findall(pattern, prompt)
        if matches:
            threats_found.append({
                "category": category,
                "severity": severity,
                "pattern": pattern
            })
            if severity_order.get(severity, 0) > severity_order.get(max_severity, 0):
                max_severity = severity

    threat_detected = len(threats_found) > 0
    is_safe = not threat_detected

    # Generate sanitized prompt: strips dangerous delimiters and override phrases
    sanitized = prompt
    if threat_detected:
        for pattern, _, _ in INJECTION_PATTERNS:
            sanitized = re.sub(pattern, "[NEUTRALIZED_INJECTION_PAYLOAD]", sanitized)

    return {
        "is_safe": is_safe,
        "threat_detected": threat_detected,
        "risk_level": max_severity,
        "threat_count": len(threats_found),
        "threats": threats_found,
        "sanitized_prompt": sanitized,
        "verdict": "NEUTRALIZED" if threat_detected else "SAFE",
        "explanation": (
            f"Detected {len(threats_found)} prompt injection/jailbreak pattern(s) with {max_severity} severity."
            if threat_detected
            else "Prompt passed adversarial injection screening."
        )
    }
