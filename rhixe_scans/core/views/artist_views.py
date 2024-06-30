from django.shortcuts import render
from django.views.generic import ListView, DetailView
from core.models import Artist


class ArtistListView(ListView):
    model = Artist
    template_name = "core/artist/artist_list.html"


class ArtistDetailView(DetailView):
    model = Artist
    template_name = "core/artist/artist_detail.html"
    slug_field = "id"
    slug_url_kwarg = "id"
