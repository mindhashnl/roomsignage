let staticCacheName = 'mysign_app';
let filesToCache = [
	'/screen',
	'/screen/',
	'manifest.json',
	'static/mysign_app/favicon/favicon-32x32.png',
	'static/mysign_app/favicon/favicon-16x16.png',
	'static/mysign_app/favicon/favicon-96x96.png'
];
let failedRequests = [];

// Cache on install
self.addEventListener('install', event => {
	this.skipWaiting();
	event.waitUntil(
		caches.open(staticCacheName)
			.then(cache => {
				return cache.addAll(filesToCache);
			})
	);
});

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
self.addEventListener('fetch', event => {
	event.respondWith(
		fetch(event.request).then(function (fetchResponse) {
			// When fetch is successful, cache and return
			caches.open(staticCacheName).then(cache => {
				return cache.addAll(filesToCache);
			});
			return fetchResponse;
		}).catch(function () {
			// Fallback on cache
			return caches.match(event.request).then(response => {
				return response;
			});
		})
	);
});
