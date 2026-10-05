"""
Google ADK Callbacks Architecture for KAVACH.
Handles model, agent, and tool callbacks for customization, security auditing, and telemetry.
"""

from typing import Callable, Any, Dict, List, Optional
import time


class ToolCallback:
    """Tool invocation lifecycle callback."""
    def __init__(
        self,
        on_tool_start: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        on_tool_end: Optional[Callable[[str, Any, float], None]] = None,
        on_tool_error: Optional[Callable[[str, Exception], None]] = None,
    ):
        self.on_tool_start = on_tool_start
        self.on_tool_end = on_tool_end
        self.on_tool_error = on_tool_error


class ModelCallback:
    """LLM inference lifecycle callback."""
    def __init__(
        self,
        on_model_start: Optional[Callable[[str, Dict[str, Any]], None]] = None,
        on_model_end: Optional[Callable[[str, Any, float], None]] = None,
        on_model_error: Optional[Callable[[str, Exception], None]] = None,
    ):
        self.on_model_start = on_model_start
        self.on_model_end = on_model_end
        self.on_model_error = on_model_error


class AgentCallbacks:
    """Comprehensive Agent Lifecycle Callbacks Manager."""
    def __init__(self):
        self.tool_callbacks: List[ToolCallback] = []
        self.model_callbacks: List[ModelCallback] = []
        self.event_log: List[Dict[str, Any]] = []

    def register_tool_callback(self, cb: ToolCallback):
        self.tool_callbacks.append(cb)

    def register_model_callback(self, cb: ModelCallback):
        self.model_callbacks.append(cb)

    def trigger_tool_start(self, tool_name: str, args: Dict[str, Any]):
        self.event_log.append({"event": "tool_start", "tool": tool_name, "args": args, "timestamp": time.time()})
        for cb in self.tool_callbacks:
            if cb.on_tool_start:
                try:
                    cb.on_tool_start(tool_name, args)
                except Exception:
                    pass

    def trigger_tool_end(self, tool_name: str, result: Any, duration_ms: float):
        self.event_log.append({"event": "tool_end", "tool": tool_name, "duration_ms": duration_ms, "timestamp": time.time()})
        for cb in self.tool_callbacks:
            if cb.on_tool_end:
                try:
                    cb.on_tool_end(tool_name, result, duration_ms)
                except Exception:
                    pass

    def trigger_tool_error(self, tool_name: str, error: Exception):
        self.event_log.append({"event": "tool_error", "tool": tool_name, "error": str(error), "timestamp": time.time()})
        for cb in self.tool_callbacks:
            if cb.on_tool_error:
                try:
                    cb.on_tool_error(tool_name, error)
                except Exception:
                    pass

    def trigger_model_start(self, model_name: str, prompt_meta: Dict[str, Any]):
        self.event_log.append({"event": "model_start", "model": model_name, "meta": prompt_meta, "timestamp": time.time()})
        for cb in self.model_callbacks:
            if cb.on_model_start:
                try:
                    cb.on_model_start(model_name, prompt_meta)
                except Exception:
                    pass

    def trigger_model_end(self, model_name: str, response: Any, duration_ms: float):
        self.event_log.append({"event": "model_end", "model": model_name, "duration_ms": duration_ms, "timestamp": time.time()})
        for cb in self.model_callbacks:
            if cb.on_model_end:
                try:
                    cb.on_model_end(model_name, response, duration_ms)
                except Exception:
                    pass
