import scrapy


class ToomicsSpider(scrapy.Spider):
    name = "toomics"
    allowed_domains = ["toomics.com"]
    start_urls = ["https://toomics.com/en/webtoon/ranking"]

    def parse(self, response):
        comics = response.xpath(
            '//*[@id="glo_contents"]/div[1]/div[2]/div/div[4]/ul[2]/li/div/a/@href'
        ).getall()
        context = {"title": comics}

        yield context
