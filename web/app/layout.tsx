import type { Metadata } from "next";
import "./globals.css";
import { CopilotProvider } from "@/components/CopilotProvider";
import { Footer } from "@/components/Footer";

export const metadata: Metadata = {
  title: "Parcel Pilot — a tour of the Generative UI spectrum",
  description:
    "Educational demo of CopilotKit's four Generative UI bands, powered by DHL Developer Portal API schemas. Not affiliated with DHL.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen flex flex-col bg-white text-dhl-ink">
        <CopilotProvider>
          <main className="flex-1">{children}</main>
          <Footer />
        </CopilotProvider>
      </body>
    </html>
  );
}
