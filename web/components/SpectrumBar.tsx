"use client";

import { BANDS, bandById, type BandId } from "./bands";

/**
 * Developer ◄────────────► Agent indicator. Position of the marker reflects
 * the active band; the other bands are shown as faint anchors so the
 * audience sees where it sits on the spectrum.
 */
export function SpectrumBar({ active }: { active: BandId }) {
  const band = bandById(active);

  return (
    <section
      aria-label="Generative UI Spectrum"
      className="border-y border-dhl-line bg-dhl-mist"
    >
      <div className="mx-auto max-w-6xl px-6 py-5">
        <div className="flex items-baseline justify-between text-sm font-medium text-dhl-ink/80">
          <span className="uppercase tracking-wide">Developer control</span>
          <span className="text-dhl-red font-semibold">
            {band.title}
          </span>
          <span className="uppercase tracking-wide">Agent autonomy</span>
        </div>

        <div className="relative mt-3 h-2 rounded-full bg-white border border-dhl-line">
          {/* gradient fill suggests the continuum */}
          <div
            className="absolute inset-y-0 left-0 rounded-full"
            style={{
              width: "100%",
              background:
                "linear-gradient(90deg, #1A1A1A 0%, #D40511 55%, #FFCC00 100%)",
              opacity: 0.12,
            }}
          />

          {/* anchors for the other bands */}
          {BANDS.map((b) => (
            <div
              key={b.id}
              aria-hidden
              className="absolute top-1/2 -translate-y-1/2 h-3 w-px bg-dhl-ink/30"
              style={{ left: `${b.position * 100}%` }}
            />
          ))}

          {/* active marker */}
          <div
            className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 h-5 w-5 rounded-full bg-dhl-red border-2 border-white shadow-chip transition-[left] duration-300"
            style={{ left: `${band.position * 100}%` }}
            aria-label={`Active band: ${band.title}`}
          />
        </div>

        <p className="mt-2 text-xs text-dhl-ink/60">{band.subtitle}</p>
      </div>
    </section>
  );
}
