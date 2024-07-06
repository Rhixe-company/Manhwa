import scrapy
from itemloaders import ItemLoader
from scraper.items import (
    MComicItem,
    MChapterItem,
)


class ManganatoSpider(scrapy.Spider):
    name = "manganato"
    allowed_domains = ["manganato.com"]
    start_urls = ["https://manganato.com/genre-all"]

    # redis_key = "asuratoon_queue:start_urls"

    # redis_batch_size = 1

    # max_idle_time = 7

    def start_requests(self):
        return [
            scrapy.FormRequest(
              "https://user.manganelo.com/login?l=manganato&re_l=login",
                formdata={"username": "rhixeero", "password": "alexander"},
                callback=self.parse,
            )
        ]

    def parse(self, response):
        self.logger.info("A response from %s just arrived!", response.url)
        comic_links = response.xpath("//div[@class='genres-item-info']/h3/a/@href")
        yield from response.follow_all(comic_links, callback=self.parse_item)
        # pages = response.xpath("//div[@class='group-page']/a/@href")
        # yield from response.follow_all(pages, callback=self.parse)

    def parse_item(self, response):
        loader = ItemLoader(item=MComicItem(), selector=response)
        image = response.urljoin(
            response.xpath("//span[@class='info-image']/img/@src").get()
        )
        loader.add_value("url", response.url)
        loader.add_value("slug", response.url)
        loader.add_xpath("title", "//div[@class='story-info-right']/h1/text()")
        loader.add_value("image_urls", image)
        item = loader.load_item()

        yield item
