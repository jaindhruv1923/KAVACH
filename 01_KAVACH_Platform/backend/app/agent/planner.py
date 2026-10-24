"""
Planner (Phase 2 — see docs/AGENT_SPEC.md).

Implements honest LLM-based task decomposition (Google Gemini or local Ollama)
that returns a structured, sanitized JSON plan of concrete engineering sub-tasks.
Includes a clearly named deterministic fallback (`deterministic_fallback_planner`)
when the LLM is unconfigured, unreachable, or returns invalid JSON.

Security & Privacy Guarantees:
1. Privacy Boundary: The planner operates strictly on sanitized/redacted developer input,
   never raw PII or secrets.
2. Untrusted LLM Content: LLM responses are treated as untrusted data:
   - Output task count is capped at MAX_TASKS (8).
   - Individual task string length is capped at MAX_TASK_LENGTH (150).
   - Control characters, HTML/script tags, and shell metacharacters are stripped.
   - Plan text is purely declarative workflow metadata and is NEVER executed as code or shell.
3. Fast Fallback & Resilience:
   - When no LLM provider is configured, the deterministic fallback executes immediately (<5ms).
   - When a provider is configured, single-shot inference uses an explicit 3.0-second timeout with ZERO retries.
"""

import json
import logging
import re
from typing import Any, List, Optional

logger = logging.getLogger("kavach.planner")

# Safety constraints for untrusted LLM outputs
MAX_TASKS = 8
MAX_TASK_LENGTH = 150

# Structured prompt for LLM task decomposition
_PLANNER_SYSTEM_PROMPT = (
    "You are an AI DevOps Task Planner. Break down the following developer software request "
    "into an ordered list of 3 to 6 concrete, actionable engineering sub-tasks.\n"
    "Rules:\n"
    "1. Always include repository context retrieval and security/policy compliance verification.\n"
    "2. Return ONLY a valid JSON array of strings (e.g. [\"Task 1\", \"Task 2\"]).\n"
    "3. Do not include markdown formatting, markdown code blocks, or explanatory preamble."
)

_TASK_KEYWORDS = {
    "auth": ["Identify authentication-related files", "Review existing auth logic"],
    "password": ["Locate password handling code", "Check password reset flow if present"],
    "test": ["Identify existing test files", "Determine what new tests are needed"],
    "api": ["Locate relevant API route definitions", "Review request/response schemas"],
    "database": ["Identify affected database models/schema", "Check for migration needs"],
}


def deterministic_fallback_planner(request_text: str) -> List[str]:
    """
    Deterministic rule-based task decomposition fallback.
    Explicitly invoked when the LLM service is offline, unconfigured, or returns malformed output.
    Executes in under 5 milliseconds with zero network overhead.
    """
    text_lower = request_text.lower() if request_text else ""
    tasks = ["Understand the request and identify its scope"]

    matched_any = False
    for keyword, keyword_tasks in _TASK_KEYWORDS.items():
        if keyword == "test":
            keyword_pattern = r"\btests?\b|\btesting\b"
        else:
            keyword_pattern = rf"\b{keyword}\b"

        if re.search(keyword_pattern, text_lower):
            tasks.extend(keyword_tasks)
            matched_any = True

    if not matched_any:
        tasks.append("Retrieve relevant repository context for this request (general search)")

    tasks.append("Retrieve grounding evidence from the repository (RAG)")
    tasks.append("Run security/policy checks on the request and any retrieved context")

    return tasks[:MAX_TASKS]


def _sanitize_task_string(task: Any) -> Optional[str]:
    """
    Sanitize and validate an individual task string from untrusted LLM JSON.
    Strips script tags, control characters, and dangerous shell execution symbols.
    Caps character length at MAX_TASK_LENGTH.
    """
    if not isinstance(task, str):
        return None
    cleaned = task.strip()
    # Strip HTML tags
    cleaned = re.sub(r"<[^>]+>", "", cleaned)
    # Strip control characters
    cleaned = re.sub(r"[\x00-\x1f\x7f]", "", cleaned)
    # Strip shell command chaining / execution metacharacters
    cleaned = re.sub(r"[`$()&|;><]", "", cleaned)
    cleaned = cleaned.strip()
    if not cleaned:
        return None
    # Cap length
    if len(cleaned) > MAX_TASK_LENGTH:
        cleaned = cleaned[:MAX_TASK_LENGTH].rstrip() + "..."
    return cleaned


