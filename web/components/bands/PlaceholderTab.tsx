import { bandById, type BandId } from "../bands";

/**
 * Shared placeholder shell for the four bands while step 4-7 are not yet
 * built. Once a band's real interaction lands, replace its tab file's
 * contents with the live component.
 */
export function PlaceholderTab({
  id,
  buildStep,
  talkingPoint,
}: {
  id: BandId;
  buildStep: number;
  talkingPoint: string;
}) {
  const band = bandById(id);

  return (
    <div className="grid gap-6 md:grid-cols-[1fr_320px]">
      <article className="rounded-lg border border-dhl-line bg-white p-6 shadow-chip">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-dhl-red">
          <span className="inline-block h-2 w-2 rounded-full bg-dhl-red" />
          Band · {band.title}
        </div>
        <h2 className="mt-2 text-2xl font-bold text-dhl-ink">
          {band.subtitle}
        </h2>
        <p className="mt-4 text-dhl-ink/80 leading-relaxed">
          The live interaction for this band is wired up in{" "}
          <strong>build step {buildStep}</strong>. The scaffold and agent are
          ready; the UI just isn't plugged in yet.
        </p>
        <blockquote className="mt-4 border-l-4 border-dhl-yellow bg-dhl-mist px-4 py-3 text-sm italic text-dhl-ink/80">
          “{talkingPoint}”
        </blockquote>
      </article>

      <aside className="rounded-lg border border-dhl-line bg-dhl-mist p-5 text-sm">
        <h3 className="text-xs font-semibold uppercase tracking-wide text-dhl-ink/60">
          DHL API
        </h3>
        <p className="mt-1 font-semibold text-dhl-ink">{band.dhlApi}</p>

        <h3 className="mt-4 text-xs font-semibold uppercase tracking-wide text-dhl-ink/60">
          Status
        </h3>
        <p className="mt-1 text-dhl-ink/80">
          Scaffold ready · interaction pending
        </p>
      </aside>
    </div>
  );
}
