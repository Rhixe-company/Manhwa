from django.shortcuts import render
from django.views.generic import ListView, DetailView
from core.models import Author


class AuthorListView(ListView):
    model = Author
    template_name = "core/author/author_list.html"


class AuthorDetailView(DetailView):
    model = Author
    template_name = "core/author/author_detail.html"
    slug_field = "id"
    slug_url_kwarg = "id"
