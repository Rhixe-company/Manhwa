import factory
from rhixe_scans.users.models import User
from core.models import Comic, Chapter, Panel, Genre, Category, Comment, UserComics
from datetime import datetime


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = (
            "username",
            "email",
        )

    last_name = factory.Faker("last_name")
    first_name = factory.Faker("first_name")
    username = factory.Sequence(lambda n: "user%d" % n)
    email = factory.Sequence(lambda n: "user%d" % n)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ("name",)

    name = factory.Iterator(["Manhwa", "Manhua", "Manga"])


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre
        django_get_or_create = ("name",)

    name = factory.Iterator(
        [
            "Action",
            "Adventure",
            "Fantasy",
            "Regression",
            "Revenge",
            "Game",
            "Psychological",
            "Comedy",
            "Magic",
            "School Life",
        ]
    )


class ComicFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comic

    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(CategoryFactory)
    # genres = factory.SubFactory(GenreFactory)
    rating = factory.Iterator(
        ["5.0", "6.0", "7.0", "8.0", "9.0", "10.0", "9.5", "9.8", "9.1", "9.9"]
    )
    crawled = factory.Faker(
        "date_between",
        start_date=datetime(year=2022, month=1, day=1).date(),
        end_date=datetime.now().date(),
    )
    title = factory.Iterator(
        [
            "A Comic Artist’s Survival Guide",
            "Above the Heavens",
            "Absolute Necromancer",
            "Absolute Sword Sense",
            "Academy’s Genius Swordmaster",
            "Academy’s Undercover Professor",
            "Arcana Fantasy",
            "Archmage Transcending Through Regression",
            "Barbarian Quest",
            "Bloodhound’s Regression Instinct",
        ]
    )
    slug = factory.Iterator(
        [
            "1908287720-a-comic-artists-survival-guide",
            "1908287720-above-the-heavens",
            "1908287720-absolute-necromancer",
            "1908287720-absolute-sword-sense",
            "1908287720-academys-genius-swordmaster",
            "1908287720-academys-undercover-professor",
            "1908287720-arcana-fantasy",
            "1908287720-archmage-transcending-through-regression",
            "1908287720-barbarian-quest",
            "1908287720-bloodhounds-regression-instinct",
        ]
    )
    images = factory.Iterator(
        [
            "/1908287720-a-comic-artists-survival-guide/cbc1a0c35b103ae2c8b91f97d3d3f4c889e012f4cover1.jpg",
            "/1908287720-above-the-heavens/ff272a04febd9d912cec8130f2e80eca488443b1abovetheheavenscover-1.jpg",
            "/1908287720-absolute-necromancer/e6cddc24c7c76ac58270f1be121aba56af8d981dNecromancerCover.jpg",
            "/1908287720-absolute-sword-sense/3c2ec83f9ef849b80ab968cfda02963c4c8cdba8swordsenseCover03.png",
            "/1908287720-academys-genius-swordmaster/e6a5019caaa048906948fa5e0140027582c8fc4bAcademyGeniusSwordmasterCover01.png",
            "/1908287720-academys-undercover-professor/9f22882cb97b10185368af1ee3a8a81a11894b88Academys_Undercover_ProfessorCover_copy.png",
            "/1908287720-arcana-fantasy/530a0feb9c96e0d6a525343276942484bda0735btall.jpg",
            "/1908287720-archmage-transcending-through-regression/6dbc6cf306620ed89cc13fdd8d33927bf0855d1cArchmageTranscendingCover01.png",
            "/1908287720-barbarian-quest/ed9382c87fc1ee26acabd743f09ecb70aae69b31BarbQuest_hElookkindadumbaf-1.jpg",
            "/1908287720-bloodhounds-regression-instinct/1c260bcca243a3e2465d6ce5eaea12c307a0b9c2BloodhoundsRegressionInstinctCover01.png",
        ]
    )
    status = factory.Iterator([x[0] for x in Comic.options])
