import type { MetadataRoute } from "next";

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: "pulse — Mint for the AI era",
    short_name: "pulse",
    description:
      "Local-first personal-finance dashboard for AI subscriptions, Claude tokens, and focused work.",
    start_url: "/",
    display: "standalone",
    orientation: "portrait-primary",
    background_color: "#0A0A0F",
    theme_color: "#10b981",
    categories: ["productivity", "finance", "developer", "utilities"],
    lang: "en-US",
    icons: [
      {
        src: "/brand/icon-192.png",
        sizes: "192x192",
        type: "image/png",
        purpose: "any",
      },
      {
        src: "/brand/icon-512.png",
        sizes: "512x512",
        type: "image/png",
        purpose: "any",
      },
      {
        src: "/brand/icon-512-maskable.png",
        sizes: "512x512",
        type: "image/png",
        purpose: "maskable",
      },
      {
        src: "/brand/apple-touch-icon.png",
        sizes: "180x180",
        type: "image/png",
        purpose: "any",
      },
    ],
    shortcuts: [
      {
        name: "Join Pro waitlist",
        short_name: "Pro",
        description: "Get early access to cloud sync + mobile",
        url: "/#waitlist",
      },
      {
        name: "View pricing",
        short_name: "Pricing",
        description: "Compare Free, Pro, Team, Enterprise",
        url: "/#pricing",
      },
    ],
    related_applications: [
      {
        platform: "windows",
        url: "https://github.com/walight999/pulse/releases",
      },
    ],
    prefer_related_applications: false,
  };
}
