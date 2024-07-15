from django.utils import timezone

# from django.utils.timezone import make_aware
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem


class ScraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        if adapter.get("image_urls"):

            if adapter.get("image_urls") and adapter.get("title"):
                date = timezone.now()
                item["crawled"] = date
                # item["crawled"] = datetime.now().date()

                return item

            if (
                adapter.get("image_urls")
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
