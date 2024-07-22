from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from core.models import Chapter, Comic


class DuplicatesPipeline:
    def __init__(self):
        self.titles_seen = set()
        self.names_seen = set()
        self.title_seen = Comic.objects.all().values_list("title", flat=True)
        self.name_seen = Chapter.objects.all().values_list("slug", flat=True)

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get("images"):
            if adapter.get("images") and adapter.get("title"):
                if (
                    adapter["slug"] in self.titles_seen
                    and adapter["title"] in self.title_seen
                ):
                    raise DropItem(
                        f"Comic-Item: {item!r} Already Exists In The Database"
                    )
                elif adapter["title"] not in self.title_seen:
                    return item
                else:
                    self.titles_seen.add(adapter["slug"])
                    return item

            if (
                adapter.get("images")
                and adapter.get("comictitle")
                and adapter.get("chaptername")
            ):
                if (
                    adapter["chapterslug"] in self.names_seen
                    and adapter["chapterslug"] in self.name_seen
                ):
                    raise DropItem(
                        f"Chapter-Item: {item!r} Already Exists In The Database"
                    )
                elif adapter["chapterslug"] not in self.name_seen:
                    return item
                else:
                    self.names_seen.add(adapter["chapterslug"])
                    return item

        else:
            raise DropItem(f"DuplicatesPipeline Item has a Missing field in:{item!r}")
