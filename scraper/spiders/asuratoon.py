from itemloaders import ItemLoader
from scraper.items import (
    ComicItem,
    ChapterItem,
)
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider

from scrapy_redis.spiders import RedisCrawlSpider


class AsuratoonSpider(CrawlSpider):
    name = "asuratoon"
    allowed_domains = ["asuratoon.com"]
    start_urls = ["https://asuratoon.com/manga/?page=1&order=update"]
    # redis_key = "asuratoon_queue:start_urls"

    # redis_batch_size = 1

    # max_idle_time = 7

    le_comic_details = LinkExtractor(restrict_xpaths='//div[@class="bsx"]/a')

    le_next = LinkExtractor(restrict_xpaths='//a[@class="r"]')

    rule_comic_details = Rule(le_comic_details, callback="parse_item", follow=False)

    rule_next = Rule(le_next, follow=True)

    rules = (
        rule_comic_details,
        rule_next,
    )

    def parse_item(self, response):

        loader = ItemLoader(item=ComicItem(), selector=response)

        image_urls = response.xpath(
            "normalize-space(//img[@class='wp-post-image']/@src)"
        ).get()
        des = [
            de.strip()
            for de in response.xpath("//div[@itemprop='description']/p/text()").getall()
        ]
        loader.add_value("url", response.url)
        loader.add_value("slug", response.url)
        loader.add_xpath("title", "normalize-space(//h1[@class='entry-title']/text())")

        loader.add_value("image_urls", response.urljoin(image_urls))
        loader.add_value("description", des)
        loader.add_xpath("status", '//div[@class="imptdt"]/i/text()')
        loader.add_xpath("rating", '//div[@itemprop="ratingValue"]/text()')
        loader.add_xpath("category", '//div[@class="imptdt"]/a/text()')
        loader.add_xpath("genres", '//span[@class="mgen"]/a/text()')
        loader.add_xpath(
            "alternativetitle",
            "normalize-space(//div[@class='wd-full'][1]/span/text())",
        )
        loader.add_xpath("released", '//div[@class="fmed"][1]/span/text()')
        loader.add_xpath("author", '//div[@class="fmed"][2]/span/text()')
        loader.add_xpath("artist", '//div[@class="flex-wrap"][2]/div/span/text()')
        loader.add_xpath(
            "serialization", '//div[@class="flex-wrap"][3]/div/span[1]/text()'
        )
        loader.add_xpath("postedby", '//i[@itemprop="name"]/text()')
        loader.add_value(
            "numChapters",
            len(response.xpath('//div[contains(@class, "eph-num")]/a/@href').getall()),
        )
        loader.add_xpath("created_at", '//time[@itemprop="datePublished"]/@datetime')
        loader.add_xpath("updated_at", '//time[@itemprop="dateModified"]/@datetime')
        item = loader.load_item()

        yield item

        # # All Chapter Page
        # chapter_page = response.xpath('//div[contains(@class, "eph-num")]/a/@href')
        # yield from response.follow_all(chapter_page, callback=self.parsechapter)
        # # All Chapter Page
        # chapter_pages = response.xpath(
        #     '//div[contains(@class, "eph-num")]/a/@href'
        # ).getall()
        # if chapter_pages:
        #     for page in chapter_pages:
        #         yield scrapy.Request(response.urljoin(page), callback=self.parsechapter)

        # chapter_page = response.xpath(
        #     '//div[contains(@class, "eph-num")]/a/@href'
        # ).get()
        # if chapter_page:
        #     yield response.follow(chapter_page, callback=self.parsechapter)
        chapter_pages = response.xpath(
            '//div[contains(@class, "eph-num")]/a/@href'
        ).getall()
        if chapter_pages:
            for page in chapter_pages[0:1]:
                yield response.follow(page, callback=self.parsechapter)
        self.logger.info("A New Comic was found at %s", response.url)

    def parsechapter(self, response):

        loader = ItemLoader(item=ChapterItem(), selector=response)
        loader.add_value("url", response.url)
        loader.add_value("chapterslug", response.url)
        loader.add_xpath("chaptername", '//h1[@class="entry-title"]/text()')
        image_urls = response.xpath('//img[@decoding="async"]/@src').getall()
        images = []
        for image in image_urls:
            images.append(response.urljoin(image))
        loader.add_value("image_urls", images)
        loader.add_xpath("comictitle", '//div[@class="allc"]/a/text()')
        loader.add_xpath("comicslug", '//div[@class="allc"]/a/@href')
        loader.add_value(
            "numPages", len(response.xpath('//img[@decoding="async"]/@src').getall())
        )
        item = loader.load_item()
        yield item
        self.logger.info("A New Chapter was found at %s", response.url)
