# CLAUDE.md — Parcel Pilot

> Context for Claude Code. Read this first, then `docs/BUILD_PLAN.md`.

## What we’re building

**Parcel Pilot** — a live demo app for a conference talk on **Generative UI**, for a
**mixed product + engineering audience**. It walks through CopilotKit’s four
Generative UI bands, each powered by real **DHL Developer Portal** API schemas:

1. **Controlled** — agent picks from pre-built components (`useCopilotAction` / render).
1. **Declarative (A2UI)** — agent assembles a catalog of building blocks at runtime.
1. **MCP Apps** — a sandboxed 3rd-party iframe surface embedded in the app.
1. **Open-Ended** — agent generates raw HTML/SVG, rendered in a sandbox.

Presented as **tabs** (jump to any band freely), with a persistent
**Developer ◄────► Agent** “spectrum bar” showing where the active band sits.

## Locked decisions (do not re-litigate)

- **LLM:** OpenAI **GPT-4o**.
- **Agent backend:** **real LangGraph (Python)** + FastAPI, via the `copilotkit` Python SDK.
- **Frontend:** **Next.js App Router** + CopilotKit React SDK.
- **DHL data:** **hybrid** — mock-first (default, offline-safe), real-capable via `DHL_MODE=live`.
- **MCP Apps + Open-Ended bands:** default to **canned-but-real** responses with a **Live toggle** (these bands are experimental; protect the live demo).
- **Theme:** **DHL red/yellow** (`#D40511` / `#FFCC00` on white). Mark clearly as an
  educational demo — NOT affiliated with or endorsed by DHL.
- **Secrets:** `.env.example` only. Never commit real keys. Never print keys to stdout.

## Architecture

```
Browser (Next.js + CopilotKit React)  :3000
   │  AG-UI events (bi-directional)
/api/copilotkit  (CopilotKit runtime route)
   │
LangGraph Python agent (FastAPI)       :8123   ← note: 8123, CopilotKit convention
   │  tools call DHL client → mock/ OR live (DHL_MODE)
```

Run BOTH with one command (`pnpm dev` via Turborepo, or root `concurrently`).

## Tooling versions to verify at build time

These APIs are young and change between releases. **Check current docs before coding** —
do not trust these pins blindly:

- Frontend: `@copilotkit/react-core`, `@copilotkit/react-ui`, `@copilotkit/runtime`
  (was ~v1.51.x in early 2026; check latest).
- Python: `copilotkit` (was 0.1.90, May 2026), `langgraph`, `langchain-openai`, `fastapi`, `uvicorn`.
- A2UI is a new spec (Google + CopilotKit launch partner). Confirm the current catalog
  API and whether it’s `a2ui={{ catalog }}` on `<CopilotKit>` or a separate hook.
- Reference starters to mirror:
  - github.com/CopilotKit/CopilotKit → `examples/integrations/langgraph-python`
  - github.com/CopilotKit/canvas-with-langgraph-python (agent on :8123, GPT-4o)
- Generative UI Spectrum reference: copilotkit.ai/generative-ui-spectrum

## DHL APIs (developer.dhl.com) used per band

- Controlled → **Shipment Tracking – Unified** (tracking timeline)
- Declarative → **MyDHL rates** + **Duty & Tax Calculator** + **Location Finder – Unified**
- MCP Apps → **Location Finder – Unified** (map picker applet)
- Open-Ended → **Shipment Tracking – Unified** route data (animated SVG journey)

Author mock JSON fixtures to match the REAL response schemas from the API reference, so
flipping `DHL_MODE=mock→live` changes nothing in the UI.

## Build order

1. Scaffold monorepo (web + agent), DHL theme, tab shell, static SpectrumBar.
1. Python LangGraph agent: GPT-4o, mock DHL client, 5 tools, FastAPI on :8123.
1. Wire `/api/copilotkit` runtime ↔ LangGraph (AG-UI). Prove with a hello round-trip.
1. **Controlled** band end-to-end (TrackingTimeline). ← first vertical slice; stop & verify.
1. **Declarative** band + A2UI catalog (Card/Button/Stat/List/PriceTable).
1. **MCP Apps** band with a LOCAL stub MCP server (offline-safe).
1. **Open-Ended** band: recorded response + Live toggle + sandboxed iframe.
1. Live-mode DHL client (`live.py`) + `.env` wiring. Only the endpoints we demo.
1. README runbook + `docs/DEMO_SCRIPT.md`. Rehearse in mock mode.

## Conventions

- TypeScript strict on the frontend. Type the catalog + tool params with Zod.
- Keep each band’s code in its own folder so it reads cleanly on a projector.
- Prefer clarity over cleverness — this code will be shown to an audience.
- Every band component should work with mock data with zero network.
- Add a footer disclaimer on every page (educational demo / not official DHL).

## Definition of done for the demo

- `pnpm dev` starts both processes; all four tabs load with mock data, no keys needed
  beyond `OPENAI_API_KEY`.
- Controlled + Declarative are fully live (agent genuinely chooses/assembles UI).
- MCP Apps + Open-Ended work from canned data, with a working Live toggle.
- A rehearsal-ready `docs/DEMO_SCRIPT.md` exists.