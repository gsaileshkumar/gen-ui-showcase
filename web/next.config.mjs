import { fileURLToPath } from "node:url";
import { dirname } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // Silence the multi-lockfile warning: the workspace root has its own
  // package.json (concurrently runner) and so does web/.
  turbopack: {
    root: __dirname,
  },
  env: {
    NEXT_PUBLIC_AGENT_URL:
      process.env.NEXT_PUBLIC_AGENT_URL ??
      "http://localhost:8123/agent/parcel_pilot",
  },
};

export default nextConfig;
