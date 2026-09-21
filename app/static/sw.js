// Service worker minimal : permet l'installation de l'app (icône sur l'écran
// d'accueil) et un cache léger. Les pages de pronostics changent souvent, donc
// on privilégie le réseau (network-first) et on ne retombe sur le cache que
// hors-ligne, avec une page de repli simple pour la navigation.
const CACHE_NAME = "nba-pronos-v1";
const APP_SHELL = [
  "/static/manifest.json",
  "/static/icons/icon-192.png",
  "/static/icons/icon-512.png",
  "/static/offline.html",
];

self.addEventListener("install", (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const { request } = event;

  if (request.mode === "navigate") {
    event.respondWith(
      fetch(request).catch(() => caches.match("/static/offline.html"))
    );
    return;
  }

  if (request.method === "GET" && new URL(request.url).pathname.startsWith("/static/")) {
    event.respondWith(
      caches.match(request).then((cached) => cached || fetch(request))
    );
  }
});
