# DHL × Generative UI — Demo App Build Plan

**Working title:** *Parcel Pilot — A Tour of the Generative UI Spectrum*
**Purpose:** A live demo for a mixed product + engineering audience that walks through CopilotKit’s four Generative UI bands (Controlled → Declarative → MCP Apps → Open-Ended), each powered by real DHL Developer Portal APIs.

-----

## 1. Decisions locked in

|Area        |Decision                                                                              |Why                                                                 |
|------------|--------------------------------------------------------------------------------------|--------------------------------------------------------------------|
|DHL data    |**Hybrid** — mock-first, real-capable via env flag                                    |Demo never fails on stage; code stays honest                        |
|Agent layer |**Real CopilotKit + AG-UI + LangGraph (Python)**                                      |Faithful to CopilotKit’s canonical stack; eng audience will trust it|
|LLM         |**OpenAI GPT-4o**                                                                     |Single provider, strong tool-calling                                |
|Backend     |**Real LangGraph Python agent**                                                       |Most faithful; the agent genuinely chooses the UI                   |
|Frontend    |**Next.js (App Router) + CopilotKit React SDK**                                       |Standard CopilotKit setup                                           |
|Presentation|**Tabbed** — one tab per band, jump freely                                            |Survives unpredictable live Q&A                                     |
|Theme       |**DHL red/yellow brand look**                                                         |Instantly legible as “shipping”; marked as a demo, not official     |
|Secrets     |`.env.example` only; real keys never committed                                        |No keys on screen or in repo                                        |
|Risky bands |MCP Apps + Open-Ended default to **canned-but-real** responses, with a **Live toggle**|These bands are experimental; protects the live demo                |

-----

## 2. The narrative spine (what the audience learns)

The whole app is one product — a DHL shipping assistant — shown four ways. The same class of problem slides along the spectrum from **full developer control** to **full agent autonomy**:

1. **Controlled** — agent picks from your pre-built components. Pixel-perfect, brand-safe. *Workhorse.*
1. **Declarative (A2UI)** — you ship a catalog of building blocks; the agent assembles them at runtime. *The long tail.*
1. **MCP Apps** — inject a 3rd-party sandboxed iframe surface into your app. *Composability.*
1. **Open-Ended** — agent generates raw HTML/SVG on the fly. *The frontier.*

Each tab shows: the live interaction, the DHL API behind it, and a “who controls the pixels?” indicator (Developer ◄────► Agent) so the spectrum is visible at all times.

-----

## 3. DHL APIs used (per band)

All from developer.dhl.com. Mock responses are hand-built to match real schemas so a live switch is seamless.

|Band       |DHL API                                                                      |Demo interaction                                                                                                   |
|-----------|-----------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
|Controlled |**Shipment Tracking – Unified**                                              |“Where’s my parcel 00340…?” → pixel-perfect tracking timeline component                                            |
|Declarative|**MyDHL (rates)** + **Duty & Tax Calculator** + **Location Finder – Unified**|“Ship 5kg Berlin→Austin, options?” → agent assembles comparison cards, cost breakdown, drop-off list from a catalog|
|MCP Apps   |**Location Finder – Unified**                                                |Embedded map “applet” (sandboxed) to pick a pickup point; selection flows back to the agent                        |
|Open-Ended |**Shipment Tracking – Unified** (route data)                                 |“Visualize this parcel’s journey” → agent generates a bespoke animated SVG map                                     |


> Note: Real DHL APIs need a business account + API key/OAuth. The hybrid layer means you only need those for “real mode”; mock mode runs offline.

-----

## 4. Architecture

