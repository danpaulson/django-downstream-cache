# django-downstream-cache

## Example settings
```
from decouple import config

from core import settings


settings.INSTALLED_APPS += [
    'downstream_cache',
]

DOWNSTREAM_CACHE_RULES = {
    ('/accounts/',): 'private, no-cache, no-store, max-age=0, must-revalidate',
    ('/rss/',): 's-maxage=300',
    ('/sitemap-news.xml',): 's-maxage=300',
    ('/sitemap.xml', '/sitemap-'): 's-maxage=43200',
}

DOWNSTREAM_CACHE_DOMAIN = 'site.com'
DOWNSTREAM_CACHE_CLIENT_PATH = 'downstream_cache.clients.cloudflare_client'
DOWNSTREAM_CACHE_CLIENT_NAME = 'CloudflareClient'
DOWNSTREAM_CACHE_HEADER_NAME = 'Cache-Tag'

DOWNSTREAM_CACHE_FORCE_BROWSER_NO_STORE = True
DOWNSTREAM_CACHE_CLEAR_CACHE = True

CLOUDFLARE_ZONE = config('CLOUDFLARE_ZONE')
CLOUDFLARE_PURGE_TOKEN = config('CLOUDFLARE_PURGE_TOKEN')
```
