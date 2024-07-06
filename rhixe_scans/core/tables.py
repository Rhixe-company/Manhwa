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
            "<div class='flex items-center'><label><input class='form-checkboxinput' %s/><span></span></label></div>"
            % attrs.as_html()
        )


# class MaterializeCssCheckboxColumn(tables.CheckBoxColumn):
#     def render(self, value, bound_column, record):
#         default = {"type": "checkbox", "name": bound_column.name, "value": value}
#         if self.is_checked(value, record):
#             default.update({"checked": "checked"})

#         general = self.attrs.get("input")
#         specific = self.attrs.get("td__input")
#         attrs = tables.utils.AttributeDict(default, **(specific or general or {}))
#         return mark_safe(
#             '<div class="flex items-center" ><input id="checkbox-table-search-1" type="checkbox" onclick="event.stopPropagation()" class="w-4 h-4 text-primary-600 bg-gray-100 rounded border-gray-300 focus:ring-primary-500 dark:focus:ring-primary-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"  %s/><label for="checkbox-table-search-1" class="sr-only"></label></div>'
#             % attrs.as_html()
#         )


class ImagesColumn(tables.Column):
    def render(self, value):
        return format_html(
            '<div class=" flex items-center p-2 mr-6 space-x-3 "><img class="w-10 h-10 rounded-full"     src="/media/{}" /></div>',
            value,
        )


class Image_urlsColumn(tables.Column):
    def render(self, value):
        return format_html(
            '<div class=" flex items-center p-2 mr-6 space-x-3 "><img class="w-10 h-10 rounded-full"     src="{}" /></div>',
            value,
        )


class TitleColumn(tables.Column):
    def render(self, value):
        return format_html(
            "<span>{}</span>",
            value,
        )


class ChapterTable(tables.Table):
    check = MaterializeCssCheckboxColumn(accessor="pk", orderable=False)
    name = TitleColumn(linkify=True)
    numPages = tables.Column()
    comic = Image_urlsColumn(accessor="comic__image_urls", linkify=True)
    update = tables.TemplateColumn(
        template_name="partials/chapters/update_button.html", orderable=False
    )
    delete = tables.TemplateColumn(
        template_name="partials/chapters/delete_button.html", orderable=False
    )

    class Meta:
        model = Chapter
        # template_name = "django_tables2/semantic.html"
        sequence = ("check", "name", "numPages", "comic", "slug")
        fields = ("check", "name", "numPages", "comic", "slug")
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
        table.paginate(page=request.GET.get("page", 1), per_page=100)
        return table


class ComicTable(tables.Table):
    # id = MaterializeCssCheckboxColumn(accessor="pk", orderable=False)
    check = MaterializeCssCheckboxColumn(accessor="pk")
    update = tables.TemplateColumn(
        template_name="partials/comics/update_button.html", orderable=False
    )
    delete = tables.TemplateColumn(
        template_name="partials/comics/delete_button.html", orderable=False
    )
    title = TitleColumn(linkify=True)
    image_urls = Image_urlsColumn(accessor="image_urls", linkify=True)
    # images = Image_urlsColumn(accessor="images", linkify=True)
    status = tables.Column()
    category = tables.Column()
    # author = tables.Column()
    # artist = tables.Column()
    # created_at = tables.DateColumn(format="M d Y")
    updated_at = tables.DateTimeColumn(format=settings.DATETIME_FORMAT)
    genres = tables.ManyToManyColumn()

    class Meta:
        model = Comic
        # template_name = "django_tables2/semantic.html"
        # template_name = "tables/bootstrap_htmx.html"
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
            "check",
            "title",
            "image_urls",
            "category",
            # "artist",
            # "author",
            "status",
            # "created_at",
            "genres",
            "updated_at",
        )
        fields = (
            "check",
            "title",
            "image_urls",
            "category",
            # "artist",
            # "author",
            "status",
            # "created_at",
            "genres",
            "updated_at",
        )

    @classmethod
    def render_paginated_table(cls, request):
        table = cls(data=Comic.objects.all())
        table.paginate(page=request.GET.get("page", 1), per_page=settings.PAGINATE_BY)
        return table


class PanelTable(tables.Table):
    check = MaterializeCssCheckboxColumn(accessor="pk")
    images = Image_urlsColumn()
    comic = Image_urlsColumn(accessor="comic__image_urls")
    chapter = Image_urlsColumn(accessor="chapter__name")

    class Meta:
        model = Panel
        # template_name = "django_tables2/semantic.html"
        fields = ("check", "images", "comic", "chapter", "slug")

    @classmethod
    def render_paginated_table(cls, request):
        table = cls(data=Panel.objects.all())
        table.paginate(page=request.GET.get("page", 1), per_page=settings.PAGINATE_BY)
        return table


class UserTable(tables.Table):

    check = MaterializeCssCheckboxColumn(accessor="pk", orderable=False)
    update = tables.TemplateColumn(
        template_name="partials/users/update_button.html", orderable=False
    )
    delete = tables.TemplateColumn(
        template_name="partials/users/delete_button.html", orderable=False
    )
    email = TitleColumn(linkify=True)

    images = ImagesColumn(linkify=True)

    class Meta:
        model = User
        # template_name = "django_tables2/semantic.html"
        sequence = (
            "check",
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
            "check",
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
