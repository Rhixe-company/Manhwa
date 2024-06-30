from core.views import artist_views
from django.urls import path

app_name = "artist"


urlpatterns = [
    path("", artist_views.ArtistListView.as_view(), name="list"),
    path("<int:pk>/", artist_views.ArtistDetailView.as_view(), name="detail"),
]

htmx_urlpatterns = []

urlpatterns += htmx_urlpatterns
