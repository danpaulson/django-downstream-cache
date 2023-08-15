from django.conf import settings
from django.core.management.base import BaseCommand

from core.downstream_cache.clients import DownstreamCacheClient


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('prefix', type=str, nargs='?', default=None)

    def handle(self, *args, **options):
        DownstreamCacheClient().purge_by_prefix(prefix=options['prefix'])
