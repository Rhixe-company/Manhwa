from django.core.management.base import BaseCommand

# from redis import from_url

from scrapy.crawler import CrawlerRunner

from scrapy.settings import Settings
from twisted.internet import defer, reactor
from crawler import settings as my_settings
from config.settings.base import env

from crawler.spiders.asuratoon import AsuratoonSpider


class Command(BaseCommand):
    help = "A  Custom command to  run my spiders"

    def handle(self, *args, **options):
        # redisClient = from_url(env("CELERY_BROKER_URL"))

        # # Push URLs to Redis Queue
        # redisClient.lpush(
        #     "asuratoon_queue:start_urls",
        #     "https://asuratoon.com/manga/?page=1&order=update",
        # )

        crawler_settings = Settings()
        crawler_settings.setmodule(my_settings)

        runner = CrawlerRunner(settings=crawler_settings)

        @defer.inlineCallbacks
        def run():
            yield runner.crawl(AsuratoonSpider)
            reactor.stop()

        run()
        results = reactor.run()

        return results
