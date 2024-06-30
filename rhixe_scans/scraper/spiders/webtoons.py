import scrapy


class WebtoonsSpider(scrapy.Spider):
    name = "webtoons"
    allowed_domains = ["www.webtoons.com"]
    start_urls = [
        "https://www.webtoons.com/en/canvas/list?genreTab=ALL&sortOrder=UPDATE"
    ]

    def parse(self, response):
        comics = response.xpath(
            '//*[@id="content"]/div[2]/div[1]/div[2]/ul/li/a/@href'
        ).getall()
        context = {"title": comics}

        yield context
