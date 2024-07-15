from core.views import comics_views
from django.urls import path


app_name = "comics"


urlpatterns = [
    # path(
    #     "",
    #     view=comics_views.index,
    #     name="index",
    # ),
    path("search/", view=comics_views.ComicSearchView.as_view(), name="search"),
    path(
        "comics/",
        view=comics_views.comics,
        name="comics",
    ),
    path("<str:pk>/", view=comics_views.comic_detail, name="detail"),
    path(
        "page/comics/",
        view=comics_views.comic_list,
        name="list",
    ),
]

htmx_urlpatterns = [
    path(
        "page/comics/<str:pk>/update/",
        view=comics_views.comic_edit,
        name="update-comic",
    ),
    path("<str:pk>/delete/", view=comics_views.comic_delete, name="delete-comic"),
]

urlpatterns += htmx_urlpatterns
