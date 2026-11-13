"""
KAVACH Multi-Model Adapter Subsystem - Base Model Specification.
Provides vendor-agnostic abstraction for cloud LLMs, local edge models, and offline deterministic engines.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from pydantic import BaseModel


class ModelResponse(BaseModel):
    provider: str
    model_name: str
    content: str
    latency_ms: float
    token_usage: Dict[str, int]
    raw_metadata: Dict[str, Any] = {}


class BaseModelAdapter(ABC):
    """Abstract base class that all KAVACH model adapters must implement."""

    def __init__(self, model_name: str, temperature: float = 0.2):
        self.model_name = model_name
        self.temperature = temperature

    @abstractmethod
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any) -> ModelResponse:
        """Generate response given a user prompt and optional system guardrail prompt."""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Check whether the model endpoint or API key is accessible."""
        pass

    @abstractmethod
    def get_capabilities(self) -> Dict[str, Any]:
        """Return context window size, streaming support, and license details."""
        pass

