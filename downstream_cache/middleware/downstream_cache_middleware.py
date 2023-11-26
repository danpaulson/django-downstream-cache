from django.conf import settings


class DownstreamCacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        path = request.path
        cache_rules = getattr(settings, 'DOWNSTREAM_CACHE_RULES', {})

        for paths, control in cache_rules.items():
            if path.startswith(paths):
                response['Cache-Control'] = control
                break

        if getattr(settings, 'DOWNSTREAM_CACHE_FORCE_BROWSER_NO_STORE', False):
            # Preserve existing Cache-Control directives, if any
            existing_cache_control = response.get('Cache-Control', '')
            if existing_cache_control:
                # Add the new directives while keeping the existing ones
                response['Cache-Control'] = f'{existing_cache_control}, no-cache, no-store, max-age=0, must-revalidate'
            else:
                # If there were no existing directives, just set the new ones
                response['Cache-Control'] = 'no-cache, no-store, max-age=0, must-revalidate'

        # Noindex API
        if path.startswith('/api/'):
            response['X-Robots-Tag'] = 'noindex'

        return response
