import type { MetadataRoute } from "next";

const BASE = "https://mintforai.com";
const today = new Date();

export default function sitemap(): MetadataRoute.Sitemap {
  return [
    { url: `${BASE}/`,            lastModified: today, changeFrequency: "weekly",  priority: 1.0 },
    { url: `${BASE}/download`,    lastModified: today, changeFrequency: "weekly",  priority: 0.95 },
    { url: `${BASE}/docs`,        lastModified: today, changeFrequency: "weekly",  priority: 0.9 },
    { url: `${BASE}/#pricing`,    lastModified: today, changeFrequency: "weekly",  priority: 0.9 },
    { url: `${BASE}/#waitlist`,   lastModified: today, changeFrequency: "weekly",  priority: 0.9 },
    { url: `${BASE}/methodology`, lastModified: today, changeFrequency: "monthly", priority: 0.85 },
    { url: `${BASE}/roadmap`,     lastModified: today, changeFrequency: "weekly",  priority: 0.8 },
    { url: `${BASE}/#features`,   lastModified: today, changeFrequency: "weekly",  priority: 0.8 },
    { url: `${BASE}/security`,    lastModified: today, changeFrequency: "monthly", priority: 0.7 },
    { url: `${BASE}/changelog`,   lastModified: today, changeFrequency: "weekly",  priority: 0.7 },
    { url: `${BASE}/privacy`,     lastModified: today, changeFrequency: "monthly", priority: 0.6 },
    { url: `${BASE}/terms`,       lastModified: today, changeFrequency: "monthly", priority: 0.5 },
  ];
}
