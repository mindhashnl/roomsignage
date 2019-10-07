var staticCacheName = "mysign_app";
var filesToCache = [
	'/screen',
	'/screen/',
	'/serviceworker.js',
	'manifest.json',
	'static/mysign_app/favicon/favicon-32x32.png',
	'static/mysign_app/favicon/favicon-16x16.png',
	'static/mysign_app/favicon/favicon-96x96.png',
];
var failedRequests = []

// Cache on install
self.addEventListener("install", event => {
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
					.filter(cacheName => (cacheName.startsWith("mysign_app")))
					.filter(cacheName => (cacheName !== staticCacheName))
					.map(cacheName => caches.delete(cacheName))
			);
		})
	);
});

// Serve from Cache
self.addEventListener("fetch", event => {
	event.respondWith(
		caches.match(event.request).then(function (response) {
			return fetch(event.request).then(function(response){
				console.log('DID FETCHE!')
				return response
			}).catch(function (error) {
				console.log(error)
				failedRequests.push(event.request)
				return response
			})
		})
	);
});

// self.setInterval(function () {
// 	console.log("Tick - 2")
// 	newFailedRequests = []
// 	console.log(failedRequests)
// 	failedRequests.forEach(function (request) {
// 		fetch(request).then(function () {
// 			console.log('DONE!')
// 		}).catch(function (error) {
// 			newFailedRequests.push(newFailedRequests)
// 		})
// 	})
// 	failedRequests = newFailedRequests
//
//
// 	// if (navigator.onLine) {
// 	// console.log("Reload")
// 	// window.location.reload()
// 	// }
// }, 1000);