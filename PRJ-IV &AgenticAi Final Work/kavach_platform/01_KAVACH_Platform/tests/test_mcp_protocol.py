"""
Test Suite for Model Context Protocol (MCP) and Agent-to-Agent (A2A) Protocols (Module 6 & Phase 7).
Tests JSON-RPC 2.0 handshake, dynamic tool discovery, execution, error codes, and A2A integrity envelopes.
"""

import pytest
from app.mcp.client import MCPClient, MCPClientError
from app.mcp.server import handle_mcp_request, MCP_PROTOCOL_VERSION
from app.agent.tools import TOOLS_REGISTRY, enable_mcp_tools
from app.a2a.protocol import A2AMessage, A2AMessageType, A2ABus


def test_mcp_client_initialize_handshake():
    client = MCPClient()
    res = client.initialize()

    assert res["protocolVersion"] == MCP_PROTOCOL_VERSION
    assert "tools" in res["capabilities"]
    assert client.is_initialized is True
    assert client.server_info["name"] == "kavach-security-mcp"


def test_mcp_client_list_tools():
    client = MCPClient()
    tools = client.list_tools()

    assert len(tools) >= 5
    tool_names = [t["name"] for t in tools]
    assert "kavach_scan_security" in tool_names
    assert "mcp_calculator" in tool_names
    assert "mcp_file_parser" in tool_names


def test_mcp_client_call_calculator():
    client = MCPClient()
    # Test Shannon Entropy calculation via MCP
    res = client.call_tool(
        "mcp_calculator",
        {"operation": "entropy", "params": {"text": "A" * 100}}
    )
    assert "calculation" in res
    calc = res["calculation"]
    assert calc["operation"] == "shannon_entropy"
    assert calc["entropy_value"] == 0.0  # Zero entropy for identical characters


def test_mcp_client_call_file_parser():
    client = MCPClient()
    code = "import math\ndef compute_risk(val):\n    return val * 2\n"
    res = client.call_tool(
        "mcp_file_parser",
        {"source_code": code, "filename": "sample.py"}
    )
    ast_details = res["ast_details"]
    assert ast_details["syntax_valid"] is True
    assert "compute_risk" in ast_details["functions"]
    assert "math" in ast_details["imports"]


def test_mcp_unknown_tool_error():
    client = MCPClient()
    with pytest.raises(MCPClientError) as exc_info:
        client.call_tool("nonexistent_phantom_tool", {})
    assert "not found" in str(exc_info.value).lower() or "-32601" in str(exc_info.value)


def test_bridge_mcp_tools_into_agent_registry():
    count = enable_mcp_tools()
    assert count >= 5
    assert "mcp_calculator" in TOOLS_REGISTRY or "mcp_mcp_calculator" in TOOLS_REGISTRY

    # Call bridged tool through standard agent tool interface
    key = "mcp_calculator" if "mcp_calculator" in TOOLS_REGISTRY else "mcp_mcp_calculator"
    invoker = TOOLS_REGISTRY[key]
    out = invoker(operation="entropy", params={"text": "random_unpredictable_key_12345!@#$%"})
    assert out["success"] is True


def test_a2a_protocol_envelope_and_signature():
    msg = A2AMessage(
        sender_agent_id="adk_planner",
        receiver_agent_id="crew_security_auditor",
        message_type=A2AMessageType.TASK_DELEGATION,
        payload={"task": "inspect_code", "target": "main.py"}
    )
    assert msg.signature is not None
    assert len(msg.signature) == 64  # SHA-256 hex string

    serialized = msg.to_dict()
    assert serialized["sender_agent_id"] == "adk_planner"
    assert serialized["message_type"] == "TASK_DELEGATION"

    deserialized = A2AMessage.from_dict(serialized)
    assert deserialized.message_id == msg.message_id
    assert deserialized.signature == msg.signature
