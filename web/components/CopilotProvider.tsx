"use client";

import { CopilotKit } from "@copilotkit/react-core";
import "@copilotkit/react-ui/styles.css";

/**
 * Wraps the app in the CopilotKit runtime client. The runtime URL points at
 * the Next.js route /api/copilotkit, which in turn proxies to the LangGraph
 * agent on :8123. The agent name must match the one registered in
 * agent/main.py.
 */
export function CopilotProvider({ children }: { children: React.ReactNode }) {
  return (
    <CopilotKit runtimeUrl="/api/copilotkit" agent="parcel_pilot">
      {children}
    </CopilotKit>
  );
}
