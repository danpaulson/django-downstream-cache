from django.core.management.base import BaseCommand

from downstream_cache.clients import DownstreamCacheClient


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('url_to_purge', type=str, nargs='?', default=None)

    def handle(self, *args, **options):
        DownstreamCacheClient().purge_by_url(url=options['url_to_purge'])
