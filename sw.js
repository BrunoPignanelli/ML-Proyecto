// Service Worker — PETINSA v1
const CACHE = 'petinsa-v1';
const SHELL = ['/petinsa_envios.html', '/manifest.json', '/icon.svg'];

// Instalar: pre-cachear el shell de la app
self.addEventListener('install', e => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(SHELL))
  );
});

// Activar: limpiar caches viejas
self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(
        keys.filter(k => k !== CACHE).map(k => caches.delete(k))
      ))
      .then(() => self.clients.claim())
  );
});

// Fetch: network-first con fallback a cache
self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);

  // Supabase API → siempre red, nunca cachear datos
  if (url.hostname.includes('supabase.co')) return;

  // CDN externo (Bootstrap, Chart.js) → cache-first
  if (url.hostname.includes('cdn.jsdelivr.net')) {
    e.respondWith(
      caches.match(e.request).then(cached => cached || fetch(e.request)
        .then(res => {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone));
          return res;
        })
      )
    );
    return;
  }

  // HTML, manifest, icono → network-first (datos frescos), cache como respaldo offline
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
