"""Parcel Pilot agent — FastAPI host for the LangGraph agent.

Exposes an AG-UI streaming endpoint at /agent/parcel_pilot on port 8123. The
Next.js runtime route (/api/copilotkit) connects to it with an AG-UI HttpAgent
and proxies events to the browser.

Why AG-UI directly (not copilotkit's add_fastapi_endpoint): in copilotkit
0.1.90 the LangGraph agent is an AG-UI agent (LangGraphAGUIAgent extends
ag_ui_langgraph.LangGraphAgent). The legacy CopilotKitRemoteEndpoint /info
discovery path is broken for it (its dict_repr calls a super().dict_repr that
doesn't exist), so we serve the agent over the AG-UI protocol and register it
on the JS runtime via the `agents` config instead of `remoteEndpoints`.
"""

from __future__ import annotations

import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from ag_ui_langgraph import add_langgraph_fastapi_endpoint
from copilotkit import LangGraphAGUIAgent

from graph import build_graph

load_dotenv()

AGENT_NAME = "parcel_pilot"
AGENT_PATH = f"/agent/{AGENT_NAME}"

app = FastAPI(title="Parcel Pilot Agent", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {
        "status": "ok",
        "dhl_mode": os.getenv("DHL_MODE", "mock"),
        "agent": AGENT_NAME,
        "agent_path": AGENT_PATH,
    }


agent = LangGraphAGUIAgent(
    name=AGENT_NAME,
    description=(
        "A DHL shipping assistant that can track shipments, quote rates, "
        "calculate duty & tax, find drop-off locations, and visualize "
        "shipment routes. Powers four Generative UI bands: Controlled, "
        "Declarative, MCP Apps, and Open-Ended."
    ),
    graph=build_graph(),
)

add_langgraph_fastapi_endpoint(app, agent, AGENT_PATH)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8123")),
        reload=True,
    )
