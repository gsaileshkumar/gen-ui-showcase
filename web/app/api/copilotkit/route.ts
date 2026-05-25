import {
  CopilotRuntime,
  ExperimentalEmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { NextRequest } from "next/server";

/**
 * CopilotKit runtime route — the bridge between the React app and the
 * LangGraph agent.
 *
 * The LLM (GPT-4o) lives in the Python agent, so we use the Empty service
 * adapter here: this route just proxies AG-UI events to the FastAPI endpoint
 * at NEXT_PUBLIC_AGENT_URL (default http://localhost:8123/copilotkit).
 */

const runtime = new CopilotRuntime({
  remoteEndpoints: [
    {
      url:
        process.env.NEXT_PUBLIC_AGENT_URL ??
        "http://localhost:8123/copilotkit",
    },
  ],
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
