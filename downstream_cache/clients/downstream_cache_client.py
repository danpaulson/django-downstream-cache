import importlib

from typing import (
    List,
    Union,
)

from django.conf import settings
from django.core.management.base import CommandError


class DownstreamCacheClient:
    client = None

    def __init__(self):
        class_ = getattr(
            importlib.import_module(settings.DOWNSTREAM_CACHE_CLIENT_PATH),
            settings.DOWNSTREAM_CACHE_CLIENT_NAME
        )
        self.client = class_()

    def purge_all_cache(self):
        if not settings.DOWNSTREAM_CACHE_CLEAR_CACHE:
            return 'Cache purge is disabled'

        self.client.purge_all_cache()

    def purge_by_host(self, hosts: Union[str, List[str]]):
        if not settings.DOWNSTREAM_CACHE_CLEAR_CACHE:
            return 'Cache purge is disabled'

        if isinstance(hosts, str):
            hosts = [hosts]

        self.client.purge_by_host(hosts)

    def purge_by_url(self, url: str):
        if not settings.DOWNSTREAM_CACHE_CLEAR_CACHE:
            return 'Cache purge is disabled'

        if not url:
            raise CommandError('URL is required')

        self.client.purge_by_url(url)

    def purge_by_tag(self, tags: Union[str, List[str]]):
        if not settings.DOWNSTREAM_CACHE_CLEAR_CACHE:
            return 'Cache purge is disabled'

        if isinstance(tags, str):
            tags = [tags]

        self.client.purge_by_tag(tags)

    def purge_by_prefix(self, prefix: str):
        if not settings.DOWNSTREAM_CACHE_CLEAR_CACHE:
            return 'Cache purge is disabled'

        if not prefix:
            raise CommandError('Prefix is required')

        self.client.purge_by_prefix(prefix)
