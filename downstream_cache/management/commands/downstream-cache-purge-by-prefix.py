from django.conf import settings
from django.core.management.base import BaseCommand

from downstream_cache.clients import DownstreamCacheClient


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('prefix', type=str, nargs='?', default=None)

    def handle(self, *args, **options):
        """
        Purge cache by prefix
        Ex: domain.com/foo
        """
        DownstreamCacheClient().purge_by_prefix(prefix=options['prefix'])
