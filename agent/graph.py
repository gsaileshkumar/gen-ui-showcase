"""LangGraph state graph for Parcel Pilot.

GPT-4o + 5 DHL tools. Standard agentic loop: model decides whether to call a
tool; tool result is fed back; loop ends when the model emits a final message
with no tool calls.
"""

from __future__ import annotations

from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import END, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode

from tools import ALL_TOOLS

SYSTEM_PROMPT = """You are Parcel Pilot, a DHL shipping assistant for a live
conference demo.

You have five tools (all DHL Developer Portal APIs, served from mock fixtures
by default):
  - track_shipment(tracking_number)
  - get_rates(origin, destination, weight_kg, dimensions_cm)
  - calc_duty(origin, destination, declared_value, currency)
  - find_locations(country, postal_code, radius_km)
  - visualize_route(tracking_number)

Use tools whenever the user asks about a shipment, price, duty, drop-off
location, or route visualization. Prefer one tool call per turn, then answer
concisely. Keep replies short — the UI does the heavy lifting.
"""


def build_graph():
    """Return a compiled LangGraph ready to be wrapped by LangGraphAgent."""

    model = ChatOpenAI(model="gpt-4o", temperature=0).bind_tools(ALL_TOOLS)
    tool_node = ToolNode(ALL_TOOLS)

    def call_model(state: MessagesState) -> dict:
        messages = [SystemMessage(content=SYSTEM_PROMPT), *state["messages"]]
        return {"messages": [model.invoke(messages)]}

    def should_continue(state: MessagesState) -> str:
        last = state["messages"][-1]
        return "tools" if getattr(last, "tool_calls", None) else END

    graph = StateGraph(MessagesState)
    graph.add_node("agent", call_model)
    graph.add_node("tools", tool_node)
    graph.set_entry_point("agent")
    graph.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
    graph.add_edge("tools", "agent")

    return graph.compile()
