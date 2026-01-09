import type { Metadata } from "next";
import "./globals.css";
import { RequestLogger } from "../src/components/telemetry/RequestLogger";

// Use system fonts as fallback instead of Google Fonts to avoid network errors
const fontClassName = "font-sans";

export const metadata: Metadata = {
  title: "Clisonix Cloud - Industrial AGI Dashboard",
  description: "The Most Advanced AGI në botë - Industrial Backend with Payment Processing",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={fontClassName}>
        <RequestLogger />
        {children}
      </body>
    </html>
  );
}
