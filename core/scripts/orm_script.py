from django.utils import timezone
from core.models import Comic, Chapter, Panel, Category, Genre, Comment
from django.db import connection
from django.db.models import F, Count, Q
from pprint import pprint
import random


def run():
    # tit_or_slu = Q(title__icontains="I Am the Fated Villain") & Q(
    #     slug__icontains="1908287720-i-am-the-fated-villain"
    # )
    # recently_created = Q(created_at__gt=timezone.now() - timezone.timedelta(days=7))
    # monthly_created = ~Q(created_at__gt=timezone.now() - timezone.timedelta(days=31))
    # not_monthly_created = ~Q(
    #     created_at__gt=timezone.now() - timezone.timedelta(days=31)
    # ) & Q(rating__gte=10.0)
    # yearly_created = ~Q(
    #     created_at__gt=timezone.now() - timezone.timedelta(days=186)
    # ) & Q(rating__gte=10.0)
    # comics = Comic.objects.filter(yearly_created).order_by("-updated_at")[6:8]
    # comic = Comic.objects.get(title="I Am the Fated Villain")
    # genres = [gen.id for gen in comic.genres.all()]
    # cat = comic.category.id
    # genresquery = Q(genres=genres[0])
    # catquery = Q(category=cat)
    # newcomics = (
    #     Comic.objects.select_related("category")
    #     .prefetch_related("genres")
    #     .filter(catquery & genresquery & not_monthly_created)
    # )
    # rating_has_number = Q(rating__regex=r"[9:10]+")
    # upcomics = Comic.objects.filter(not_monthly_created).values_list("slug", flat=True)
    # # chapters = comic.chapter_set.all()
    # chapters = Chapter.objects.select_related("comic").filter(comic__slug=comic.slug)
    # chapter = chapters[0]
    # panels = Panel.objects.select_related("chapter").filter(chapter__slug=chapter.slug)
    # print({"count": upcomics.count(), "data": upcomics})
    # pprint(connection.queries)
    topcomics = Comic.objects.get_topcomics()
    print({"count": topcomics.count(), "data": topcomics})
