from render_block import render_block_to_string
from core.models import UserComics, Comic, Vote
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.conf import settings
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.http.response import HttpResponse
from core.utils import get_max_order, reorder
from core.decorators import user_only
from django.core.paginator import Paginator
from django_htmx.http import trigger_client_event, HttpResponseClientRefresh
from django.http import JsonResponse
from django.db.models import F, Q


def thumbs(request):
    if request.POST.get("action") == "thumbs":

        id = request.POST.get("comicid")
        button = request.POST.get("button")
        update = Comic.objects.get(id=id)

        if update.thumbs.filter(id=request.user.id).exists():

            query = Q(comic_id=id) & Q(user_id=request.user.id)
            q = Vote.objects.filter(query)[0]
            evote = q.vote

            if evote == True:
                # Now we need action
                if button == "thumbsup":
                    update.thumbsup = F("thumbsup") - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()
                    context = {"up": up, "down": down, "remove": "none"}

                    return JsonResponse(context)

                if button == "thumbsdown":
                    update.thumbsup = F("thumbsup") - 1
                    update.thumbsdown = F("thumbsdown") + 1

                    update.save()
                    q.vote = False
                    q.save(update_fields=["vote"])
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    context = {"up": up, "down": down}

                    return JsonResponse(context)

            if evote == False:

                if button == "thumbsup":
                    update.thumbsup = F("thumbsup") + 1
                    update.thumbsdown = F("thumbsdown") - 1
                    update.save()

                    q.vote = True
                    q.save(update_fields=["vote"])
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown

                    context = {"up": up, "down": down}

                    return JsonResponse(context)

                if button == "thumbsdown":
                    update.thumbsdown = F("thumbsdown") - 1
                    update.thumbs.remove(request.user)
                    update.save()
                    update.refresh_from_db()
                    up = update.thumbsup
                    down = update.thumbsdown
                    q.delete()
                    context = {"up": up, "down": down}
                    return JsonResponse(context)

        else:
            # New Selection

            if button == "thumbsup":
                update.thumbsup = F("thumbsup") + 1
                update.thumbs.add(request.user)
                update.save()
                # Add new Vote
                new = Vote(comic_id=id, user_id=request.user.id, vote=True)
                new.save()
            else:
                update.thumbsdown = F("thumbsdown") + 1
                update.thumbs.add(request.user)
                update.save()
                # Add new Vote
                new = Vote(comic_id=id, user_id=request.user.id, vote=False)
                new.save()

            update.refresh_from_db()
            up = update.thumbsup
            down = update.thumbsdown
            context = {"up": up, "down": down}

            return JsonResponse(context)


@user_only
def like(request):
    if request.POST.get("action") == "comic":
        result = ""
        id = request.POST.get("comicid")
        comic = get_object_or_404(Comic, id=id)
        if comic.likes.filter(id=request.user.id).exists():
            comic.likes.remove(request.user)
            comic.like_count -= 1
            result = comic.like_count
            comic.save()
        else:
            comic.likes.add(request.user)
            comic.like_count += 1
            result = comic.like_count
            comic.save()

        return JsonResponse(
            {
                "result": result,
            }
        )


@require_http_methods(["GET"])
@user_only
@login_required
def bookmarks_list(request):
    comics = UserComics.objects.prefetch_related("comic").filter(user=request.user)
    paginator = Paginator(comics, settings.PAGINATE_BY)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    context = {"comics": page_obj}
    if request.htmx:
        html = render_block_to_string(
            "partials/bookmarks/comic-list.html", "bookmarkComics", context
        )
        return HttpResponse(html)
    return render(request, "core/bookmarks/comics.html", context)


@require_http_methods(["POST", "GET"])
@user_only
@login_required
def add_comic(request):
    title = request.POST.get("comictitle")

    # add comic
    comic = Comic.objects.get_or_create(title=title)[0]

    if not UserComics.objects.filter(comic=comic, user=request.user).exists():

        UserComics.objects.create(
            comic=comic, user=request.user, order=get_max_order(request.user)
        )

    # comics = UserComics.objects.prefetch_related("comic").filter(user=request.user)
    # paginator = Paginator(comics, settings.PAGINATE_BY)
    # page_number = request.GET.get("page", 1)
    # page_obj = paginator.get_page(page_number)
    # html = render_block_to_string(
    #     "partials/bookmarks/comic-list.html",
    #     "bookmarkComics",
    #     {"comics": page_obj},
    # )
    # return HttpResponse(html)
    return HttpResponseClientRefresh()


@require_http_methods(["DELETE", "GET"])
@user_only
@login_required
def delete_comic(request, pk):
    # remove the comic from the user's list
    UserComics.objects.get(comic=pk).delete()

    reorder(request.user)
    # comics = UserComics.objects.prefetch_related("comic").filter(user=request.user)
    # paginator = Paginator(comics, settings.PAGINATE_BY)
    # page_number = request.GET.get("page", 1)
    # page_obj = paginator.get_page(page_number)
    # html = render_block_to_string(
    #     "partials/bookmarks/comic-list.html",
    #     "bookmarkComics",
    #     {"comics": page_obj},
    # )
    # return HttpResponse(html)
    return HttpResponseClientRefresh()


@require_http_methods(["POST"])
@user_only
@login_required
def search_comic(request):
    search_text = request.POST.get("search")

    # look up all comics that contain the text
    # exclude user comics
    usercomics = UserComics.objects.prefetch_related("comic").filter(user=request.user)
    results = Comic.objects.filter(title__icontains=search_text).exclude(
        title__in=usercomics.values_list("comic__title", flat=True)
    )
    context = {"results": results}
    return render(request, "partials/bookmarks/search-results.html", context)


def clear(request):
    return HttpResponse("")


@require_http_methods(["POST", "GET"])
@user_only
@login_required
def sort(request):
    comic_pks_order = request.POST.getlist("comic_order")
    comics = []
    for idx, comic_pk in enumerate(comic_pks_order, start=1):
        usercomic = UserComics.objects.get(pk=comic_pk)
        usercomic.order = idx
        usercomic.save()
        comics.append(usercomic)

    # newcomics = UserComics.objects.prefetch_related("comic").filter(user=request.user)
    # paginator = Paginator(newcomics, settings.PAGINATE_BY)
    # page_number = request.GET.get("page", 1)
    # page_obj = paginator.get_page(page_number)
    # html = render_block_to_string(
    #     "partials/bookmarks/comic-list.html",
    #     "bookmarkComics",
    #     {"comics": page_obj},
    # )
    # return HttpResponse(html)
    return HttpResponseClientRefresh()


@require_http_methods(["GET"])
@user_only
@login_required
def detail(request, pk):
    usercomic = get_object_or_404(UserComics, pk=pk)
    context = {"usercomic": usercomic}
    return render(request, "partials/bookmarks/comic-detail.html", context)


@require_http_methods(["POST"])
@user_only
@login_required
def upload_image(request, pk):
    usercomic = get_object_or_404(UserComics, pk=pk)
    print(request.FILES)
    image = request.FILES.get("image")
    usercomic.comic.images.save(image.name, image)
    context = {"usercomic": usercomic}
    return render(request, "partials/bookmarks/comic-detail.html", context)
