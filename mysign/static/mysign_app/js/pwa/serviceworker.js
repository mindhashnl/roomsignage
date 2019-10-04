var staticCacheName = "mysign_app" + new Date().getTime();
var filesToCache = [
  '/screen',
  '/screen/',
  '/serviceworker.js',
  'manifest.json',
    'static/mysign_app/favicon/favicon-32x32.png',
    'static/mysign_app/favicon/favicon-16x16.png',
    'static/mysign_app/favicon/favicon-96x96.png',
];

// Cache on install
self.addEventListener("install", event => {
  this.skipWaiting();
  event.waitUntil(
      caches.open(staticCacheName)
          .then(cache => {
            return cache.addAll(filesToCache);
          })
  )
});

// Clear cache on activate
self.addEventListener('activate', event => {
  event.waitUntil(
      caches.keys().then(cacheNames => {
        return Promise.all(
            cacheNames
                .filter(cacheName => (cacheName.startsWith("mysign_app")))
                .filter(cacheName => (cacheName !== staticCacheName))
                .map(cacheName => caches.delete(cacheName))
        );
      })
  );

  event.respondWith(
    fetch(event.request).catch(() => console.log("you are offline "))
  );
});

// Serve from Cache
self.addEventListener("fetch", event => {
  event.respondWith(
      caches.match(event.request)
          .then(response => {
            return response || fetch(event.request);
          })
          .catch(() => {
            return caches.match('screen');
          })
  )
});

self.setInterval(function() {
  console.log("Tick")
    if (navigator.onLine) {
      console.log("Reload")
      window.location.reload()
    }
}, 5000);