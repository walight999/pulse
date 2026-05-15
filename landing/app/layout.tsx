import type { Metadata, Viewport } from "next";
import { Analytics } from "@vercel/analytics/react";
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL("https://mintforai.com"),
  title: {
    default: "pulse — Mint for the AI era",
    template: "%s · pulse",
  },
  description:
    "Local-first personal-finance dashboard for the AI era. Track every recurring AI subscription, every Claude token, every hour of focused work — and prove your $200/mo plan returns $4,000 in API-equivalent value.",
  keywords: [
    "AI subscription tracker",
    "Claude token usage",
    "personal finance AI",
    "local-first dashboard",
    "AI spend analytics",
    "Claude Max ROI",
    "ChatGPT cost tracker",
    "developer productivity",
    "subscription manager",
    "open source",
  ],
  authors: [{ name: "White", url: "https://github.com/walight999" }],
  creator: "White",
  publisher: "pulse",
  alternates: { canonical: "/" },
  openGraph: {
    title: "pulse — Mint for the AI era",
    description: "Prove your $200 Claude plan returns $4,000 in API value.",
    url: "https://mintforai.com",
    siteName: "pulse",
    images: [{ url: "/brand/og-social-card.png", width: 1200, height: 630, alt: "pulse dashboard" }],
    locale: "en_US",
    type: "website",
  },
  twitter: {
    card: "summary_large_image",
    title: "pulse — Mint for the AI era",
    description: "Prove your $200 Claude plan returns $4,000 in API value.",
    images: ["/brand/og-social-card.png"],
    creator: "@mintforai",
  },
  icons: {
    icon: "/brand/app-icon.png",
    apple: "/brand/apple-touch-icon.png",
    shortcut: "/brand/app-icon.png",
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-image-preview": "large",
      "max-snippet": -1,
      "max-video-preview": -1,
    },
  },
  category: "productivity",
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: dark)",  color: "#0A0A0F" },
    { media: "(prefers-color-scheme: light)", color: "#10b981" },
  ],
  colorScheme: "dark",
  width: "device-width",
  initialScale: 1,
  maximumScale: 5,
};

const jsonLd = {
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "SoftwareApplication",
      "@id": "https://mintforai.com/#app",
      name: "pulse",
      alternateName: "pulse — Mint for the AI era",
      description:
        "Local-first personal-finance dashboard for the AI era. Tracks AI subscriptions, Claude/ChatGPT/Cursor token usage, and computer activity in one private dashboard.",
      url: "https://mintforai.com",
      applicationCategory: "ProductivityApplication",
      applicationSubCategory: "PersonalFinance",
      operatingSystem: "Windows, macOS, Linux",
      softwareVersion: "1.5",
      datePublished: "2026-05-11",
      license: "https://github.com/walight999/pulse/blob/main/LICENSE",
      offers: [
        {
          "@type": "Offer",
          name: "Free",
          price: "0",
          priceCurrency: "USD",
          description: "Free local app, fully featured. MIT-licensed.",
        },
        {
          "@type": "Offer",
          name: "Pro",
          price: "9",
          priceCurrency: "USD",
          billingDuration: "P1M",
          description: "Cloud sync, mobile PWA, multi-provider live, friend leaderboard.",
        },
        {
          "@type": "Offer",
          name: "Team",
          price: "19",
          priceCurrency: "USD",
          billingDuration: "P1M",
          description: "Per-seat. Shared team dashboard, Slack/Teams/Discord, admin controls.",
        },
      ],
      author: {
        "@id": "https://mintforai.com/#organization",
      },
    },
    {
      "@type": "Organization",
      "@id": "https://mintforai.com/#organization",
      name: "pulse",
      url: "https://mintforai.com",
      logo: "https://mintforai.com/brand/logomark.png",
      sameAs: [
        "https://github.com/walight999/pulse",
      ],
      contactPoint: {
        "@type": "ContactPoint",
        contactType: "customer support",
        email: "hi@mintforai.com",
        availableLanguage: ["English", "Thai"],
      },
    },
    {
      "@type": "WebSite",
      "@id": "https://mintforai.com/#website",
      url: "https://mintforai.com",
      name: "pulse",
      description: "Mint for the AI era — local-first personal-finance dashboard.",
      publisher: { "@id": "https://mintforai.com/#organization" },
      inLanguage: "en-US",
    },
    {
      "@type": "FAQPage",
      "@id": "https://mintforai.com/#faq",
      mainEntity: [
        {
          "@type": "Question",
          name: "Is Free really free forever?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "Yes. The local desktop app is MIT-licensed open source. Revenue comes from cloud sync, team dashboards, and enterprise services — not from selling binaries.",
          },
        },
        {
          "@type": "Question",
          name: "Why do you charge for Pro if everything is open-source?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "You're paying for the cloud infrastructure (encrypted sync server, mobile PWA hosting, friend leaderboard ranking, AI assistant API). You can self-host the cloud server from the same repo for free.",
          },
        },
        {
          "@type": "Question",
          name: "Can I cancel any time?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "Yes. Pro is month-to-month. Team has a 14-day money-back guarantee. Enterprise contracts are annual with 30-day exit clauses.",
          },
        },
        {
          "@type": "Question",
          name: "When does Pro launch?",
          acceptedAnswer: {
            "@type": "Answer",
            text: "Q3 2026. Waitlist signups get 1 month free + early access to friend leaderboard invite codes.",
          },
        },
      ],
    },
  ],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="font-sans antialiased">
        {children}
        {/* Privacy-safe analytics: no cookies, no PII. Disabled at build time
            if NEXT_PUBLIC_ANALYTICS_DISABLED=1. See WAITLIST_SETUP.md. */}
        {process.env.NEXT_PUBLIC_ANALYTICS_DISABLED !== "1" && <Analytics />}
      </body>
    </html>
  );
}
