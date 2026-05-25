/**
 * Persistent footer disclaimer — required on every page per the build plan.
 */
export function Footer() {
  return (
    <footer className="border-t border-dhl-line bg-dhl-mist">
      <div className="mx-auto max-w-6xl px-6 py-4 text-xs text-dhl-ink/70">
        Educational demo. Not affiliated with or endorsed by DHL. Uses publicly
        documented DHL Developer Portal API schemas.
      </div>
    </footer>
  );
}
