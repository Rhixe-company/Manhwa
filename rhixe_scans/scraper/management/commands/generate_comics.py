import random
from faker import Faker
from django.core.management.base import BaseCommand
from rhixe_scans.users.models import User
from core.models import Comic, Chapter, Panel, Genre, Category, Comment, UserComics


class Command(BaseCommand):
    help = "Generates transactions for testing"

    def handle(self, *args, **options):
        fake = Faker()

        # create categories
        categories = ["Manhwa", "Manhua", "Manga"]

        for category in categories:
            Category.objects.get_or_create(name=category)

        # get the user
        user = User.objects.filter(username="bot").first()
        if not user:
            user = User.objects.create_superuser(username="bot", password="20010709")

        categories = Category.objects.all()
        status = [x[0] for x in Comic.options]
        for i in range(20):
            Comic.objects.create(
                category=random.choice(categories),
                user=user,
                rating=random.uniform(6, 10),
                crawled=fake.date_between(start_date="-1y", end_date="today"),
                status=random.choice(status),
            )
