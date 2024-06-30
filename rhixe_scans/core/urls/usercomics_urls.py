from core.views import usercomics_views
from django.urls import path

app_name = "bookmarks"


urlpatterns = [
    path(
        "",
        view=usercomics_views.bookmarks_list,
        name="list",
    ),
    path("like/", usercomics_views.like, name="like"),
    path("thumbs/", usercomics_views.thumbs, name="thumbs"),
]

htmx_urlpatterns = [
    path("add-comic/", usercomics_views.add_comic, name="add-comic"),
    path(
        "delete-comic/<str:pk>/",
        usercomics_views.delete_comic,
        name="delete-comic",
    ),
    path("search-comic/", usercomics_views.search_comic, name="search-comic"),
    path("clear/", usercomics_views.clear, name="clear"),
    path("sort/", usercomics_views.sort, name="sort"),
    # path("detail/<str:pk>/", usercomics_views.detail, name="detail"),
    # path(
    #     "comic-list-partial",
    #     usercomics_views.comics_partial,
    #     name="comic-list-partial",
    # ),
    path(
        "upload-image/<str:pk>/",
        usercomics_views.upload_image,
        name="upload-image",
    ),
]

urlpatterns += htmx_urlpatterns
