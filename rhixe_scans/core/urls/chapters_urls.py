from core.views import chapters_views
from django.urls import path

app_name = "chapters"


urlpatterns = [
    path(
        "",
        view=chapters_views.chapter_list,
        name="list",
    ),
    path(
        "<str:pk>/",
        view=chapters_views.chapter_detail,
        name="detail",
    ),
]

htmx_urlpatterns = [
    path(
        "<str:pk>/update/",
        view=chapters_views.chapter_edit,
        name="update-chapter",
    ),
    path(
        "<str:pk>/delete/",
        view=chapters_views.chapter_delete,
        name="delete-chapter",
    ),
]

urlpatterns += htmx_urlpatterns
