from core.views import author_views
from django.urls import path

app_name = "author"


urlpatterns = [
    path("", author_views.AuthorListView.as_view(), name="list"),
    path("<int:pk>/", author_views.AuthorDetailView.as_view(), name="detail"),
]

htmx_urlpatterns = []

urlpatterns += htmx_urlpatterns
