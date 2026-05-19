/* 고팡 Service Worker v3 — GitHub Pages */
const CACHE = 'gopang-v3';
const ASSETS = ['./', './index.html', './manifest.json',
                './icon-192.png', './icon-512.png'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(ASSETS)));
  self.skipWaiting();
});
self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ));
  self.clients.claim();
});
self.addEventListener('fetch', e => {
  if (e.request.url.includes('deepseek.com') ||
      e.request.url.includes('workers.dev')) return;
  e.respondWith(
    fetch(e.request).catch(() => caches.match(e.request))
  );
});