const CACHE_NAME = 'bi-generator-v3';
const CORE_ASSETS = [
  './',
  './index.html',
  './kaart_bedieningen.html',
  './manifest.json',
  './config.js',
  './locs_gps.json',
  './icon.svg',
  './icon-192.png',
  './icon-512.png'
];

// Install: pre-cache essential assets
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(CORE_ASSETS).catch((err) => {
        console.warn('Pre-cache error (ignored):', err);
      });
    })
  );
  self.skipWaiting();
});

// Activate: clean up old caches immediately
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
      );
    })
  );
  self.clients.claim();
});

// Fetch: NETWORK FIRST for HTML & navigation, Cache fallback for offline
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url);

  // For external services, fetch directly
  if (
    url.hostname.includes('arcgisonline.com') ||
    url.hostname.includes('openstreetmap.org') ||
    url.hostname.includes('openrailwaymap.org') ||
    url.hostname.includes('supabase.co')
  ) {
    return;
  }

  // HTML Navigation or Documents: Network First so updates are seen immediately!
  const isHtml = event.request.mode === 'navigate' ||
                 (event.request.headers.get('accept') && event.request.headers.get('accept').includes('text/html')) ||
                 url.pathname.endsWith('.html') ||
                 url.pathname.endsWith('/');

  if (isHtml) {
    event.respondWith(
      fetch(event.request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            const clone = networkResponse.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
          }
          return networkResponse;
        })
        .catch(() => {
          return caches.match(event.request).then((cached) => cached || caches.match('./index.html'));
        })
    );
    return;
  }

  // Static Assets (icons, manifest): Stale-while-revalidate
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      const fetchPromise = fetch(event.request)
        .then((networkResponse) => {
          if (networkResponse && networkResponse.status === 200) {
            caches.open(CACHE_NAME).then((cache) => cache.put(event.request, networkResponse.clone()));
          }
          return networkResponse;
        })
        .catch(() => cachedResponse);

      return cachedResponse || fetchPromise;
    })
  );
});
