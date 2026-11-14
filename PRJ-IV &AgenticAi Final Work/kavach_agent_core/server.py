"""
KAVACH Real-Time Live Execution Cockpit & SSE Streaming API
Course: CSE3101 Agentic AI - Final Capstone Project
Authors: Dhruv Jain (230532), BML Munjal University
"""

import os
import sys
import json
import time
import queue
import threading
from typing import Dict, Any, Generator
from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from kavach_agent_core.tools import MCP_TOOL_SCHEMAS, TOOL_REGISTRY
from kavach_agent_core.llm_client import LLMClient
from kavach_agent_core.multi_agent_swarm import KavachMultiAgentSwarm, AGENT_ROSTER, SwarmExecutionResult

app = FastAPI(
    title="KAVACH Live Agentic AI Cockpit API",
    description="Real-Time Autonomous Multi-Agent Swarm Streaming Daemon (CSE3101 Agentic AI)",
    version="4.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

llm_client = LLMClient()
swarm_engine = KavachMultiAgentSwarm(llm_client=llm_client)


class GoalRequest(BaseModel):
    goal: str


@app.get("/api/status")
def get_status():
    """Return live system capabilities and LLM provider."""
    return {
        "status": "ONLINE",
        "active_provider": llm_client.get_active_provider_name(),
        "air_gapped_mode": llm_client.air_gapped_mode,
        "agents_count": len(AGENT_ROSTER),
        "tools_count": len(TOOL_REGISTRY),
    }


@app.get("/api/agents")
def get_agents():
    """Return details of all 5 specialized agents in the swarm."""
    return {name: persona.dict() for name, persona in AGENT_ROSTER.items()}


@app.get("/api/tools")
def get_tools():
    """Return all 11 MCP tool schemas."""
    return {"tools": MCP_TOOL_SCHEMAS}


@app.post("/api/swarm/execute")
def execute_swarm(req: GoalRequest):
    """Execute swarm synchronously and return complete execution result."""
    res: SwarmExecutionResult = swarm_engine.execute_swarm(goal=req.goal)
    return res.dict()


@app.get("/api/swarm/stream")
def stream_swarm_execution(goal: str = Query(..., description="User goal or task for the agent swarm")):
    """
    Server-Sent Events (SSE) streaming endpoint.
    Emits real-time agent thoughts, tool dispatches, observations, and A2A messages.
    """
    def event_generator() -> Generator[str, None, None]:
        event_q = queue.Queue()

        def on_event(ev: Dict[str, Any]):
            event_q.put({"type": "EVENT", "data": ev})

        def run_thread():
            try:
                res = swarm_engine.execute_swarm(goal=goal, on_event_callback=on_event)
                event_q.put({"type": "COMPLETE", "data": res.dict()})
            except Exception as e:
                event_q.put({"type": "ERROR", "data": {"error": str(e)}})
            finally:
                event_q.put(None)  # Sentinel to end stream

        t = threading.Thread(target=run_thread, daemon=True)
        t.start()

        # Stream events to client
        while True:
            item = event_q.get()
            if item is None:
                break
            msg_type = item["type"]
            data_json = json.dumps(item["data"])
            yield f"event: {msg_type}\ndata: {data_json}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


# =========================================================================
# LIVE COCKPIT WEB UI
# =========================================================================

COCKPIT_HTML_PATH = os.path.join(os.path.dirname(__file__), "cockpit.html")

@app.get("/", response_class=HTMLResponse)
@app.get("/cockpit", response_class=HTMLResponse)
def serve_cockpit():
    if os.path.exists(COCKPIT_HTML_PATH):
        with open(COCKPIT_HTML_PATH, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>KAVACH Live Agent Cockpit</h1><p>UI loading...</p>"


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "8005"))
    print(f"Starting KAVACH Real-Time Agent Cockpit on http://localhost:{port}/")
    uvicorn.run("kavach_agent_core.server:app", host="127.0.0.1", port=port, reload=False)
