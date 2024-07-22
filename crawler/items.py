# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags
from scrapy.item import Field, Item

import dateparser


def get_rating(value):

    return float(value)


def get_date(value):
    object = dateparser.parse(value, date_formats=["%d %B %Y , h:i A"])

    return object


def get_slug(value):
    object = value.split("/")[-2]
    return object

def mget_slug(value):
    # object = value.split("/")[-2]
    object = value.split("/")[-1]
    return object

def get_html(value):
    object = remove_tags(value)
    return object



class ComicItem(Item):
    image_urls = Field()
    images = Field()
    title = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    description = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=Join(),
    )
    slug = Field(input_processor=MapCompose(get_slug), output_processor=TakeFirst())
    postedby = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    rating = Field(input_processor=MapCompose(get_rating), output_processor=TakeFirst())
    status = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    category = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    alternativetitle = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
        default="-",
    )
    released = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    author = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    artist = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    serialization = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    genres = Field()
    numChapters = Field(output_processor=TakeFirst())
    crawled = Field(output_processor=TakeFirst())
    created_at = Field(
        input_processor=MapCompose(str.strip, get_date), output_processor=TakeFirst()
    )
    updated_at = Field(
        input_processor=MapCompose(str.strip, get_date), output_processor=TakeFirst()
    )
    url = Field(output_processor=TakeFirst())
    spider = Field()


class MComicItem(Item):
    image_urls = Field()
    images = Field()
    title = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    description = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=Join(),
    )
    slug = Field(input_processor=MapCompose(get_slug), output_processor=TakeFirst())
    postedby = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    rating = Field(input_processor=MapCompose(get_rating), output_processor=TakeFirst())
    status = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    category = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    alternativetitle = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
        default="-",
    )
    released = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    author = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    artist = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    serialization = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    genres = Field()
    numChapters = Field(output_processor=TakeFirst())
    crawled = Field(output_processor=TakeFirst())
    created_at = Field(
        input_processor=MapCompose(str.strip, get_date), output_processor=TakeFirst()
    )
    updated_at = Field(
        input_processor=MapCompose(str.strip, get_date), output_processor=TakeFirst()
    )
    url = Field(output_processor=TakeFirst())
    spider = Field()


class ChapterItem(Item):
    image_urls = Field()
    images = Field()
    comictitle = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    comicslug = Field(
        input_processor=MapCompose(get_slug), output_processor=TakeFirst()
    )
    chaptername = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    chapterslug = Field(
        input_processor=MapCompose(get_slug), output_processor=TakeFirst()
    )
    numPages = Field(output_processor=TakeFirst())
    crawled = Field(output_processor=TakeFirst())
    posted_on = Field(output_processor=TakeFirst())
    updated_on = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    spider = Field()


class MChapterItem(Item):
    image_urls = Field()
    images = Field()
    comictitle = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    comicslug = Field(
        input_processor=MapCompose(get_slug), output_processor=TakeFirst()
    )
    chaptername = Field(
        input_processor=MapCompose(
            str.strip,
            get_html,
        ),
        output_processor=TakeFirst(),
    )
    chapterslug = Field(
        input_processor=MapCompose(get_slug), output_processor=TakeFirst()
    )
    numPages = Field(output_processor=TakeFirst())
    crawled = Field(output_processor=TakeFirst())
    posted_on = Field(output_processor=TakeFirst())
    updated_on = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    spider = Field()