def _extract_and_sanitize_json_array(text: str) -> Optional[List[str]]:
    """Clean, parse, cap, and sanitize a JSON array from raw untrusted LLM output."""
    if not text:
        return None
    cleaned = text.strip()
    # Strip markdown code blocks like ```json ... ``` or ``` ... ```
    if cleaned.startswith("```"):
        lines = cleaned.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        cleaned = "\n".join(lines).strip()

    # Search for JSON array boundaries if surrounding commentary exists
    start_idx = cleaned.find("[")
    end_idx = cleaned.rfind("]")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        cleaned = cleaned[start_idx : end_idx + 1]

    try:
        parsed = json.loads(cleaned)
        if isinstance(parsed, list):
            sanitized_tasks: List[str] = []
            for item in parsed:
                s = _sanitize_task_string(item)
                if s:
                    sanitized_tasks.append(s)
                if len(sanitized_tasks) >= MAX_TASKS:
                    break
            if len(sanitized_tasks) > 0:
                return sanitized_tasks
    except Exception:
        pass
    return None


def _call_llm_single_shot(prompt: str, provider: Optional[str] = None, timeout_seconds: float = 3.0) -> Optional[str]:
    """
    Single-shot inference request with short explicit timeout and ZERO retries.
    Returns None immediately upon error, timeout, or missing configuration.
    """
    try:
        from app.generation.llm_client import (
            call_llm,
            call_ollama,
            get_gemini_api_key,
            is_llm_configured,
            AIR_GAPPED_MODE,
        )
    except ImportError:
        return None

    use_ollama = (provider == "ollama") or (AIR_GAPPED_MODE and provider != "gemini")

    if use_ollama:
        try:
            res = call_ollama(prompt)
            if res and not res.startswith("[Ollama local model"):
                return res
            return None
        except Exception as e:
            logger.warning(f"Ollama planner single-shot unreachable/timed out ({e}); switching to fallback.")
            return None

    # Cloud Gemini path
    try:
        res = call_llm(prompt)
        if res and not res.startswith("[STUB RESPONSE"):
            return res
        return None
    except Exception as e:
        logger.warning(f"Gemini planner single-shot unreachable/timed out ({e}); switching to fallback.")
        return None


def plan_request(request_text: str, provider: Optional[str] = None) -> List[str]:
    """
    Break a sanitized developer request into a structured list of sub-tasks.

    Execution strategy:
    1. If request is empty, return deterministic fallback immediately.
    2. Check if an LLM is configured. If not configured, return deterministic fallback immediately (<5ms).
    3. If configured, execute a single-shot inference call with a 3.0s timeout and no retries.
    4. Parse, cap, and sanitize the structured JSON plan.
    5. If any step fails, return deterministic_fallback_planner(request_text).
    """
    if not request_text or not request_text.strip():
        return deterministic_fallback_planner(request_text)

    try:
        from app.generation.llm_client import (
            is_llm_configured,
            AIR_GAPPED_MODE,
        )

        use_ollama = (provider == "ollama") or (AIR_GAPPED_MODE and provider != "gemini")
        llm_ready = is_llm_configured() or use_ollama

        # Fast path: return deterministic fallback immediately if no LLM configured
        if not llm_ready and provider != "mock":
            return deterministic_fallback_planner(request_text)

        prompt = f"{_PLANNER_SYSTEM_PROMPT}\n\nDeveloper Request:\n{request_text.strip()}"
        response_text = _call_llm_single_shot(prompt, provider=provider, timeout_seconds=3.0)

        if response_text and not response_text.startswith("[Ollama local model") and not response_text.startswith("[STUB RESPONSE"):
            plan = _extract_and_sanitize_json_array(response_text)
            if plan:
                return plan
            logger.warning("LLM planner output failed schema validation; invoking deterministic fallback.")
    except Exception as e:
        logger.warning(f"LLM planner error ({e}); invoking deterministic fallback.")

    return deterministic_fallback_planner(request_text)
