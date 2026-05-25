/**
 * Single source of truth for the four Generative UI bands. Used by the tab
 * shell and the SpectrumBar so they never drift apart.
 *
 * `position` is 0..1 along the Developer ◄──► Agent axis — purely visual.
 */

export type BandId = "controlled" | "declarative" | "mcp" | "open";

export interface Band {
  id: BandId;
  title: string;
  subtitle: string;
  position: number;
  dhlApi: string;
}

export const BANDS: Band[] = [
  {
    id: "controlled",
    title: "Controlled",
    subtitle: "Agent picks from pre-built components",
    position: 0.12,
    dhlApi: "Shipment Tracking — Unified",
  },
  {
    id: "declarative",
    title: "Declarative (A2UI)",
    subtitle: "Agent assembles a catalog of building blocks",
    position: 0.4,
    dhlApi: "MyDHL rates + Duty & Tax + Location Finder",
  },
  {
    id: "mcp",
    title: "MCP Apps",
    subtitle: "Sandboxed 3rd-party iframe surface",
    position: 0.68,
    dhlApi: "Location Finder — Unified",
  },
  {
    id: "open",
    title: "Open-Ended",
    subtitle: "Agent generates raw HTML/SVG",
    position: 0.92,
    dhlApi: "Shipment Tracking — Unified (route data)",
  },
];

export const bandById = (id: BandId): Band =>
  BANDS.find((b) => b.id === id) ?? BANDS[0];
