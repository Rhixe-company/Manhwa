import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from itemloaders import ItemLoader
from scraper.items import ComicItem, ChapterItem


class WebtoonSpider(CrawlSpider):
    name = "webtoon"
    allowed_domains = ["webtoon.com"]
    start_urls = ["https://www.webtoons.com/en/genres/"]
    # redis_key = "asuratoon_queue:start_urls"

    # redis_batch_size = 1

    # max_idle_time = 7

    le_comic_details = LinkExtractor(restrict_xpaths="//ul[@class='card_lst']/li/a")

    le_next = LinkExtractor(restrict_xpaths='//ul[@class="snb _genre"]/li/a')

    rule_comic_details = Rule(le_comic_details, callback="parse_item", follow=False)

    rule_next = Rule(le_next, follow=True)

    rules = (
        rule_comic_details,
        # rule_next,
    )

    def parse_item(self, response):

        image = response.urljoin(
            response.xpath("normalize-space(//span[@class='thmb']/img/@src)").get()
        )
        title = response.xpath("normalize-space(//div[@class='info']/h1/text())").get()

        comic = (image, title)
        print(comic)
        yield comic
