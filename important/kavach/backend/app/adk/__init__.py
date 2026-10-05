"""
Google ADK (Agent Development Kit) implementation for KAVACH.
Complies with CSE3101 Agentic AI Module 4 (20 Sessions):
- Agent (LlmAgent) class, lifecycle, and capabilities
- Tool context, built-in tools, and custom tool development
- State, sessions, and memory (transient vs persistent)
- Coordinator agents, sub-agents, task delegation
- Multi-agent workflows (graph, dynamic, collaborative, template)
- Callbacks: model, agent, and tool callbacks
"""

from .agent import LlmAgent, AgentLifecycleState
from .coordinator import CoordinatorAgent
from .callbacks import AgentCallbacks, ToolCallback, ModelCallback
from .memory import AgentMemory, TransientMemory, PersistentSessionMemory
from .workflow import AgentWorkflowGraph, WorkflowExecutionMode

__all__ = [
    "LlmAgent",
    "AgentLifecycleState",
    "CoordinatorAgent",
    "AgentCallbacks",
    "ToolCallback",
    "ModelCallback",
    "AgentMemory",
    "TransientMemory",
    "PersistentSessionMemory",
    "AgentWorkflowGraph",
    "WorkflowExecutionMode",
]
