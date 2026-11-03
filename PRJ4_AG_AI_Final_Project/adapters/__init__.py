"""
KAVACH Multi-Model Adapter Factory.
"""

from typing import Optional
from adapters.base_adapter import BaseModelAdapter, ModelResponse
from adapters.gemini_adapter import GeminiAdapter
from adapters.ollama_adapter import OllamaAdapter
from adapters.deterministic_adapter import DeterministicAdapter


def get_adapter(provider: str = "deterministic", model_name: Optional[str] = None) -> BaseModelAdapter:
    """Return model adapter instance according to provider specification."""
    p_lower = provider.lower()
    if "gemini" in p_lower:
        return GeminiAdapter(model_name=model_name or "gemini-2.5-flash")
    elif "ollama" in p_lower or "deepseek" in p_lower or "llama" in p_lower:
        return OllamaAdapter(model_name=model_name or "deepseek-r1:1.5b")
    else:
        return DeterministicAdapter(model_name=model_name or "deterministic-rule-engine-v3")


__all__ = [
    "BaseModelAdapter",
    "ModelResponse",
    "GeminiAdapter",
    "OllamaAdapter",
    "DeterministicAdapter",
    "get_adapter",
]
