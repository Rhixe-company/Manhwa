from django.shortcuts import render

from django.contrib import messages


def user_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You are not authorized to view this page")
            return render(
                request,
                "partials/error.html",
            )

    return wrapper_function


def admin_only(view_func):
    def wrapper_function(request, *args, **kwargs):
        user = request.user
        if user.is_authenticated and user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            messages.error(request, "You are not authorized to view this page")
            return render(
                request,
                "partials/error.html",
            )

    return wrapper_function
