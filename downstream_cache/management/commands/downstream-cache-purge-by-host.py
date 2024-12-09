from django.core.management.base import BaseCommand

from downstream_cache.clients import DownstreamCacheClient


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('hosts', nargs='*', default=[])

    def handle(self, *args, **options):
        DownstreamCacheClient().purge_by_host(options.get('hosts', []))
