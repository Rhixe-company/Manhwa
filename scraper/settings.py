# Scrapy settings for scraper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import os
import sys
from pathlib import Path

import django
from django.conf import settings

from config.settings.base import env

BOT_NAME = "scraper"

SPIDER_MODULES = ["scraper.spiders"]
NEWSPIDER_MODULE = "scraper.spiders"


# # Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "scraper (+https://www.rhixescans.tk)"
# DECAPTCHA_ENABLED = 1

# DECAPTCHA_SOLVER = "decaptcha.solvers.deathbycaptcha.DeathbycaptchaSolver"
# DECAPTCHA_DEATHBYCAPTCHA_USERNAME = "shirk3y"
# DECAPTCHA_DEATHBYCAPTCHA_PASSWORD = "scraping2014"

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2148.0 Safari/537.36"
# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 64

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 64
CONCURRENT_REQUESTS_PER_IP = 64

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# # Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#     "Accept-Language": "en",
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
SPIDER_MIDDLEWARES = {
    "scraper.middlewares.default.ScraperSpiderMiddleware": 543,
}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scraper.middlewares.rotate.RotateUserAgentMiddleware": 540,
    "scraper.middlewares.retry.TooManyRequestsRetryMiddleware": 541,
    "scraper.middlewares.default.ScraperDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    "scraper.pipelines.default.ScraperPipeline": 100,
    "scraper.pipelines.dupelicate.DuplicatesPipeline": 200,
    # "scraper.pipelines.images.ScraperImagesPipeline": 300,
    # "scraper.pipelines.database.ScraperDbPipeline": 400,
    # "scrapy_redis.pipelines.RedisPipeline": 600,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = "httpcache"
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
from scrapy.utils.reactor import install_reactor

TWISTED_REACTOR = install_reactor(
    "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
)
FEED_EXPORT_ENCODING = "utf-8"


LOG_LEVEL = "INFO"

REQUEST_FINGERPRINTER_CLASS = "scraper.utils.RequestFingerprinter"
RETRY_TIMES = 2
RETRY_ENABLED = True
RETRY_HTTP_CODES = [500, 502, 503, 504, 429, 400, 402, 403, 404, 301, 300, 302]
USER_AGENT_LIST = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
]


BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(os.path.join(BASE_DIR, "config"))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
os.environ.setdefault("DJANGO_ALLOW_ASYNC_UNSAFE", "true")
django.setup()
# Local store
IMAGES_STORE = settings.MEDIA_ROOT

# # Production store
# AWS_ACCESS_KEY_ID = settings.AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY = settings.AWS_SECRET_ACCESS_KEY
# AWS_STORAGE_BUCKET_NAME = settings.AWS_STORAGE_BUCKET_NAME
# IMAGES_STORE = "s3://{}/media/".format(AWS_STORAGE_BUCKET_NAME)
# AWS_REGION_NAME = settings.AWS_S3_REGION_NAME


MEDIA_ALLOW_REDIRECTS = True
REACTOR_THREADPOOL_MAXSIZE = 20
DOWNLOAD_FAIL_ON_DATALOSS = False
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"
# SCHEDULER = "scrapy_redis.scheduler.Scheduler"
# SCHEDULER_PERSIST = False
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderPriorityQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderStack"
# REDIS_URL = env("CELERY_BROKER_URL")
