// Service worker: lets the app open with no internet once it has been
// visited online. The browser runs this file in the background.
//
// How it works ("stale-while-revalidate"):
//   - Every request for one of the app's files is answered from the saved
//     copy straight away (fast, and works offline).
//   - At the same time, a fresh copy is fetched and saved for next time.
// So after you upload a change to GitHub, it shows up the second time you
// open the app (the first visit fetches it, the next one uses it).
//
// Change VERSION to force every device to throw away its old copies.
const VERSION = "hz-v1";

const FILES = [
  "./",
  "index.html",
  "lib/hanzi-writer.min.js",
  "data/strokes.js",
  "data/words.js",
  "data/topics.js",
  "data/dict.js",
];

// First visit: download and save every file.
self.addEventListener("install", (event) => {
  event.waitUntil(caches.open(VERSION).then((cache) => cache.addAll(FILES)));
  self.skipWaiting();
});

// Remove copies saved under an older VERSION.
self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys().then((names) =>
      Promise.all(names.filter((n) => n !== VERSION).map((n) => caches.delete(n))))
  );
  self.clients.claim();
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  // Only this app's own files. Downloads from other sites (stroke data for
  // extra characters) go straight to the network; the app saves those itself.
  if (event.request.method !== "GET" || url.origin !== location.origin) return;

  event.respondWith(
    caches.open(VERSION).then(async (cache) => {
      const saved = await cache.match(event.request, { ignoreSearch: true });
      const fresh = fetch(event.request)
        .then((res) => { if (res.ok) cache.put(event.request, res.clone()); return res; })
        .catch(() => saved);   // offline: fall back to the saved copy
      return saved || fresh;
    })
  );
});
