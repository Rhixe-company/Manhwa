from django.db import models
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
from django.urls import reverse
from core.managers import NewManager
from django.db.models.functions import Lower, Upper
from django.utils.translation import gettext_lazy as _
import uuid
from mptt.models import MPTTModel, TreeForeignKey
from django.utils import timezone
from django.template.defaultfilters import slugify  # new

from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
User = get_user_model()


def panel_location(instance, filename):
    return "{}/{}/{}".format(
        str(instance.chapter.comic.slug)
        .replace(" ", "_")
        .replace(":", " ")
        .replace("/", "")
        .replace("\\", ""),
        instance.chapter.slug,
        filename,
    )


def comment_location(instance, filename):
    return "{}/{}/{}".format(
        str(instance.chapter.comic.slug)
        .replace(" ", "_")
        .replace(":", " ")
        .replace("/", "")
        .replace("\\", ""),
        instance.chapter.slug,
        filename,
    )


def comic_location(instance, filename):
    return "{}/{}".format(
        str(instance.slug)
        .replace(" ", "_")
        .replace(":", " ")
        .replace("/", "")
        .replace("\\", ""),
        filename,
    )


ext_validator = FileExtensionValidator(
    ["ico", "png", "jpg", "svg", "jpeg", "gif", "webp", "ttf", "eot", "woff", "woff2"]
)


class Genre(models.Model):
    name = models.CharField(_("Name"), max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Genres"

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("genre:detail", kwargs={"pk": self.pk})


class Author(models.Model):
    name = models.CharField(_("Name"), max_length=500, unique=True)

    class Meta:
        verbose_name_plural = "Authors"

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("author:detail", kwargs={"pk": self.pk})


class Artist(models.Model):
    name = models.CharField(_("Name"), max_length=500, unique=True)

    class Meta:
        verbose_name_plural = "Artists"

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("artist:detail", kwargs={"pk": self.pk})


class Category(models.Model):
    name = models.CharField(_("Name"), max_length=1020, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("category:detail", kwargs={"pk": self.pk})


class Comic(models.Model):
    options = (
        ("Completed", "completed"),
        ("Ongoing", "ongoing"),
        ("Dropped", "dropped"),
        ("Coming_Soon", "coming_soon"),
        ("Hiatus", "hiatus"),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("Title"), max_length=50000, unique=True)
    slug = models.SlugField(
        _("Slug"), max_length=50000, unique=True, default="", null=False, blank=True
    )
    images = models.ImageField(
        _("Images"),
        upload_to=comic_location,
        validators=[ext_validator],
        max_length=40000,
        default="/images/placeholder.png",
        blank=True,
    )
    image_urls = models.URLField(max_length=40000, null=True, blank=True)

    description = models.TextField(_("Description"), blank=True, null=True)
    status = models.CharField(_("Status"), max_length=150, choices=options)
    rating = models.FloatField(_("Rating"))
    alternativetitle = models.CharField(
        _("Alternative Title"), max_length=50000, null=True, blank=True
    )
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comic_author",
    )
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comic_artist",
    )
    released = models.CharField(_("Released"), max_length=50000, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="comic_category"
    )
    serialization = models.CharField(
        _("Serialization"), max_length=50000, null=True, blank=True
    )
    postedby = models.CharField(_("Posted by"), max_length=50000, null=True, blank=True)
    numChapters = models.PositiveSmallIntegerField(_("Total Chapters"), default=0)
    url = models.URLField(_("Url"), max_length=50000, null=True, blank=True)

    updated_at = models.DateTimeField(_("Updated"), default=timezone.now)
    crawled = models.DateField(_("Downloaded"))
    created_at = models.DateField(_("Published"))
    genres = models.ManyToManyField(Genre, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    users = models.ManyToManyField(
        User, related_name="comics", through="UserComics", blank=True
    )
    likes = models.ManyToManyField(User, related_name="like", default=None, blank=True)
    like_count = models.BigIntegerField(default="0")
    thumbsup = models.IntegerField(default="0")
    thumbsdown = models.IntegerField(default="0")
    thumbs = models.ManyToManyField(
        User, related_name="thumbs", default=None, blank=True
    )

    objects = NewManager.as_manager()

    class Meta:
        ordering = ["-updated_at", Lower("title")]
        get_latest_by = "updated_at"

        verbose_name_plural = "Comics"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.images and self.images != "/images/placeholder.png":
            self.images.delete()
        super().delete(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("comics:detail", kwargs={"pk": self.slug})

    def update_absolute_url(self) -> str:
        return reverse("comics:update-comic", kwargs={"pk": self.id})

    def delete_absolute_url(self) -> str:
        return reverse("comics:delete-comic", kwargs={"pk": self.id})


class UserComics(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comic = models.ForeignKey(Comic, on_delete=models.CASCADE)
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.comic.title


class Chapter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(_("Name"), max_length=50000)
    slug = models.SlugField(
        _("Slug"), max_length=50000, unique=True, default="", null=False
    )
    crawled = models.DateField(_("Downloaded"), default="")
    url = models.URLField(_("Url"), max_length=50000, null=True, blank=True)
    numPages = models.PositiveSmallIntegerField(_("Total Pages"), default=0)
    comic = models.ForeignKey(
        Comic, on_delete=models.CASCADE, related_name="chapter_comic"
    )
    updated_at = models.DateTimeField(_("Updated"), auto_now=True)
    created_at = models.DateField(_("Published"), auto_now_add=True)

    class Meta:
        ordering = [Upper("name")]
        get_latest_by = "-updated_at"
        verbose_name_plural = "Chapters"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("chapters:detail", kwargs={"pk": self.slug})

    def update_absolute_url(self) -> str:
        return reverse("chapters:update-chapter", kwargs={"pk": self.pk})

    def delete_absolute_url(self) -> str:
        return reverse("chapters:delete-chapter", kwargs={"pk": self.pk})


class Panel(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    images = models.ImageField(
        _("Images"),
        upload_to=panel_location,
        validators=[ext_validator],
        max_length=40000,
        default="/images/placeholder.png",
        blank=True,
    )
    image_urls = models.URLField(max_length=40000)
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name="panel_chapter"
    )
    comic = models.ForeignKey(
        Comic, on_delete=models.CASCADE, related_name="panel_comic"
    )

    class Meta:
        verbose_name_plural = "Panels"

    def __str__(self):
        return str(self.image_urls)

    def delete(self, *args, **kwargs):
        if self.images and self.images != "/images/placeholder.png":
            self.images.delete()
        super().delete(*args, **kwargs)


class Comment(MPTTModel):
    name = models.CharField(_("Name"), max_length=50, unique=True)

    body = RichTextUploadingField(_("Body"))
    chapter = models.ForeignKey(
        Chapter, on_delete=models.CASCADE, related_name="comment_chapter"
    )
    user = models.ForeignKey(
        User,
        related_name="comments",
        on_delete=models.CASCADE,
    )
    publish = models.DateTimeField(default=timezone.now)
    parent = TreeForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:

        verbose_name_plural = "Comments"

    def __str__(self):
        return self.name

    def get_absolute_url(self) -> str:
        return reverse("comments:detail", kwargs={"pk": self.pk})


class Vote(models.Model):
    comic = models.ForeignKey(
        Comic,
        related_name="comicid",
        on_delete=models.CASCADE,
        default=None,
        blank=True,
    )
    user = models.ForeignKey(
        User, related_name="userid", on_delete=models.CASCADE, default=None, blank=True
    )
    vote = models.BooleanField(default=True)

    def __str__(self):
        return str(self.vote)
