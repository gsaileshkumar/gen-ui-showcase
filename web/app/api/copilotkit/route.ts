import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { HttpAgent } from "@ag-ui/client";
import { NextRequest } from "next/server";

/**
 * CopilotKit runtime route — the bridge between the React app and the
 * LangGraph agent.
 *
 * The LLM (GPT-4o) lives in the Python agent, which speaks the AG-UI protocol.
 * We register it on the runtime by name via the `agents` config (not
 * `remoteEndpoints`): the key must match `agent="parcel_pilot"` on the
 * <CopilotKit> provider and the agent name in agent/main.py. The Empty service
 * adapter is fine here because all chat is handled by the agent.
 */

const AGENT_URL =
  process.env.NEXT_PUBLIC_AGENT_URL ??
  "http://localhost:8123/agent/parcel_pilot";

const runtime = new CopilotRuntime({
  agents: {
    parcel_pilot: new HttpAgent({ url: AGENT_URL }),
  },
});

const serviceAdapter = new ExperimentalEmptyAdapter();

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });
  return handleRequest(req);
};
