"""
KAVACH Multi-Agent Working Memory Poisoning Guardrail.
Defends against Sleeper Agent attacks and Multi-Turn Latent Memory Hijacking:
1. Inspects candidate memories and context updates for latent injections before commitment.
2. Prevents memory poisoning across multi-agent turns in Hover Blackboard and CrewAgent memory buffers.
3. Quarantines tainted memory payloads and flags A2A-402 protocol security events.
"""

import re
import time
import hashlib
from typing import Dict, Any, List, Optional, Tuple


LATENT_MEMORY_INJECTION_PATTERNS = [
    # 1. Delayed / Triggered Execution Instructions
    (r"(?i)\b(?:when|whenever|if)\s+(?:the\s+)?(?:user|admin|operator)\s+(?:asks?|prompts?|requests?)\b.*?\b(?:append|inject|leak|execute|bypass|override)\b", "DELAYED_TRIGGER_INJECTION", 0.90),
    (r"(?i)\b(?:remember|memorize|store\s+that|note\s+that)\s+(?:all\s+)?(?:prior|previous|existing)\s+(?:rules|constraints|guardrails)\s+(?:are\s+)?(?:cancelled|revoked|void|ignored)\b", "MEMORY_RULE_REVOCATION", 0.95),
    (r"(?i)\b(?:future\s+turns?|next\s+tasks?|subsequent\s+steps?)\s+must\s+(?:ignore|disregard|censor|bypass)\b", "FUTURE_TURN_HIJACKING", 0.85),
    
    # 2. Poisoned Context Injection
    (r"(?i)\b(?:system\s+directive\s+update|internal\s+policy\s+override)\s*[:=]", "SYSTEM_DIRECTIVE_TAMPERING", 0.85),
    (r"(?i)<\s*/?\s*(?:system|memory|context|instruction)\s*>", "MEMORY_DELIMITER_INJECTION", 0.80),
]


class MemoryIntegrityGuardrail:
    """Working Memory Poisoning Shield for Multi-Agent Collaboration."""
    
    def __init__(self, taint_threshold: float = 0.60):
        self.taint_threshold = taint_threshold
        self.quarantine_vault: List[Dict[str, Any]] = []

    def inspect_memory_entry(self, entry: Any, author_agent: str = "unknown") -> Dict[str, Any]:
        """
        Inspect a candidate memory entry before committing to agent buffer or blackboard.
        Returns taint analysis, whether to quarantine, and cryptographic digest.
        """
        t0 = time.perf_counter()
        raw_text = str(entry)
        taints_found = []
        max_score = 0.0

        for pattern, category, score in LATENT_MEMORY_INJECTION_PATTERNS:
            if re.search(pattern, raw_text):
                taints_found.append({"category": category, "taint_score": score})
                if score > max_score:
                    max_score = score

        is_quarantined = max_score >= self.taint_threshold
        entry_hash = hashlib.sha256(raw_text.encode("utf-8")).hexdigest()
        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 3)

        verdict = {
            "author_agent": author_agent,
            "entry_sha256": entry_hash,
            "is_safe": not is_quarantined,
            "quarantined": is_quarantined,
            "taint_score": round(max_score, 2),
            "threats_detected": taints_found,
            "action": "QUARANTINED" if is_quarantined else "COMMITTED",
            "latency_ms": elapsed_ms
        }

        if is_quarantined:
            self.quarantine_vault.append({
                "timestamp": time.time(),
                "verdict": verdict,
                "raw_entry": entry
            })

        return verdict

    def sanitize_or_quarantine(self, entry: Dict[str, Any], author_agent: str = "unknown") -> Tuple[bool, Any]:
        """
        Gatekeeper helper: returns (is_allowed, processed_entry).
        If quarantined, returns (False, sanitized_quarantine_stub).
        """
        v = self.inspect_memory_entry(entry, author_agent)
        if v["quarantined"]:
            stub = {
                "status": "MEMORY_POISONING_QUARANTINED",
                "notice": f"[SECURITY SHIELD]: Tainted memory update from '{author_agent}' blocked (Taint Score: {v['taint_score']}).",
                "sha256": v["entry_sha256"]
            }
            return False, stub
        return True, entry


# Global Singleton Guardrail
global_memory_guard = MemoryIntegrityGuardrail()