```
┌─────────────────────────────────────────────────────────┐
│  Browser (mixed audience sees this)                      │
│  Next.js App Router + CopilotKit React SDK               │
│  ┌───────────┬────────────┬───────────┬───────────────┐ │
│  │Controlled │ Declarative│ MCP Apps  │  Open-Ended   │ │  ← tabs
│  └───────────┴────────────┴───────────┴───────────────┘ │
│  - useComponent() (Controlled)                           │
│  - a2ui catalog   (Declarative)                          │
│  - MCPApps iframe (MCP)                                  │
│  - openGenerativeUI sandbox (Open)                       │
└───────────────┬─────────────────────────────────────────┘
                │ AG-UI events (bi-directional)
┌───────────────▼─────────────────────────────────────────┐
│  Next.js API route  /api/copilotkit  (CopilotKit runtime)│
└───────────────┬─────────────────────────────────────────┘
                │ AG-UI ↔ LangGraph
┌───────────────▼─────────────────────────────────────────┐
│  Python LangGraph agent (FastAPI)                        │
│  - GPT-4o, tool-calling                                  │
│  - tools: track_shipment, get_rates, calc_duty,          │
│           find_locations, visualize_route                │
│  - DHL client layer ──► mock/  OR  live (env flag)       │
└──────────────────────────────────────────────────────────┘
```

Two processes, started by one command (`make dev` via `concurrently`):

- **web** — Next.js on :3000
- **agent** — FastAPI/LangGraph on :8123

-----

## 5. Repo structure

```
parcel-pilot/
├── README.md                  # setup + on-stage runbook
├── Makefile                   # `make dev`, `make mock`, `make live`
├── .env.example               # OPENAI_API_KEY=, DHL_API_KEY=, DHL_MODE=mock
├── package.json               # root scripts (concurrently)
│
├── web/                       # Next.js frontend
│   ├── app/
│   │   ├── layout.tsx         # CopilotKit provider, DHL theme
│   │   ├── page.tsx           # tab shell + spectrum indicator
│   │   └── api/copilotkit/route.ts   # CopilotKit runtime endpoint
│   ├── components/
│   │   ├── bands/
│   │   │   ├── ControlledTab.tsx
│   │   │   ├── DeclarativeTab.tsx
│   │   │   ├── McpAppsTab.tsx
│   │   │   └── OpenEndedTab.tsx
│   │   ├── controlled/
│   │   │   ├── TrackingTimeline.tsx   # registered via useComponent
│   │   │   ├── ParcelCard.tsx
│   │   │   └── EtaBadge.tsx
│   │   ├── catalog/                   # A2UI building blocks (Declarative)
│   │   │   ├── Card.tsx  Button.tsx  Stat.tsx  List.tsx  PriceTable.tsx
│   │   │   └── catalog.ts             # definitions + renderers
│   │   ├── mcp/MapApplet.tsx          # sandboxed location picker
│   │   ├── open/SandboxFrame.tsx      # renders agent HTML/SVG safely
│   │   ├── SpectrumBar.tsx            # Developer ◄──► Agent indicator
│   │   └── theme/                     # DHL red/yellow tokens
│   └── lib/agui.ts
│
├── agent/                     # Python LangGraph agent
│   ├── main.py                # FastAPI app, AG-UI endpoint
│   ├── graph.py               # LangGraph state graph, GPT-4o
│   ├── tools.py               # the 5 tools (call DHL client)
│   ├── dhl/
│   │   ├── client.py          # picks mock vs live by DHL_MODE
│   │   ├── live.py            # real developer.dhl.com calls
│   │   └── mock/              # JSON fixtures matching real schemas
│   │       ├── tracking.json  rates.json  duty.json  locations.json
│   └── requirements.txt
│
└── docs/
    ├── DEMO_SCRIPT.md         # what to say/click per tab
    └── SPECTRUM.md            # one-pager of the 4 bands
```

-----

## 6. How each band is implemented (the real mechanics)

### Controlled — `useComponent`

- Register `TrackingTimeline`, `ParcelCard`, `EtaBadge` with the agent (name, description, Zod params, render fn).
- Agent calls `track_shipment` tool → returns data → chooses `TrackingTimeline` → CopilotKit renders YOUR component with that data.
- **Talking point:** “The agent chose *which* component and filled the data. I guaranteed *how it looks*. Pixel-perfect every time.”

### Declarative — A2UI catalog

- Define `catalogDefinitions` (Card, Button, Stat, List, PriceTable) + `catalogRenderers` mapping each to a DHL-styled React component.
- Pass `a2ui={{ catalog }}` to `<CopilotKit>`.
- Agent calls rates + duty + locations tools, then emits an **A2UI tree** assembling those primitives. Different queries → different layouts.
- **Talking point:** “I shipped the lego bricks. The agent built the layout. This is where the long tail lives.”

