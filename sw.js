// 车载光学知识工作台 · Service Worker（离线缓存，装到桌面后可离线使用）
const CACHE = 'optics-workbench-v0.8.3';
const ASSETS = [
  './',
  './index.html',
  './manifest.webmanifest',
  './icon-192.png',
  './icon-512.png'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', event => {
  // 导航请求：优先网络，失败回退缓存（保证离线也能开）
  if (event.request.mode === 'navigate') {
    event.respondWith(fetch(event.request).catch(() => caches.match('./index.html')));
    return;
  }
  // 其他资源：缓存优先
  event.respondWith(
    caches.match(event.request).then(r => r || fetch(event.request))
  );
});
