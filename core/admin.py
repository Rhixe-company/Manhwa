from django.contrib import admin
from .models import (
    Category,
    Chapter,
    Comic,
    Comment,
    Genre,
    Panel,
    UserComics,
    Artist,
    Author,
    Vote,
)

# from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# from mptt.admin import MPTTModelAdmin
# from django_ckeditor_5.widgets import CKEditor5Widget


class PanelInline(admin.TabularInline):
    model = Panel
    extra = 2


class ComicInline(admin.TabularInline):
    model = Comic
    extra = 2


class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 2


@admin.register(Comic)
class ComicAdminConfig(admin.ModelAdmin):
    model = Comic
    search_fields = (
        "title",
        "slug",
        "alternativetitle",
    )
    list_filter = ("alternativetitle",)
    ordering = ("-updated_at",)
    list_display = (
        "title",
        "images",
        "slug",
    )
    prepopulated_fields = {"slug": ("title",)}
    inlines = [ChapterInline]


@admin.register(Chapter)
class ChapterAdminConfig(admin.ModelAdmin):
    model = Chapter
    search_fields = (
        "name",
        "slug",
    )
    list_filter = (
        "name",
        "slug",
    )
    ordering = ("-updated_at",)
    list_display = (
        "name",
        "slug",
    )
    inlines = [PanelInline]


@admin.register(Category)
class CategoryAdminConfig(admin.ModelAdmin):
    model = Category

    inlines = [ComicInline]


# Register your models here.
admin.site.register(Panel)

admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Artist)


# class CommentAdminForm(forms.ModelForm):

#     class Meta:
#         model = Comment
#         fields = "__all__"
#         widgets = {"body": CKEditor5Widget(attrs={"class": "django_ckeditor_5"})}


# class CommentAdmin(MPTTModelAdmin):
#     form = CommentAdminForm


admin.site.register(Comment)
admin.site.register(UserComics)
admin.site.register(Vote)
