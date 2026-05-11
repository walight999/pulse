import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "pulse — Mint for the AI era",
  description:
    "Local-first personal-finance dashboard for the AI era. Track every recurring AI subscription, every Claude token, every hour of focused work — and prove your $200/mo plan returns $4,000 in API-equivalent value.",
  openGraph: {
    title: "pulse — Mint for the AI era",
    description: "Prove your $200 Claude plan returns $4,000 in API value.",
    url: "https://mintforai.com",
    siteName: "pulse",
    images: [{ url: "/brand/og-social-card.png", width: 1200, height: 630 }],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "pulse — Mint for the AI era",
    description: "Prove your $200 Claude plan returns $4,000 in API value.",
    images: ["/brand/og-social-card.png"],
  },
  icons: {
    icon: "/brand/app-icon.png",
    apple: "/brand/app-icon.png",
  },
  themeColor: "#10b981",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">{children}</body>
    </html>
  );
}
