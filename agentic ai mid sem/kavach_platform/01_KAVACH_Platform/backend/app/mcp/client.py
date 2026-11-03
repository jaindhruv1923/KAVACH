"""
Model Context Protocol (MCP) Client for KAVACH Agentic AI Platform.

Complies with standard MCP JSON-RPC 2.0 specifications (Protocol 2024-11-05).
Enables the KAVACH ReAct Agent and orchestrator to:
1. Initialize protocol handshakes with MCP servers.
2. Query dynamic tool lists (`tools/list`).
3. Call remote/local MCP tools (`tools/call`) with strict schema validation.
4. Bridge discovered MCP tools into KAVACH's registered agent toolset.
"""

import json
import uuid
import time
from typing import Dict, Any, List, Optional, Callable
from urllib import request as urllib_request
from urllib.error import URLError, HTTPError

from app.mcp.server import handle_mcp_request, MCP_PROTOCOL_VERSION


class MCPClientError(Exception):
    """Raised when an MCP protocol, network, or server error occurs."""
    pass


class MCPClient:
    """
    Standard Model Context Protocol (MCP) Client.
    Supports in-process direct dispatch (zero network latency, offline safe)
    or standard JSON-RPC HTTP transport.
    """

    def __init__(
        self,
        server_url: Optional[str] = None,
        timeout_seconds: float = 10.0,
        client_name: str = "kavach-agentic-client",
        client_version: str = "2.1.0"
    ):
        self.server_url = server_url
        self.timeout_seconds = timeout_seconds
        self.client_name = client_name
        self.client_version = client_version
        self.is_initialized = False
        self.server_protocol_version: Optional[str] = None
        self.server_info: Dict[str, Any] = {}
        self.cached_tools: List[Dict[str, Any]] = []

    def _send_rpc(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Dispatch a JSON-RPC 2.0 request either in-process or over HTTP."""
        req_id = str(uuid.uuid4())
        payload = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params or {}
        }

        # In-process transport (Direct and deterministic)
        if not self.server_url:
            response = handle_mcp_request(payload)
            if "error" in response:
                err = response["error"]
                raise MCPClientError(f"MCP Server Error [{err.get('code', -1)}]: {err.get('message', 'Unknown')}")
            return response.get("result", {})

        # HTTP JSON-RPC 2.0 Transport
        try:
            data_bytes = json.dumps(payload).encode("utf-8")
            req = urllib_request.Request(
                self.server_url,
                data=data_bytes,
                headers={"Content-Type": "application/json", "User-Agent": f"{self.client_name}/{self.client_version}"},
                method="POST"
            )
            with urllib_request.urlopen(req, timeout=self.timeout_seconds) as resp:
                resp_bytes = resp.read()
                resp_json = json.loads(resp_bytes.decode("utf-8"))
                if "error" in resp_json:
                    err = resp_json["error"]
                    raise MCPClientError(f"Remote MCP Error [{err.get('code', -1)}]: {err.get('message')}")
                return resp_json.get("result", {})
        except (URLError, HTTPError) as e:
            raise MCPClientError(f"HTTP transport failed to {self.server_url}: {e}")
        except Exception as e:
            raise MCPClientError(f"MCP client dispatch error: {e}")

    def initialize(self) -> Dict[str, Any]:
        """Send initialize request to establish protocol handshake."""
        params = {
            "protocolVersion": MCP_PROTOCOL_VERSION,
            "capabilities": {
                "roots": {"listChanged": False},
                "sampling": {}
            },
            "clientInfo": {
                "name": self.client_name,
                "version": self.client_version
            }
        }
        res = self._send_rpc("initialize", params)
        self.server_protocol_version = res.get("protocolVersion")
        self.server_info = res.get("serverInfo", {})
        self.is_initialized = True
        return res

    def list_tools(self) -> List[Dict[str, Any]]:
        """Query available tools advertised by the MCP server."""
        if not self.is_initialized:
            self.initialize()

        res = self._send_rpc("tools/list", {})
        tools = res.get("tools", [])
        self.cached_tools = tools
        return tools

    def call_tool(self, tool_name: str, arguments: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a tool via MCP JSON-RPC protocol."""
        if not self.is_initialized:
            self.initialize()

        params = {
            "name": tool_name,
            "arguments": arguments or {}
        }
        res = self._send_rpc("tools/call", params)
        return res

    def bridge_tools_to_agent_registry(
        self,
        target_registry: Dict[str, Callable],
        target_schemas: List[Dict[str, Any]],
        prefix: str = "mcp_"
    ) -> int:
        """
        Dynamically register discovered MCP tools into KAVACH's ReAct agent tool registry.
        Returns count of bridged tools.
        """
        tools = self.list_tools()
        bridged_count = 0

        for tool_meta in tools:
            name = tool_meta.get("name", "")
            description = tool_meta.get("description", "")
            input_schema = tool_meta.get("inputSchema", {})

            # Avoid collision or duplicate registration
            reg_name = name if name.startswith(prefix) else f"{prefix}{name}"

            # Factory function closure to capture tool name
            def make_invoker(t_name: str):
                def invoker(**kwargs) -> Dict[str, Any]:
                    try:
                        res = self.call_tool(t_name, kwargs)
                        return {
                            "success": True,
                            "mcp_tool": t_name,
                            "content": res.get("content", []),
                            "details": res.get("details") or res.get("calculation") or res.get("ast_details") or res
                        }
                    except Exception as err:
                        return {
                            "success": False,
                            "mcp_tool": t_name,
                            "error": str(err)
                        }
                return invoker

            target_registry[reg_name] = make_invoker(name)

            # Convert to agent tool schema
            target_schemas.append({
                "name": reg_name,
                "description": f"[MCP Protocol] {description}",
                "parameters": input_schema,
            })
            bridged_count += 1

        return bridged_count


# Global default in-process MCP client singleton
global_mcp_client = MCPClient()
