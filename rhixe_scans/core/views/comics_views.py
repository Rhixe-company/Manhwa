from core.decorators import admin_only, user_only
from core.forms import ComicForm
from core.models import Comic, UserComics, Chapter
from core.tables import ComicTable
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django_htmx.http import trigger_client_event, HttpResponseClientRefresh
from render_block import render_block_to_string
from core.filters import ComicFilter, SearchFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export import ExportMixin
from django_tables2.export.export import TableExport
from django.conf import settings
from django_tables2 import RequestConfig
from scraper.tasks import my_task
from django.utils import timezone
from celery_progress.views import get_progress
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from celery.result import AsyncResult
from django.db.models import F, Count, Q


class TaskStatus(LoginRequiredMixin, View):
    def get(self, request, task_id, *args, **kwargs):
        # Other checks could go here
        return get_progress(request, task_id=task_id)


@user_only
@admin_only
@login_required
def progress_view(request):
    result = my_task.delay(10)
    context = {"task_ids": [result.task_id]}
    return render(request, "core/comics/display_progress.html", context)


@login_required
def task_status(request, task_id):
    # result = AsyncResult(task_id)
    # context = {"state": result.state, "info": result.info}
    # # Other checks could go here
    # return HttpResponse(context)
    return get_progress(request, task_id=task_id)


@require_http_methods(["POST", "GET"])
@user_only
@admin_only
@login_required
def comic_list(request):

    if request.method == "POST":
        form = ComicForm(request.POST, request.FILES)
        if form.is_valid():
            comic = form.save(commit=False)
            comic.user = request.user
            genres = form.cleaned_data["genres"]
            if genres:
                comic.genres.set([gen for gen in genres])
            comic.save()
            context = {"form": ComicForm()}
            html = render_block_to_string(
                "partials/comics/create.html", "Comicscreate", context
            )
            response = HttpResponse(html)
            return trigger_client_event(response, "comic_added")
            # return HttpResponseClientRefresh()

        else:
            context = {"form": form}
            html = render_block_to_string(
                "partials/comics/create.html", "Comicscreate", context
            )
            response = HttpResponse(html)

            # return HttpResponseClientRefresh()
            return response

    comics = Comic.objects.all()
    myFilter = ComicFilter(request.GET, queryset=comics)
    table = ComicTable(myFilter.qs)
    # table.paginate(page=request.GET.get("page", 1), per_page=settings.PAGINATE_BY)
    RequestConfig(request, paginate={"per_page": settings.PAGINATE_BY}).configure(table)
    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response(f"table.{export_format}")
    form = ComicForm()
    export_formats = ["json"]
    context = {
        "table": table,
        "form": form,
        "filter": myFilter,
        "export_formats": export_formats,
    }

    if request.htmx:
        return render(request, "partials/comics/table.html", context)

    return render(request, "core/comics/admin.html", context)


class ComicSearchView(SingleTableMixin, FilterView):
    table_class = ComicTable
    model = Comic

    template_name = "core/views/search.html"

    filterset_class = SearchFilter

    def get_template_names(self):
        if self.request.htmx:
            return "partials/searchs/search-results.html"
        return "core/views/search.html"


@require_http_methods(["GET"])
# @user_only
# @admin_only
# @login_required
def index(request):
    page_number = request.GET.get("page", 1)
    startswith = request.GET.get("startswith", "")
    query = Q(title__icontains=startswith)
    comics = Comic.objects.filter(query)
    myFilter = ComicFilter(request.GET, queryset=comics)
    comics = myFilter.qs
    paginator = Paginator(comics, settings.PAGINATE_BY)

    page_obj = paginator.get_page(page_number)
    context = {
        "comics": page_obj,
        "pagecount": page_obj.paginator.num_pages,
        "count": comics.count(),
        "topcomics": Comic.objects.get_topcomics(),
        "featuredcomics": Comic.objects.get_featuredcomics(),
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "myFilter": myFilter,
    }
    if request.htmx:
        return render(request, "partials/pages/grid.html", context)

    return render(request, "core/views/index.html", context)


@require_http_methods(["GET"])
# @user_only
# @admin_only
# @login_required
def comics(request):
    page_number = request.GET.get("page", 1)
    per_page = request.GET.get("per_page", settings.PAGINATE_BY)
    startswith = request.GET.get("startswith", "")
    comics = Comic.objects.filter(title__startswith=startswith)
    myFilter = ComicFilter(request.GET, queryset=comics)
    comics = myFilter.qs
    # nel = request.GET.get("page")
    paginator = Paginator(comics, per_page)

    page_obj = paginator.get_page(page_number)
    context = {
        "comics": page_obj,
        "pagecount": paginator.num_pages,
        "count": comics.count(),
        "page": {
            "current": page_obj.number,
            "has_next": page_obj.has_next(),
            "has_previous": page_obj.has_previous(),
        },
        "myFilter": myFilter,
    }

    return render(request, "core/views/comics.html", context)


@require_http_methods(["GET"])
# @user_only
# @admin_only
# @login_required
def comic_detail(request, pk):

    comic = get_object_or_404(Comic, slug=pk)
    fav = bool
    if request.user.is_authenticated:
        if UserComics.objects.filter(comic=comic, user=request.user).exists():
            fav = True

    chapters = Chapter.objects.select_related("comic").filter(comic__slug=comic.slug)
    genres = [gen.id for gen in comic.genres.all()]
    cat = comic.category.id
    genresquery = Q(genres=genres[0])
    catquery = Q(category=cat)
    not_monthly_created = ~Q(
        created_at__gt=timezone.now() - timezone.timedelta(days=31)
    ) & Q(rating__gte=10.0)
    relatedcomics = (
        Comic.objects.select_related("category")
        .prefetch_related("genres")
        .filter(catquery & genresquery & not_monthly_created)[0:4]
    )

    context = {
        "comic": comic,
        "chapters": chapters,
        "relatedcomics": relatedcomics,
        "fav": fav,
    }

    return render(request, "core/comics/comic.html", context)


@require_http_methods(["GET", "POST"])
@user_only
@admin_only
@login_required
def comic_edit(request, pk):
    comic = get_object_or_404(Comic, slug=pk)
    if request.method == "POST":
        form = ComicForm(request.POST, request.FILES, instance=comic)
        if form.is_valid():

            images = form.cleaned_data["images"]

            newcomic = form.save(commit=False)
            newcomic.images = images
            newcomic.user = request.user
            genres = form.cleaned_data["genres"]
            newcomic.genres.set([gen for gen in genres])
            newcomic.save()

            context = {
                "comic": comic,
                "record": comic,
                "form": ComicForm(instance=comic),
            }
        else:
            context = {"record": comic, "comic": comic, "form": form}

        html = render_block_to_string(
            "partials/comics/update_button.html", "Comicsupdate", context
        )
        response = HttpResponse(html)
        if form.is_valid():

            return trigger_client_event(response, "comic_added")
            # return HttpResponseClientRefresh()
        return response

    form = ComicForm(instance=comic)
    context = {"record": comic, "comic": comic, "form": form}
    html = render_block_to_string(
        "partials/comics/update_button.html", "Comicsupdate", context
    )
    return HttpResponse(html)


@require_http_methods(["DELETE"])
@user_only
@admin_only
@login_required
def comic_delete(request, pk):
    if Comic.objects.filter(slug=pk).exists():
        comic = get_object_or_404(Comic, slug=pk)
        # panels = Panel.objects.filter(comic=comic.pk)
        # panels.delete()
        comic.delete()

        response = HttpResponse("")

        return trigger_client_event(response, "comic_added")
        # return HttpResponseClientRefresh()
