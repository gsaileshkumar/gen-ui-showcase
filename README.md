# Parcel Pilot

A live conference demo of [**CopilotKit**](https://copilotkit.ai)'s four
Generative UI bands — **Controlled → Declarative (A2UI) → MCP Apps →
Open-Ended** — built around real DHL Developer Portal API schemas.

> Educational demo. Not affiliated with or endorsed by DHL.

## What's in the box (today)

This commit is **build steps 1 & 2** of the plan (`docs/BUILD_PLAN.md`):

- **Step 1 — scaffold.** Monorepo with `web/` (Next.js 16 + CopilotKit React)
  and `agent/` (FastAPI + LangGraph Python), DHL red/yellow theme, four-tab
  shell with a static Developer ◄──► Agent SpectrumBar, `.env.example`, and
  one-command dev script.
- **Step 2 — agent.** GPT-4o LangGraph agent on `:8123`, mock DHL client with
  fixtures matching the real Developer Portal schemas, and 5 tool stubs
  (`track_shipment`, `get_rates`, `calc_duty`, `find_locations`,
  `visualize_route`).

The four bands are scaffolded as placeholder tabs — they describe what the
band will do but don't run interactions yet. Those come in steps 4-7.

## Quickstart

```bash
# one-time setup
cp .env.example .env                              # add OPENAI_API_KEY
npm install                                       # root (just `concurrently`)
npm --prefix web install                          # Next.js app
pip install -r agent/requirements.txt             # LangGraph agent

# run both processes on one command
npm run dev
```

That starts:

- **web**   — Next.js on <http://localhost:3000>
- **agent** — FastAPI/LangGraph on <http://localhost:8123>

Hit <http://localhost:3000> and click through the four tabs. The SpectrumBar
should slide as you switch tabs.

## What to verify

1. **Health check** — `curl http://localhost:8123/healthz` returns
   `{"status":"ok","dhl_mode":"mock"}`.
2. **Agent endpoint exists** — `curl http://localhost:8123/agent/parcel_pilot/health`
   returns `{"status":"ok","agent":{"name":"parcel_pilot"}}` — proves the AG-UI
   endpoint is up.
3. **Runtime sees the agent** — with both servers up,
   `curl -s -X POST http://localhost:3000/api/copilotkit -H "Content-Type: application/json" -d '{"method":"info","params":{},"body":{}}'`
   returns JSON whose `agents` map contains `parcel_pilot`. (This is what the
   browser client checks during runtime sync — if it's missing you get
   "agent parcel_pilot not found / No agents registered".)
4. **Web app loads** — `http://localhost:3000` shows the yellow DHL hero band,
   the four tabs (Controlled / Declarative / MCP Apps / Open-Ended), and the
   SpectrumBar slides between positions as you click them.
5. **Footer disclaimer is present** on every tab.
6. **No keys in repo** — `git grep` for `sk-` and your real DHL key turns up
   nothing. Only `.env.example` is committed.

The end-to-end chat round-trip is **not** wired yet — that's step 3 of the
build plan (Controlled band vertical slice). The runtime is wired
(`web/app/api/copilotkit/route.ts` registers the agent at
`:8123/agent/parcel_pilot` via the `agents` config) but no chat UI is mounted
on any tab yet.

## Tech stack

| Layer      | What                                                      |
| ---------- | --------------------------------------------------------- |
| Frontend   | Next.js 16 (App Router) + React 19 + Tailwind             |
| Copilot    | `@copilotkit/react-core` / `react-ui` / `runtime` 1.57.x  |
| LLM        | OpenAI **GPT-4o** (called from the Python agent)          |
| Backend    | FastAPI + LangGraph 1.0.x via `copilotkit==0.1.90`        |
| DHL data   | Mock fixtures matching real schemas; flip with `DHL_MODE` |

## Project layout

```
.
├── package.json          # root scripts (concurrently runs web + agent)
├── .env.example
├── agent/                # Python LangGraph agent (FastAPI on :8123)
│   ├── main.py           # FastAPI app + AG-UI endpoint at /agent/parcel_pilot
│   ├── graph.py          # GPT-4o + ToolNode agentic loop
│   ├── tools.py          # 5 DHL tools
│   ├── dhl/
│   │   ├── client.py     # picks mock vs live by DHL_MODE
│   │   ├── live.py       # real DHL calls (stubbed, build step 8)
│   │   └── mock/*.json   # fixtures matching real schemas
│   └── requirements.txt
├── web/                  # Next.js 16 frontend
│   ├── app/
│   │   ├── layout.tsx              # CopilotProvider + Footer
│   │   ├── page.tsx                # TabShell
│   │   └── api/copilotkit/route.ts # CopilotRuntime → agent via `agents` config
│   └── components/
│       ├── bands.ts                # band metadata (single source)
│       ├── TabShell.tsx
│       ├── SpectrumBar.tsx
│       ├── Footer.tsx
│       └── bands/{Controlled,Declarative,McpApps,OpenEnded}Tab.tsx
└── docs/
    └── BUILD_PLAN.md
```

## DHL mode

`DHL_MODE=mock` (default) is offline-safe: every tool returns a fixture from
`agent/dhl/mock/*.json` shaped like the real DHL Developer Portal response.

`DHL_MODE=live` requires `DHL_API_KEY`. The live client (`agent/dhl/live.py`)
is intentionally stubbed today and will raise `NotImplementedError` — it's
wired in build step 8 once we know exactly which endpoints we're demoing on
stage.

**Rehearse in mock.** Only switch to live once you have keys and a stable
network at the venue.

## Next up

Build order (see `docs/BUILD_PLAN.md` §11):

3. Wire `/api/copilotkit` ↔ LangGraph with a hello round-trip
4. **Controlled** band end-to-end (TrackingTimeline) ← first vertical slice
5. **Declarative** band + A2UI catalog
6. **MCP Apps** with a local stub MCP server
7. **Open-Ended** with recorded response + Live toggle
8. Live-mode DHL client + `.env` wiring
9. `docs/DEMO_SCRIPT.md` + rehearsal
