'use strict';

self.addEventListener('install', () => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    (async () => {
      try {
        await self.registration.unregister();
      } catch (e) {
        console.warn('Failed to unregister the service worker:', e);
      }

      try {
        const clients = await self.clients.matchAll({
          type: 'window',
        });
        // Reload clients to ensure they are not using the old service worker.
        clients.forEach((client) => {
          if (client.url && 'navigate' in client) {
            client.navigate(client.url);
          }
        });
      } catch (e) {
        console.warn('Failed to navigate some service worker clients:', e);
      }
    })()
  );
});

// Bypass the service worker for Django admin, API and other server-handled paths
self.addEventListener('fetch', (event) => {
  try {
    const url = new URL(event.request.url);
    const pathname = url.pathname || '';
    if (pathname.startsWith('/admin') || pathname.startsWith('/django-admin') || pathname.startsWith('/api')) {
      // Let the request go to network / server as usual
      return;
    }
  } catch (e) {
    // If URL parsing fails, do nothing and let other handlers (if any) manage the request
  }
});
