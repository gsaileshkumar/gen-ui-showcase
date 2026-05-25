"""Parcel Pilot agent — FastAPI host for the LangGraph agent.

Exposes the AG-UI endpoint at /copilotkit on port 8123 (CopilotKit's
canvas-with-langgraph-python convention). The Next.js runtime route at
/api/copilotkit on the web side proxies into here.
"""

from __future__ import annotations

import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from copilotkit import CopilotKitSDK, LangGraphAGUIAgent
from copilotkit.integrations.fastapi import add_fastapi_endpoint

from graph import build_graph

load_dotenv()

app = FastAPI(title="Parcel Pilot Agent", version="0.1.0")


@app.get("/healthz")
def healthz() -> dict[str, str]:
    return {
        "status": "ok",
        "dhl_mode": os.getenv("DHL_MODE", "mock"),
    }


sdk = CopilotKitSDK(
    agents=[
        LangGraphAGUIAgent(
            name="parcel_pilot",
            description=(
                "A DHL shipping assistant that can track shipments, quote rates, "
                "calculate duty & tax, find drop-off locations, and visualize "
                "shipment routes. Powers four Generative UI bands: Controlled, "
                "Declarative, MCP Apps, and Open-Ended."
            ),
            graph=build_graph(),
        ),
    ],
)

add_fastapi_endpoint(app, sdk, "/copilotkit")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8123")),
        reload=True,
    )
