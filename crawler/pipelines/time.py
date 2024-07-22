# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from django.utils import timezone

# from django.utils.timezone import make_aware
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class TimeCrawlerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("images"):

            if adapter.get("images") and adapter.get("title"):
                date = timezone.now()
                item["crawled"] = date
                # item["crawled"] = datetime.now().date()
                item["spider"] = spider.name
                return item

            if (
                adapter.get("images")
                and adapter.get("comictitle")
                and adapter.get("chaptername")
            ):
                date = timezone.now()

                item["crawled"] = date
                # item["crawled"] = datetime.now().date()
                return item
        else:
            raise DropItem(
                f"ScraperPipeline default Item has a Missing field in:{item!r}"
            )
