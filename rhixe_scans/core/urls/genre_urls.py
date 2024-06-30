from core.views import genre_views
from django.urls import path

app_name = "genre"


urlpatterns = [
    path("", genre_views.GenreListView.as_view(), name="list"),
    path("<int:pk>/", genre_views.GenreDetailView.as_view(), name="detail"),
]

htmx_urlpatterns = []

urlpatterns += htmx_urlpatterns
