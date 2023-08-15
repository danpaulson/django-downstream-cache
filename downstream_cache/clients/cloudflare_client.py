import requests

from django.conf import settings


class CloudflareClient:
    base_api_url = 'https://api.cloudflare.com/client/v4/zones/'

    def __init__(self):
        pass
    
    def purge_all_cache(self):
        api_url = f"{self.base_api_url}{settings.CLOUDFLARE_ZONE}/purge_cache"
        headers = {
            "Authorization": f"Bearer {settings.CLOUDFLARE_PURGE_TOKEN}",
            "Content-Type": "application/json"
            }
        payload = '{"purge_everything":true}'
        r = requests.post(api_url, headers=headers, data=payload)
    
    def purge_by_tags(self, tags: list):
        api_url = f"{self.base_api_url}{settings.CLOUDFLARE_ZONE}/purge_cache"
        headers = {
            "Authorization": f"Bearer {settings.CLOUDFLARE_PURGE_TOKEN}",
            "Content-Type": "application/json"
            }
        tags = '","'.join(tags)
        payload = f'{{"tags":["{tags}"]}}'
        r = requests.post(api_url, headers=headers, data=payload)

    def purge_by_url(self, url: str):
        api_url = f"{self.base_api_url}{settings.CLOUDFLARE_ZONE}/purge_cache"
        headers = {
            "Authorization": f"Bearer {settings.CLOUDFLARE_PURGE_TOKEN}",
            "Content-Type": "application/json"
            }
        payload = f'{{"files":[{{"url":"{url}"}}]}}'
        r = requests.post(api_url, headers=headers, data=payload)
    
    def purge_by_prefix(self, prefix: str):
        api_url = f"{self.base_api_url}{settings.CLOUDFLARE_ZONE}/purge_cache"
        headers = {
            "Authorization": f"Bearer {settings.CLOUDFLARE_PURGE_TOKEN}",
            "Content-Type": "application/json"
            }
        payload = f'{{"prefixes":["{prefix}"]}}'
        r = requests.post(api_url, headers=headers, data=payload)
