import django_filters
from django import forms
from core.models import Comic, Genre, Chapter, Category
from django.contrib.auth import get_user_model

User = get_user_model()


class ComicFilter(django_filters.FilterSet):
    comic_status = django_filters.ChoiceFilter(
        choices=Comic.options,
        field_name="status",
        lookup_expr="iexact",
        empty_label="Any",
    )
    # start_date = django_filters.DateFilter(
    #     field_name="created_at",
    #     lookup_expr="gte",
    #     label="Date From",
    #     widget=forms.DateInput(attrs={"type": "date", "class": "form-search"}),
    # )

    # end_date = django_filters.DateFilter(
    #     field_name="created_at",
    #     lookup_expr="lte",
    #     label="Date To",
    #     widget=forms.DateInput(attrs={"type": "date", "class": "form-search"}),
    # )
    rating = django_filters.RangeFilter(
        field_name="rating",
        widget=forms.NumberInput(attrs={"placeholder": "0", "class": "form-search"}),
    )

    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )
    genres = django_filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple()
    )
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={"placeholder": "Search Comics Everywhere..", "class": "form-search"}
        ),
    )

    class Meta:
        model = Comic
        fields = (
            "comic_status",
            "title",
            "rating",
            # "end_date",
            "category",
            "genres",
        )


class SearchFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=Comic.options,
        field_name="status",
        lookup_expr="iexact",
        empty_label="Any",
    )

    rating = django_filters.RangeFilter(
        field_name="rating",
        lookup_expr="gte",
        label="Rating",
    )

    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )
    genres = django_filters.ModelMultipleChoiceFilter(
        queryset=Genre.objects.all(),
        # widget=forms.CheckboxSelectMultiple(),
    )
    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={"placeholder": "Search Comics Everywhere..", "class": "form-search"}
        ),
    )

    class Meta:
        model = Comic
        fields = (
            "status",
            "title",
            "rating",
            "category",
            "genres",
        )


class ChapterFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        field_name="name",
        lookup_expr="icontains",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search Chapters Everywhere..",
                "class": "form-search",
            }
        ),
    )

    class Meta:
        model = Chapter
        fields = ("name",)


class UserFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(
        field_name="email",
        lookup_expr="icontains",
        widget=forms.EmailInput(
            attrs={"placeholder": "Search Users Everywhere..", "class": "form-search"}
        ),
    )

    class Meta:
        model = User
        fields = ("email",)
