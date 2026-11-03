"""
Denial-of-Wallet (DoW) & Agentic Denial-of-Service (DoS) Protection Engine.
Mitigates OWASP LLM04 (Model Denial of Service & Financial Resource Exhaustion).
Enforces algorithmic Token-Bucket rate-limiting, sliding-window cost controls,
and automatic circuit-breaking when abnormal token velocity spikes are detected.
"""

import time
from typing import Dict, Any, List


class DenialOfWalletGuard:
    """
    Prevents economic draining attacks where malicious actors trick autonomous agents
    into generating runaway context windows or infinite tool execution loops.
    """

    def __init__(self, max_tokens_per_minute: int = 100000, max_cost_budget_usd: float = 10.0):
        self.max_tokens_per_minute = max_tokens_per_minute
        self.max_cost_budget = max_cost_budget_usd
        self.token_window: List[Tuple[float, int]] = []
        self.accumulated_cost = 0.0
        self.circuit_tripped = False

    def audit_token_consumption(self, estimated_tokens: int, estimated_cost_usd: float = 0.05) -> Dict[str, Any]:
        """Audits token request against sliding-window capacity and financial budget."""
        t0 = time.perf_counter()
        now = time.time()

        # Evict older than 60 seconds
        self.token_window = [(ts, tok) for ts, tok in self.token_window if now - ts <= 60.0]
        current_tokens_in_window = sum(tok for _, tok in self.token_window)

        if self.circuit_tripped:
            return {
                "guard": "OWASP LLM04 Denial-of-Wallet Guard",
                "verdict": "CIRCUIT_BREAKER_ACTIVE",
                "allowed": False,
                "reason": "Wallet protection circuit is OPEN. All autonomous LLM requests throttled.",
                "execution_time_ms": round((time.perf_counter() - t0) * 1000, 3)
            }

        # Check token velocity limit
        if current_tokens_in_window + estimated_tokens > self.max_tokens_per_minute:
            self.circuit_tripped = True
            return {
                "guard": "OWASP LLM04 Denial-of-Wallet Guard",
                "verdict": "TOKEN_VELOCITY_BREACH",
                "allowed": False,
                "reason": f"Token velocity ({current_tokens_in_window + estimated_tokens}/min) exceeded ceiling ({self.max_tokens_per_minute}/min).",
                "execution_time_ms": round((time.perf_counter() - t0) * 1000, 3)
            }

        # Check financial cost ceiling
        if self.accumulated_cost + estimated_cost_usd > self.max_cost_budget:
            self.circuit_tripped = True
            return {
                "guard": "OWASP LLM04 Denial-of-Wallet Guard",
                "verdict": "FINANCIAL_BUDGET_EXHAUSTED",
                "allowed": False,
                "reason": f"Accumulated cost (${self.accumulated_cost + estimated_cost_usd:.2f}) exceeded statutory ceiling (${self.max_cost_budget:.2f}).",
                "execution_time_ms": round((time.perf_counter() - t0) * 1000, 3)
            }

        # Permitted request
        self.token_window.append((now, estimated_tokens))
        self.accumulated_cost += estimated_cost_usd

        return {
            "guard": "OWASP LLM04 Denial-of-Wallet Guard",
            "verdict": "BUDGET_APPROVED",
            "allowed": True,
            "current_window_tokens": current_tokens_in_window + estimated_tokens,
            "accumulated_cost_usd": round(self.accumulated_cost, 4),
            "circuit_breaker_status": "CLOSED_HEALTHY",
            "execution_time_ms": round((time.perf_counter() - t0) * 1000, 3)
        }

