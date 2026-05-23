"use client";

import clsx from "clsx";
import { useState } from "react";
import { BANDS, type BandId } from "./bands";
import { SpectrumBar } from "./SpectrumBar";
import { ControlledTab } from "./bands/ControlledTab";
import { DeclarativeTab } from "./bands/DeclarativeTab";
import { McpAppsTab } from "./bands/McpAppsTab";
import { OpenEndedTab } from "./bands/OpenEndedTab";

const RENDERERS: Record<BandId, () => React.ReactNode> = {
  controlled: () => <ControlledTab />,
  declarative: () => <DeclarativeTab />,
  mcp: () => <McpAppsTab />,
  open: () => <OpenEndedTab />,
};

export function TabShell() {
  const [active, setActive] = useState<BandId>("controlled");

  return (
    <div className="flex flex-col">
      <header className="dhl-band">
        <div className="mx-auto max-w-6xl px-6 py-6 flex items-center gap-4">
          <div
            aria-hidden
            className="h-10 w-10 rounded bg-dhl-red text-white grid place-items-center font-black text-lg shadow-chip"
          >
            PP
          </div>
          <div>
            <h1 className="text-2xl font-black tracking-tight text-dhl-ink">
              Parcel Pilot
            </h1>
            <p className="text-sm text-dhl-ink/70">
              A tour of the Generative UI spectrum — powered by DHL Developer Portal API schemas
            </p>
          </div>
        </div>
      </header>

      <nav
        aria-label="Generative UI bands"
        className="border-b border-dhl-line bg-white sticky top-0 z-10"
      >
        <div className="mx-auto max-w-6xl px-6 flex gap-6 overflow-x-auto">
          {BANDS.map((b) => {
            const isActive = b.id === active;
            return (
              <button
                key={b.id}
                onClick={() => setActive(b.id)}
                aria-current={isActive ? "page" : undefined}
                className={clsx(
                  "py-4 border-b-2 text-sm font-semibold whitespace-nowrap transition-colors",
                  isActive
                    ? "tab-active"
                    : "border-transparent text-dhl-ink/60 hover:text-dhl-ink"
                )}
              >
                {b.title}
              </button>
            );
          })}
        </div>
      </nav>

      <SpectrumBar active={active} />

      <section className="mx-auto max-w-6xl px-6 py-8 w-full">
        {RENDERERS[active]()}
      </section>
    </div>
  );
}