### MCP Apps — embedded applet

- `MCPApps={["location-picker.mcp…"]}` (or a local stub MCP server for offline).
- Renders a sandboxed iframe map; user picks a drop-off point; selection posts back through AG-UI to the agent.
- **Default:** local stub server (offline-safe). **Live toggle:** real MCP endpoint.
- **Talking point:** “A 3rd-party surface, injected into my app, talking to my agent.”

### Open-Ended — sandboxed generative HTML/SVG

- `openGenerativeUI={true}`; agent returns full SVG/HTML; rendered in a sandboxed iframe.
- **Default:** canned-but-real recorded response (so it’s instant + reliable). **Live toggle:** generate on the fly.
- **Talking point:** “Maximum freedom. Slower, less predictable, more expensive — the experimental frontier. Watch what happens when I flip to live…”

-----

## 7. The hybrid DHL data layer

`agent/dhl/client.py` reads `DHL_MODE`:

- `mock` (default) → returns fixtures from `dhl/mock/*.json`, with a small artificial delay so streaming looks real.
- `live` → calls real endpoints with `DHL_API_KEY` / OAuth.

Fixtures are authored from the real API reference schemas (Tracking Unified, MyDHL rates, Duty & Tax, Location Finder) so the shape is identical — switching modes changes nothing in the UI.

-----

## 8. Theme

- DHL palette: red `#D40511`, yellow `#FFCC00`, on white; bold sans (Inter/Delivery-like).
- Persistent footer disclaimer: *“Educational demo. Not affiliated with or endorsed by DHL. Uses publicly documented DHL Developer Portal API schemas.”*
- `SpectrumBar` always visible: a Developer ◄────► Agent slider that highlights the active tab’s position.

-----

## 9. Setup & on-stage runbook (goes in README)

```bash
# one-time
cp .env.example .env        # add OPENAI_API_KEY; leave DHL_MODE=mock
npm install                 # root + web
pip install -r agent/requirements.txt

# on stage — ONE command
make dev                    # starts web :3000 + agent :8123 (mock mode)
```

- Rehearse in `mock`. Only switch `DHL_MODE=live` if you have keys and a stable network.
- Pre-open all four tabs once before going live (warms the agent).
- Have `docs/DEMO_SCRIPT.md` on a second screen.

-----

## 10. Demo script outline (per tab)

1. **Open on Controlled.** Type a tracking number. “Reliable, brand-safe — the 80% case.”
1. **Declarative.** Ask for shipping options. Re-ask differently → different layout appears. “Same bricks, agent-assembled.”
1. **MCP Apps.** Pick a locker in the embedded map. “3rd-party surface, my agent.”
1. **Open-Ended.** “Visualize the journey.” Flip the Live toggle for the wow (with the honest caveat).
1. **Close on the SpectrumBar.** “One product, four ways. Pick the band per surface — that’s the real lesson.”

-----

## 11. Build order (suggested for whoever implements)

1. Scaffold repo + theme + tab shell + SpectrumBar (static).
1. Python agent + GPT-4o + mock DHL client + 5 tools.
1. Wire CopilotKit runtime route ↔ LangGraph (AG-UI).
1. **Controlled** band end-to-end (proves the pipe).
1. **Declarative** band + A2UI catalog.
1. **MCP Apps** with local stub server.
1. **Open-Ended** with recorded response + live toggle.
1. Live-mode DHL client + `.env` wiring.
1. README runbook + DEMO_SCRIPT + rehearse.

-----

## 12. Open risks / things to verify during build

- Exact CopilotKit API surface (`useComponent`, `a2ui`, `MCPApps`, `openGenerativeUI`) — pin versions; these are young APIs and prop names may differ by release. **Check the live CopilotKit docs at build time.**
- A2UI spec is new (Google + CopilotKit launch) — confirm current catalog schema.
- MCP Apps integration is iframe-only today; fine for web demo, not mobile.
- Real DHL OAuth flows differ per division — only wire the ones you’ll actually demo live.