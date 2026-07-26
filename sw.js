/* Karaoke Night — offline support.
 *
 * Strategy: network-first, falling back to cache.
 *
 * That order matters. You edit the Excel, run build.py and push a new songs.js;
 * a cache-first worker would keep serving the old song list until the cache
 * expired, which is the classic "why won't my PWA update" trap. Network-first
 * means an online phone always sees the latest songs, and an offline one (a
 * karaoke bar basement, say) still gets the full app from cache.
 */

const CACHE = "karaoke-v1";

const ASSETS = [
  "./",
  "./index.html",
  "./songs.js",
  "./manifest.webmanifest",
  "./icons/icon-192.png",
  "./icons/icon-512.png",
  "./icons/apple-touch-icon.png",
  "./icons/favicon-32.png"
];

self.addEventListener("install", (e) => {
  e.waitUntil(
    caches.open(CACHE)
      // Individual failures shouldn't abort the whole install.
      .then((c) => Promise.allSettled(ASSETS.map((u) => c.add(u))))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const req = e.request;

  // Only our own GETs. Leave YouTube and everything else alone.
  if (req.method !== "GET") return;
  if (new URL(req.url).origin !== self.location.origin) return;

  e.respondWith(
    fetch(req)
      .then((res) => {
        if (res && res.ok) {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy)).catch(() => {});
        }
        return res;
      })
      .catch(() =>
        caches.match(req).then((hit) => {
          if (hit) return hit;
          // A navigation with nothing cached for that exact URL still needs a
          // page, or the user gets the browser's offline dinosaur.
          if (req.mode === "navigate") return caches.match("./index.html");
          return Response.error();
        })
      )
  );
});
