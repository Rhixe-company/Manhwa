from django.shortcuts import render
from django.views.generic import ListView, DetailView
from core.models import Genre


class GenreListView(ListView):
    model = Genre
    template_name = "core/genres/genre_list.html"


class GenreDetailView(DetailView):
    model = Genre
    template_name = "core/genres/genre_detail.html"
    slug_field = "id"
    slug_url_kwarg = "id"
