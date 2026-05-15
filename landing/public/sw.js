// pulse landing service worker
// ============================================================
// Strategy:
//   - / (home)       → network-first, fall back to cache. The home page changes
//                      most often and we want fresh hero / pricing / waitlist.
//   - /demo, /docs, /methodology, /alternatives, /roadmap, /download,
//     /security, /privacy, /terms, /changelog → stale-while-revalidate.
//     Show cache instantly, fetch in background, update cache for next time.
//   - /brand/*, /samples/*, /favicon.ico, /icons → cache-first (immutable-ish).
//   - /api/* → network only, never cached.
//   - /_next/static/* → cache-first (Next already content-hashes the names).
//
// Bump CACHE_VERSION whenever the precache list changes so old caches are evicted.

const CACHE_VERSION = "pulse-v1.7.0";
const STATIC_CACHE = `${CACHE_VERSION}-static`;
const PAGES_CACHE = `${CACHE_VERSION}-pages`;
const RUNTIME_CACHE = `${CACHE_VERSION}-runtime`;

const PRECACHE_URLS = [
  "/",
  "/offline",
  "/demo",
  "/docs",
  "/methodology",
  "/alternatives",
  "/roadmap",
  "/download",
  "/security",
  "/privacy",
  "/terms",
  "/changelog",
  "/manifest.webmanifest",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    (async () => {
      const cache = await caches.open(PAGES_CACHE);
      // Don't fail install if one URL fails — others should still be cached.
      await Promise.all(
        PRECACHE_URLS.map((url) =>
          cache.add(url).catch((e) => console.warn("[sw] precache skip", url, e))
        )
      );
      self.skipWaiting();
    })()
  );
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    (async () => {
      // Delete caches from older CACHE_VERSION values
      const keys = await caches.keys();
      await Promise.all(
        keys
          .filter((k) => !k.startsWith(CACHE_VERSION))
          .map((k) => caches.delete(k))
      );
      await self.clients.claim();
    })()
  );
});

self.addEventListener("fetch", (event) => {
  const req = event.request;
  if (req.method !== "GET") return;

  const url = new URL(req.url);

  // Same-origin only — don't intercept analytics or third-party fonts
  if (url.origin !== self.location.origin) return;

  // Never cache the waitlist API
  if (url.pathname.startsWith("/api/")) return;

  // Cache-first for content-hashed Next static + brand assets
  if (
    url.pathname.startsWith("/_next/static/") ||
    url.pathname.startsWith("/brand/") ||
    url.pathname.startsWith("/samples/") ||
    url.pathname.startsWith("/icons/") ||
    url.pathname === "/favicon.ico"
  ) {
    event.respondWith(cacheFirst(req, STATIC_CACHE));
    return;
  }

  // Network-first for the home page (most-edited)
  if (url.pathname === "/" || url.pathname === "/index.html") {
    event.respondWith(networkFirst(req, PAGES_CACHE));
    return;
  }

  // Stale-while-revalidate for everything else (subpages)
  if (PRECACHE_URLS.includes(url.pathname)) {
    event.respondWith(staleWhileRevalidate(req, PAGES_CACHE));
    return;
  }

  // Default: try network, fall back to cache, fall back to /offline
  event.respondWith(networkFirstWithOffline(req, RUNTIME_CACHE));
});

async function cacheFirst(req, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(req);
  if (cached) return cached;
  try {
    const resp = await fetch(req);
    if (resp.ok) cache.put(req, resp.clone());
    return resp;
  } catch (e) {
    return Response.error();
  }
}

async function networkFirst(req, cacheName) {
  const cache = await caches.open(cacheName);
  try {
    const resp = await fetch(req);
    if (resp.ok) cache.put(req, resp.clone());
    return resp;
  } catch (e) {
    const cached = await cache.match(req);
    return cached || Response.error();
  }
}

async function staleWhileRevalidate(req, cacheName) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(req);
  const fetchPromise = fetch(req)
    .then((resp) => {
      if (resp.ok) cache.put(req, resp.clone());
      return resp;
    })
    .catch(() => cached);
  return cached || fetchPromise;
}

async function networkFirstWithOffline(req, cacheName) {
  const cache = await caches.open(cacheName);
  try {
    const resp = await fetch(req);
    if (resp.ok) cache.put(req, resp.clone());
    return resp;
  } catch (e) {
    const cached = await cache.match(req);
    if (cached) return cached;
    // Last-resort fallback for navigations
    if (req.mode === "navigate") {
      const offline = await caches.match("/offline");
      if (offline) return offline;
    }
    return Response.error();
  }
}
