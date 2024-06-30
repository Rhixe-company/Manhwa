# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from core.views import comics_views
from rhixe_scans.users import views as users_views
from django.conf.urls.i18n import i18n_patterns
from allauth.account.decorators import secure_admin_login


admin.autodiscover()
admin.site.login = secure_admin_login(admin.site.login)


urlpatterns = i18n_patterns(
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        "",
        view=comics_views.index,
        name="index",
    ),
    path("comics/", include("core.urls.comics_urls", namespace="comics")),
    path("bookmarks/", include("core.urls.usercomics_urls", namespace="bookmarks")),
    path("chapters/", include("core.urls.chapters_urls", namespace="chapters")),
    # Django Admin, use {% url 'admin:index' %}
    # User management
    path("users/", include("rhixe_scans.users.urls", namespace="users")),
    path("category/", include("core.urls.category_urls", namespace="category")),
    path("genre/", include("core.urls.genre_urls", namespace="genre")),
    path("artist/", include("core.urls.artist_urls", namespace="artist")),
    path("author/", include("core.urls.author_urls", namespace="author")),
    path(
        "progress/",
        view=comics_views.progress_view,
        name="progress",
    ),
    path(
        "task-status/<str:task_id>",
        comics_views.task_status,
        name="task_status",
    ),
    path("ckeditor/", include("ckeditor_uploader.urls")),
    path("accounts/signup/", view=users_views.RegisterView.as_view()),
    path("accounts/login/", view=users_views.LoginView.as_view()),
    path("accounts/2fa/", users_views.index, name="mfa_index"),
    path(
        "accounts/2fa/authenticate/",
        users_views.authenticate,
        name="mfa_authenticate",
    ),
    path(
        "accounts/2fa/reauthenticate/",
        users_views.reauthenticate,
        name="mfa_reauthenticate",
    ),
    path("accounts/", include("allauth.urls")),
    path("accounts/", include("allauth.socialaccount.urls")),
    path("captcha/", include("captcha.urls")),
)

if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
    if "django_browser_reload" in settings.INSTALLED_APPS:

        urlpatterns = [
            path("__reload__/", include("django_browser_reload.urls")),
        ] + urlpatterns
