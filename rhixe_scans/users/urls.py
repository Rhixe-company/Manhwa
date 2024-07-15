from django.urls import path


from . import views

app_name = "users"

urlpatterns = [
    path("~redirect/", view=views.user_redirect_view, name="redirect"),
    path("~update/", view=views.user_update_view, name="update"),
    path("<int:pk>/", view=views.user_detail_view, name="detail"),
    path(
        "",
        view=views.user_list,
        name="list",
    ),
]

htmx_urlpatterns = [
    path(
        "<int:pk>/update/",
        view=views.user_edit,
        name="update-user",
    ),
    path(
        "<int:pk>/delete/",
        view=views.user_delete,
        name="delete-user",
    ),
    path("check-username/", views.check_username, name="check-username"),
    path("check-email/", views.check_email, name="check-email"),
]

urlpatterns += htmx_urlpatterns
