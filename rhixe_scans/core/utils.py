from django.db.models import Max
from core.models import UserComics


def get_max_order(user) -> int:
    existing_comics = UserComics.objects.filter(user=user)
    if not existing_comics.exists():
        return 1
    else:
        current_max = existing_comics.aggregate(max_order=Max("order"))["max_order"]
        return current_max + 1


def reorder(user):
    existing_comics = UserComics.objects.filter(user=user)
    if not existing_comics.exists():
        return
    number_of_comics = existing_comics.count()
    new_ordering = range(1, number_of_comics + 1)

    for order, user_comic in zip(new_ordering, existing_comics):
        user_comic.order = order
        user_comic.save()
