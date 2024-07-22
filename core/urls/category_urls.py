from core.views import category_views
from django.urls import path

app_name = "category"


urlpatterns = [
    path("", category_views.CategoryListView.as_view(), name="list"),
    path("add/", category_views.CategoryCreateView.as_view(), name="add_category"),
    path("<int:pk>/", category_views.CategoryDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/edit/",
        category_views.CategoryUpdateView.as_view(),
        name="edit_category",
    ),
    path(
        "<int:pk>/delete/",
        category_views.category_delete,
        name="delete_category",
    ),
]

htmx_urlpatterns = []

urlpatterns += htmx_urlpatterns
