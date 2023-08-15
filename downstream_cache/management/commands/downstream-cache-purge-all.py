from django.core.management.base import BaseCommand

from core.downstream_cache.clients import DownstreamCacheClient


class Command(BaseCommand):
    def handle(self, *args, **options):
        DownstreamCacheClient().purge_all_cache()
