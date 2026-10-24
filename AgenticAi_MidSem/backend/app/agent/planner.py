"""
Planner (Phase 2 — see docs/AGENT_SPEC.md).

Implements honest LLM-based task decomposition (Google Gemini or local Ollama)
that returns a structured JSON plan of concrete engineering sub-tasks.
Includes a clearly named deterministic fallback (`deterministic_fallback_planner`)
when the LLM is unconfigured, unreachable, or returns invalid JSON.
"""

import json
import logging
import re
from typing import List, Optional

logger = logging.getLogger("kavach.planner")

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

    return tasks


def _extract_json_array(text: str) -> Optional[List[str]]:
    """Clean and parse a JSON array from raw LLM output, stripping markdown fences if present."""
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
        if isinstance(parsed, list) and all(isinstance(item, str) for item in parsed) and len(parsed) > 0:
            return parsed
    except Exception:
        pass
    return None


def plan_request(request_text: str, provider: Optional[str] = None) -> List[str]:
    """
    Break a natural-language developer request into a structured list of sub-tasks.

    Execution strategy:
    1. Attempts honest LLM task decomposition via Gemini or Ollama.
    2. Parses and validates the structured JSON plan.
    3. If LLM is unconfigured, unreachable, or fails schema validation,
       gracefully switches to `deterministic_fallback_planner`.
    """
    if not request_text or not request_text.strip():
        return deterministic_fallback_planner(request_text)

    # Check if LLM is available
    try:
        from app.generation.llm_client import (
            call_llm,
            call_ollama,
            is_llm_configured,
            AIR_GAPPED_MODE,
        )

        use_ollama = (provider == "ollama") or (AIR_GAPPED_MODE and provider != "gemini")
        llm_ready = is_llm_configured() or use_ollama

        if llm_ready:
            prompt = f"{_PLANNER_SYSTEM_PROMPT}\n\nDeveloper Request:\n{request_text.strip()}"
            if use_ollama:
                response_text = call_ollama(prompt)
            else:
                response_text = call_llm(prompt)

            if response_text and not response_text.startswith("[Ollama local model") and not response_text.startswith("[STUB RESPONSE"):
                plan = _extract_json_array(response_text)
                if plan:
                    return plan
                logger.warning("LLM planner output failed JSON schema validation; invoking deterministic fallback.")
    except Exception as e:
        logger.warning(f"LLM planner invocation error: {e}; invoking deterministic fallback.")

    return deterministic_fallback_planner(request_text)
