import itertools
import django_tables2 as tables
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib.auth import get_user_model
from .models import Chapter, Comic, Panel
from django.conf import settings
from django_tables2.utils import A

User = get_user_model()


class MaterializeCssCheckboxColumn(tables.CheckBoxColumn):
    def render(self, value, bound_column, record):
        default = {"type": "checkbox", "name": bound_column.name, "value": value}
        if self.is_checked(value, record):
            default.update({"checked": "checked"})

        general = self.attrs.get("input")
        specific = self.attrs.get("td__input")
        attrs = tables.utils.AttributeDict(default, **(specific or general or {}))
        return mark_safe(
            '<div class="flex items-center" ><input id="checkbox-table-search-1" type="checkbox" onclick="event.stopPropagation()" class="w-4 h-4 text-primary-600 bg-gray-100 rounded border-gray-300 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"  %s/><label for="checkbox-table-search-1" class="sr-only"></label></div>'
            % attrs.as_html()
        )


class ImageColumn(tables.Column):
    def render(self, value):
        return format_html(
            '<div class="avatar"><div class="mask mask-squircle w-12 h-12"><img     src="/media/{}" /></div></div>',
            value,
        )


class TitleColumn(tables.Column):
    def render(self, value):
        return format_html(
            "<div><h5>{}</h5></div>",
            value,
        )


class ChapterTable(tables.Table):
    id = MaterializeCssCheckboxColumn(accessor="pk", orderable=False)
    name = TitleColumn(linkify=True)
    numPages = tables.Column()
    comic = ImageColumn(accessor="comic__images", linkify=True)
    update = tables.TemplateColumn(
        template_name="partials/chapters/update_button.html", orderable=False
    )
    delete = tables.TemplateColumn(
        template_name="partials/chapters/delete_button.html", orderable=False
    )

    class Meta:
        model = Chapter
        template_name = "django_tables2/semantic.html"
        sequence = ("id", "name", "numPages", "comic", "slug")
        fields = ("id", "name", "numPages", "comic", "slug")
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend",  # Instead of `desc`
                }
            },
        }
        row_attrs = {"data-id": lambda record: record.pk}

    @classmethod
    def render_paginated_table(cls, request):
        table = cls(data=Chapter.objects.all())
        table.paginate(page=request.GET.get("page", 1), per_page=settings.PAGINATE_BY)
        return table


class ComicTable(tables.Table):
    id = MaterializeCssCheckboxColumn(accessor="pk", orderable=False)
    update = tables.TemplateColumn(
        template_name="partials/comics/update_button.html", orderable=False
    )
    delete = tables.TemplateColumn(
        template_name="partials/comics/delete_button.html", orderable=False
    )
    title = TitleColumn(linkify=True)
    images = ImageColumn(accessor="images", linkify=True)
    status = tables.Column()
    category = tables.Column()
    created_at = tables.DateColumn(format="M d Y")
    updated_at = tables.DateTimeColumn(format=settings.DATETIME_FORMAT)
    genres = tables.ManyToManyColumn()

    class Meta:
        model = Comic
        template_name = "django_tables2/semantic.html"
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend",  # Instead of `desc`
                }
            },
        }
        row_attrs = {"data-id": lambda record: record.pk}
        sequence = (
            "id",
            "title",
            "images",
            "category",
            "status",
            "created_at",
            "genres",
            "updated_at",
        )
        fields = (
            "title",
            "images",
            "category",
            "status",
            "id",
            "created_at",
            "genres",
            "updated_at",
        )

    @classmethod
    def render_paginated_table(cls, request):
        table = cls(
            data=Comic.objects.select_related("category")
            .prefetch_related("genres")
            .all()
        )
        table.paginate(page=request.GET.get("page", 1), per_page=settings.PAGINATE_BY)
        return table


class PanelTable(tables.Table):
    id = MaterializeCssCheckboxColumn(accessor="pk")
    images = ImageColumn()
    comic = ImageColumn(accessor="comic__images")
    chapter = ImageColumn(accessor="chapter__name")

    class Meta:
        model = Panel
        template_name = "django_tables2/semantic.html"
        fields = ("check", "images", "comic", "chapter", "slug")

    @classmethod
    def render_paginated_table(cls, request):
        table = cls(data=Panel.objects.all())
        table.paginate(page=request.GET.get("page", 1), per_page=settings.PAGINATE_BY)
        return table


class UserTable(tables.Table):

    id = MaterializeCssCheckboxColumn(accessor="pk", orderable=False)
    update = tables.TemplateColumn(
        template_name="partials/users/update_button.html", orderable=False
    )
    delete = tables.TemplateColumn(
        template_name="partials/users/delete_button.html", orderable=False
    )
    email = TitleColumn(linkify=True)

    images = ImageColumn(linkify=True)

    class Meta:
        model = User
        template_name = "django_tables2/semantic.html"
        sequence = (
            "id",
            "email",
            "username",
            "images",
            "is_superuser",
        )
        fields = (
            "email",
            "username",
            "images",
            "is_superuser",
            "id",
        )
        attrs = {
            "th": {
                "_ordering": {
                    "orderable": "sortable",  # Instead of `orderable`
                    "ascending": "ascend",  # Instead of `asc`
                    "descending": "descend",  # Instead of `desc`
                }
            },
        }
        row_attrs = {"data-id": lambda record: record.pk}

    @classmethod
    def render_paginated_table(cls, request):
        table = cls(data=User.objects.all())
        table.paginate(page=request.GET.get("page", 1), per_page=settings.PAGINATE_BY)
        return table
