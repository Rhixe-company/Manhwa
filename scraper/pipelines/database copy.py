from core.models import Category, Chapter, Comic, Genre, Panel, Author, Artist
from django.db.models import Q
from django.db.utils import IntegrityError
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from django.contrib.auth import get_user_model

User = get_user_model()


class ScraperDbPipeline:

    def process_item(self, item, spider):

        adapter = ItemAdapter(item)
        if adapter.get("image_urls"):
            if adapter.get("image_urls") and adapter.get("title"):
                category = Category.objects.filter(
                    Q(name__startswith=item["category"])
                ).update_or_create(name=item["category"])[0]
                artist = Artist.objects.filter(
                    Q(name__startswith=item.get("artist"))
                ).update_or_create(name=item.get("artist"))[0]
                author = Author.objects.filter(
                    Q(name__startswith=item.get("author"))
                ).update_or_create(name=item.get("author"))[0]

                try:
                    user = User.objects.filter(email="admin@rhixe.company").first()
                    if not user:
                        user = User.objects.create_superuser(
                            email="admin@rhixe.company", password="R4I7gcJHX"
                        )
                    comic = Comic.objects.filter(
                        Q(title__startswith=item["title"])
                        | Q(slug__startswith=item.get("slug"))
                        | Q(
                            alternativetitle__startswith=item.get(
                                "alternativetitle", "-"
                            )
                        )
                    ).update_or_create(
                        user=user,
                        category=category,
                        title=item["title"],
                        slug=item["slug"],
                        crawled=item["crawled"],
                        updated_at=item["updated_at"],
                        created_at=item["created_at"],
                        url=item["url"],
                        image_urls=item["image_urls"][0],
                        # images=img["path"],
                        status=item["status"],
                        description=item.get("description"),
                        numChapters=item["numChapters"],
                        rating=item.get("rating"),
                        released=item.get("released"),
                        postedby=item.get("postedby"),
                        alternativetitle=item.get("alternativetitle"),
                        serialization=item.get("serialization"),
                        author=author,
                        artist=artist,
                    )[
                        0
                    ]

                    genres = item.get("genres")
                    if genres:
                        for genre in genres:
                            obj = Genre.objects.filter(
                                Q(name__startswith=genre)
                            ).update_or_create(name=genre)[0]
                            comic.genres.add(obj)
                            comic.save()

                except IntegrityError as e:
                    raise DropItem(f"Comic-Error:   {e!r}")
                # for img in item.get("images"):
                #     try:
                #         user = User.objects.filter(email="admin@rhixe.company").first()
                #         if not user:
                #             user = User.objects.create_superuser(
                #                 email="admin@rhixe.company", password="R4I7gcJHX"
                #             )
                #         comic = Comic.objects.filter(
                #             Q(title__startswith=item["title"])
                #             | Q(slug__startswith=item.get("slug"))
                #             | Q(
                #                 alternativetitle__startswith=item.get(
                #                     "alternativetitle", "-"
                #                 )
                #             )
                #         ).update_or_create(
                #             user=user,
                #             category=category,
                #             title=item["title"],
                #             slug=item["slug"],
                #             crawled=item["crawled"],
                #             updated_at=item["updated_at"],
                #             created_at=item["created_at"],
                #             url=item["url"],
                #             image_urls=img["url"],
                #             images=img["path"],
                #             status=item["status"],
                #             description=item.get("description"),
                #             numChapters=item["numChapters"],
                #             rating=item.get("rating"),
                #             released=item.get("released"),
                #             postedby=item.get("postedby"),
                #             alternativetitle=item.get("alternativetitle"),
                #             serialization=item.get("serialization"),
                #             author=author,
                #             artist=artist,
                #         )[
                #             0
                #         ]

                #         genres = item.get("genres")
                #         if genres:
                #             for genre in genres:
                #                 obj = Genre.objects.filter(
                #                     Q(name__startswith=genre)
                #                 ).update_or_create(name=genre)[0]
                #                 comic.genres.add(obj)
                #                 comic.save()

                #     except IntegrityError as e:
                #         raise DropItem(f"Comic-Error:   {e!r}")

                return item

            if (
                adapter.get("image_urls")
                and adapter.get("comictitle")
                and adapter.get("chaptername")
            ):
                existcom = Comic.objects.filter(
                    Q(title__startswith=item.get("comictitle"))
                    | Q(slug__startswith=item.get("comicslug"))
                ).exists()
                if existcom:

                    if (
                        Comic.objects.filter(
                            Q(title__startswith=item.get("comictitle"))
                            | Q(slug__startswith=item.get("comicslug"))
                        ).count()
                        >= 2
                    ):
                        dbcom = Comic.objects.filter(
                            Q(title__startswith=item.get("comictitle"))
                            | Q(slug__startswith=item.get("comicslug"))
                        ).first()
                        try:
                            chapter = Chapter.objects.filter(
                                Q(name__startswith=item["chaptername"])
                            ).update_or_create(
                                comic=dbcom,
                                name=item["chaptername"],
                                slug=item["chapterslug"],
                                crawled=item["crawled"],
                                url=item["url"],
                                numPages=item.get("numPages"),
                            )[
                                0
                            ]
                        except IntegrityError as e:

                            raise DropItem(f"Chapter-Error:   {e!r}")
                        images = item.get("image_urls")
                        if images:
                            for img in images:
                                try:
                                    page = Panel.objects.filter(
                                        Q(image_urls__startswith=img)
                                    ).update_or_create(
                                        comic=dbcom,
                                        chapter=chapter,
                                        image_urls=img,
                                    )[
                                        0
                                    ]
                                except IntegrityError as e:

                                    DropItem(f"Panel-Error:   {e!r}")
                        # images = item.get("images")
                        # if images:
                        #     for img in images:
                        #         try:
                        #             page = Panel.objects.filter(
                        #                 Q(images__startswith=img)
                        #                 | Q(image_urls__startswith=img["path"])
                        #             ).update_or_create(
                        #                 comic=dbcom,
                        #                 chapter=chapter,
                        #                 image_urls=img["url"],
                        #                 images=img["path"],
                        #             )[
                        #                 0
                        #             ]
                        #         except IntegrityError as e:

                        #             DropItem(f"Panel-Error:   {e!r}")
                    else:
                        dbcom = Comic.objects.get(
                            Q(title__startswith=item.get("comictitle"))
                            | Q(slug__startswith=item.get("comicslug"))
                        )
                        try:
                            chapter = Chapter.objects.filter(
                                Q(name__startswith=item["chaptername"])
                            ).update_or_create(
                                comic=dbcom,
                                name=item["chaptername"],
                                slug=item["chapterslug"],
                                crawled=item["crawled"],
                                url=item["url"],
                                numPages=item.get("numPages"),
                            )[
                                0
                            ]
                        except IntegrityError as e:

                            raise DropItem(f"Chapter-Error:   {e!r}")

                        images = item.get("image_urls")
                        if images:
                            for img in images:
                                try:
                                    page = Panel.objects.filter(
                                        Q(image_urls__startswith=img)
                                    ).update_or_create(
                                        comic=dbcom,
                                        chapter=chapter,
                                        image_urls=img,
                                    )[
                                        0
                                    ]
                                except IntegrityError as e:

                                    DropItem(f"Panel-Error:   {e!r}")
                        # images = item.get("images")
                        # if images:
                        #     for img in images:
                        #         try:
                        #             page = Panel.objects.filter(
                        #                 Q(images__startswith=img)
                        #                 | Q(image_urls__startswith=img["path"])
                        #             ).update_or_create(
                        #                 comic=dbcom,
                        #                 chapter=chapter,
                        #                 image_urls=img["url"],
                        #                 images=img["path"],
                        #             )[
                        #                 0
                        #             ]
                        #         except IntegrityError as e:

                        #             DropItem(f"Panel-Error:   {e!r}")

                return item
