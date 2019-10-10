let staticCacheName = 'mysign_app';
// Clear cache on activate
self.addEventListener('activate', event => {
	// Clean cache files
	event.waitUntil(
		caches.keys().then(cacheNames => {
			return Promise.all(
				cacheNames
					.filter(cacheName => (cacheName.startsWith('mysign_app')))
					.filter(cacheName => (cacheName !== staticCacheName))
					.map(cacheName => caches.delete(cacheName))
			);
		})
	);
});

// Serve from Cache
self.addEventListener('fetch', function (event) {
	event.respondWith(
		caches.open(staticCacheName).then(function (cache) {
			return cache.match(event.request).then(function (response) {
				return fetch(event.request).then(function (response) {
					cache.put(event.request, response.clone());
					return response;
				}).catch(function () {
					return response;
				});
			});
		})
	);
});
