from django import forms
from .models import Category, Chapter, Comic, Comment, Genre, Panel
from django.utils.translation import gettext_lazy as _
from django.forms.models import inlineformset_factory
from mptt.forms import TreeNodeChoiceField
from django_ckeditor_5.widgets import CKEditor5Widget


class ComicForm(forms.ModelForm):

    # category = forms.ModelChoiceField(
    #     queryset=Category.objects.all(), widget=forms.RadioSelect()
    # )
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )
    # images = forms.FileField(label="Images",required=False)

    class Meta:
        model = Comic
        fields = [
            "title",
            "alternativetitle",
            # "slug",
            "images",
            "image_urls",
            "serialization",
            "postedby",
            "url",
            "rating",
            "numChapters",
            "status",
            "author",
            "artist",
            "category",
            "released",
            "description",
            "crawled",
            # "updated_at",
            "created_at",
            "genres",
        ]
        # fields = "__all__"
        # exclude = ["users", "user", "id"]
        widgets = {
            "title": forms.TextInput(
                attrs={"placeholder": _("Enter  Title"), "class": "form-charinput"}
            ),
            "alternativetitle": forms.TextInput(
                attrs={
                    "placeholder": _("Enter Alternative Title"),
                    "class": "form-charinput",
                }
            ),
            # "slug": forms.TextInput(
            #     attrs={"placeholder": _("Enter  Slug"), "class": "form-charinput"}
            # ),
            "image_urls": forms.URLInput(attrs={"class": "form-charinput"}),
            "serialization": forms.TextInput(attrs={"class": "form-charinput"}),
            "postedby": forms.TextInput(attrs={"class": "form-charinput"}),
            "url": forms.URLInput(attrs={"class": "form-charinput"}),
            "rating": forms.NumberInput(attrs={"class": "form-charinput"}),
            "numChapters": forms.NumberInput(attrs={"class": "form-charinput"}),
            "status": forms.Select(attrs={"class": "form-selectinput"}),
            "author": forms.Select(attrs={"class": "form-selectinput"}),
            "artist": forms.Select(attrs={"class": "form-selectinput"}),
            "category": forms.Select(attrs={"class": "form-selectinput"}),
            "released": forms.TextInput(
                attrs={"placeholder": _("Enter  Released"), "class": "form-charinput"}
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": _("Enter  Description"),
                    "rows": "4",
                    "class": "form-textareainput",
                }
            ),
            "crawled": forms.DateInput(
                attrs={"type": "date", "class": "form-charinput"}
            ),
            # "updated_at": forms.DateInput(
            #     attrs={"type": "date", "class": "form-charinput"}
            # ),
            "created_at": forms.DateInput(
                attrs={"type": "date", "class": "form-charinput"}
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields["images"].required = False
        self.fields["images"].widget.attrs.update({"class": "form-fileinput"})

    def clean(self):
        cleaned_data = super().clean()

        return cleaned_data

    # def save(self, request):
    #     comic = super(ComicForm, self).save(request)
    #     comic.images = self.cleaned_data["images"]

    #     comic.save()
    #     print(comic.images)
    #     return comic


class ChapterForm(forms.ModelForm):
    comic = forms.ModelChoiceField(queryset=Comic.objects.all())

    class Meta:
        model = Chapter
        # fields = "__all__"
        fields = [
            "name",
            "comic",
            "numPages",
            "url",
            "crawled",
        ]

        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": _("Enter  Name"), "class": "form-charinput"}
            ),
            # "slug": forms.TextInput(
            #     attrs={"placeholder": _("Enter  Slug"), "class": "form-charinput"}
            # ),
            "url": forms.URLInput(attrs={"class": "form-charinput"}),
            "numPages": forms.NumberInput(attrs={"class": "form-charinput"}),
            "comic": forms.Select(attrs={"class": "form-selectinput"}),
            "crawled": forms.DateInput(
                attrs={"type": "date", "class": "form-charinput"}
            ),
        }


CategoryComicFormset = inlineformset_factory(
    Category,
    Comic,
    fields=[
        "title",
        "alternativetitle",
        "slug",
        "images",
        "image_urls",
        "serialization",
        "postedby",
        "url",
        "rating",
        "numChapters",
        "status",
        "author",
        "artist",
        "category",
        "released",
        "description",
        "crawled",
        "updated_at",
        "created_at",
        "genres",
    ],
    widgets={
        "title": forms.TextInput(
            attrs={"placeholder": _("Enter  Title"), "class": "form-charinput"}
        ),
        "alternativetitle": forms.TextInput(
            attrs={
                "placeholder": _("Enter Alternative Title"),
                "class": "form-charinput",
            }
        ),
        "slug": forms.TextInput(
            attrs={"placeholder": _("Enter  Slug"), "class": "form-charinput"}
        ),
        "image_urls": forms.URLInput(attrs={"class": "form-charinput"}),
        "images": forms.FileInput(attrs={"class": "form-files form-charinput"}),
        "serialization": forms.TextInput(attrs={"class": "form-charinput"}),
        "postedby": forms.TextInput(attrs={"class": "form-charinput"}),
        "url": forms.URLInput(attrs={"class": "form-charinput"}),
        "rating": forms.NumberInput(attrs={"class": "form-charinput"}),
        "numChapters": forms.NumberInput(attrs={"class": "form-charinput"}),
        "status": forms.Select(attrs={"class": "form-selectinput"}),
        "author": forms.Select(attrs={"class": "form-selectinput"}),
        "artist": forms.Select(attrs={"class": "form-selectinput"}),
        "category": forms.Select(attrs={"class": "form-selectinput"}),
        "genres": forms.CheckboxSelectMultiple(),
        "released": forms.TextInput(
            attrs={"placeholder": _("Enter  Released"), "class": "form-charinput"}
        ),
        "description": forms.Textarea(
            attrs={
                "placeholder": _("Enter  Description"),
                "rows": "4",
                "class": "form-textareainput",
            }
        ),
        "crawled": forms.DateInput(attrs={"type": "date", "class": "form-charinput"}),
        "updated_at": forms.DateInput(
            attrs={"type": "date", "class": "form-charinput"}
        ),
        "created_at": forms.DateInput(
            attrs={"type": "date", "class": "form-charinput"}
        ),
    },
    extra=1,
)


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())
    body = forms.Textarea()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["parent"].widget.attrs.update({"class": "form-selectinput"})
        self.fields["parent"].label = ""
        self.fields["parent"].required = False

    class Meta:
        model = Comment
        fields = ("name", "body", "parent")

        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": _("Enter  Name"), "class": "form-charinput"}
            ),
            # "body": CKEditor5Widget(
            #     # attrs={
            #     #     "rows": "6",
            #     #     "class": "django_ckeditor_5 px-0 w-full text-sm text-gray-900 border-0 focus:ring-0 focus:outline-none dark:text-white dark:placeholder-gray-400 dark:bg-gray-800",
            #     #     "placeholder": _("Write a comment..."),
            #     # }
            # ),
        }

    # def save(self, *args, **kwargs):
    #     Comment.objects.rebuild()
    #     return super(NewCommentForm, self).save(*args, **kwargs)


from django.conf import settings
from django.core.validators import FileExtensionValidator


class UploadFileForm(forms.Form):
    upload = forms.FileField(
        validators=[
            FileExtensionValidator(
                getattr(
                    settings,
                    "CKEDITOR_5_UPLOAD_FILE_TYPES",
                    ["ico", "jpg", "svg", "jpeg", "png", "gif", "bmp", "webp", "tiff"],
                ),
            ),
        ],
    )
