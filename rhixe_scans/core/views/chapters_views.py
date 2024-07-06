from django_tables2 import RequestConfig
from core.decorators import admin_only, user_only
from core.forms import ChapterForm, NewCommentForm
from core.models import Chapter, Comment, Panel
from core.tables import ChapterTable
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.views.decorators.http import require_http_methods
from django_htmx.http import trigger_client_event, HttpResponseClientRefresh

from render_block import render_block_to_string
from core.filters import ChapterFilter

from django.conf import settings
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2.export.export import TableExport
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse


@require_http_methods(["POST", "GET"])
@user_only
@admin_only
@login_required
def chapter_list(request):

    if request.method == "POST":
        form = ChapterForm(request.POST)
        if form.is_valid():
            chapter = form.save(commit=False)

            chapter.comic = form.cleaned_data["comic"]
            chapter.save()
            context = {"form": ChapterForm()}
        else:
            context = {"form": form}
        html = render_block_to_string(
            "partials/chapters/create.html", "Chapterscreate", context
        )
        response = HttpResponse(html)
        if form.is_valid():
            return trigger_client_event(response, "chapter_added")
            # return HttpResponseClientRefresh()
        return response

    chapters = Chapter.objects.all()
    myFilter = ChapterFilter(request.GET, queryset=chapters)
    table = ChapterTable(myFilter.qs)
    # table.paginate(page=request.GET.get("page", 1), per_page=settings.PAGINATE_BY)
    RequestConfig(request, paginate={"per_page": settings.PAGINATE_BY}).configure(table)
    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response(f"table.{export_format}")
    form = ChapterForm()
    export_formats = ["json"]
    context = {
        "table": table,
        "form": form,
        "filter": myFilter,
        "export_formats": export_formats,
    }

    if request.htmx:
        return render(request, "partials/chapters/table.html", context)

    return render(request, "core/chapters/admin.html", context)


@require_http_methods(["GET", "POST"])
@user_only
# @admin_only
@login_required
def chapter_detail(request, pk):
    chapter = get_object_or_404(Chapter, slug=pk)
    pagedata = Panel.objects.select_related("chapter").filter(
        chapter__slug=chapter.slug
    )
    allcomments = chapter.comment_chapter.all()
    page = request.GET.get("page", 1)

    paginator = Paginator(allcomments, settings.PAGINATE_BY)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    if request.method == "POST":
        comment_form = NewCommentForm(request.POST)
        if comment_form.is_valid():

            comment = comment_form.save(commit=False)

            comment.user = request.user
            comment.chapter = Chapter.objects.get(id=pk)
            comment.save()

            return HttpResponseRedirect("/chapters/" + chapter.slug)
    else:
        comment_form = NewCommentForm()

    context = {
        "chapter": chapter,
        "pages": pagedata,
        "comments": comments,
        "comment_form": comment_form,
        "allcomments": allcomments,
    }

    return render(request, "core/chapters/chapter.html", context)


@require_http_methods(["GET", "POST"])
@user_only
@login_required
def chapter_edit(request, pk):
    chapter = get_object_or_404(Chapter, id=pk)
    if request.method == "POST":
        form = ChapterForm(request.POST, instance=chapter)
        if form.is_valid():
            newchapter = form.save(commit=False)

            newchapter.comic = form.cleaned_data["comic"]
            newchapter.save()
            context = {
                "record": chapter,
                "chapter": chapter,
                "form": ChapterForm(instance=chapter),
            }
        else:
            context = {"record": chapter, "chapter": chapter, "form": form}

        html = render_block_to_string(
            "partials/chapters/update_button.html", "Chaptersupdate", context
        )
        response = HttpResponse(html)
        if form.is_valid():
            # return trigger_client_event(response, "chapter_added")
            return HttpResponseClientRefresh()
        return response
    form = ChapterForm(instance=chapter)
    context = {"record": chapter, "chapter": chapter, "form": form}
    html = render_block_to_string(
        "partials/chapters/update_button.html", "Chaptersupdate", context
    )
    return HttpResponse(html)


@require_http_methods(["DELETE"])
@admin_only
@login_required
def chapter_delete(request, pk):
    if Chapter.objects.filter(id=pk).exists():
        chapter = get_object_or_404(Chapter, id=pk)

        chapter.delete()

        response = HttpResponse("")

        return trigger_client_event(response, "chapter_added")
        # return HttpResponseClientRefresh()
