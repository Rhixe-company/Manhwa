from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import DetailView
from django.views.generic import RedirectView
from django.views.generic import UpdateView
from core.decorators import admin_only, user_only
from rhixe_scans.users.forms import UserForm, UserAdminForm
from rhixe_scans.users.models import User
from core.tables import UserTable
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django_htmx.http import trigger_client_event, HttpResponseClientRefresh
from render_block import render_block_to_string
from core.filters import UserFilter
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from allauth.account.views import LoginView, SignupView
from django_tables2.export import ExportMixin
from django_tables2.export.export import TableExport
from django.conf import settings
from django_tables2 import RequestConfig
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


def avatar(request):
    if request.user.is_authenticated:
        user = User.objects.get(email=request.user)

        avatar = User.objects.filter(email=user)

        context = {
            "avatar": avatar,
        }
        return context
    else:
        return {"NotLoggedIn": User.objects.none()}


def check_username(request):
    username = request.POST.get("username")

    if User.objects.filter(username=username).exists():
        return HttpResponse(
            " <div class='myerror mt-4' x-data='{ dismissed:false }' x-show='!dismissed' x-init='setTimeout(() =>  dismissed=true, 10000)'><div id='toast'class='mb-4 flex w-full max-w-md items-center rounded-lg bg-white p-4 text-gray-500 shadow dark:bg-gray-800 dark:text-gray-400'role='alert'><div  class='error'><svg class='h-5 w-5' aria-hidden='true' xmlns='http://www.w3.org/2000/svg' fill='currentColor' viewBox='0 0 20 20'><path d='M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z' /></svg><span class='sr-only'>Error icon</span></div><div class='ml-3 text-sm font-normal'>This username already exists</div><button @click='dismissed=true' type='button'class='-mx-1.5 -my-1.5 ml-auto inline-flex h-8 w-8 items-center justify-center rounded-lg bg-white p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-900 focus:ring-2 focus:ring-gray-300 dark:bg-gray-800 dark:text-gray-500 dark:hover:bg-gray-700 dark:hover:text-white'data-dismiss-target='#toast' aria-label='Close'><span class='sr-only'>Close</span><svg class='h-3 w-3' aria-hidden='true' xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 14 14'><path stroke='currentColor' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6' /></svg></button></div></div>"
        )
    else:
        return HttpResponse(
            "<div class='mysuccess    mt-4' x-data='{ dismissed:false }' x-show='!dismissed' x-init='setTimeout(() =>  dismissed=true, 10000)'><div id='toast'class='mb-4 flex w-full max-w-md items-center rounded-lg bg-white p-4 text-gray-500 shadow dark:bg-gray-800 dark:text-gray-400'role='alert'><div class='success' ><svg class='h-5 w-5' aria-hidden='true' xmlns='http://www.w3.org/2000/svg' fill='currentColor' viewBox='0 0 20 20'><path d='M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z' /></svg><span class='sr-only'>Check icon</span></div><div class='ml-3 text-sm font-normal'>This username is available</div><button @click='dismissed=true' type='button' class='-mx-1.5 -my-1.5 ml-auto inline-flex h-8 w-8 items-center justify-center rounded-lg bg-white p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-900 focus:ring-2 focus:ring-gray-300 dark:bg-gray-800 dark:text-gray-500 dark:hover:bg-gray-700 dark:hover:text-white' data-dismiss-target='#toast' aria-label='Close'><span class='sr-only'>Close</span><svg class='h-3 w-3' aria-hidden='true' xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 14 14'><path stroke='currentColor' stroke-linecap='round' stroke-linejoin='round' stroke-width='2'd='m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6' /></svg></button></div></div>"
        )


def check_email(request):
    email = request.POST.get("email")
    if User.objects.filter(email=email).exists():
        return HttpResponse(
            " <div class='myerror mt-4' x-data='{ dismissed:false }' x-show='!dismissed' x-init='setTimeout(() =>  dismissed=true, 10000)'><div id='toast'class='mb-4 flex w-full max-w-md items-center rounded-lg bg-white p-4 text-gray-500 shadow dark:bg-gray-800 dark:text-gray-400'role='alert'><div  class='error'><svg class='h-5 w-5' aria-hidden='true' xmlns='http://www.w3.org/2000/svg' fill='currentColor' viewBox='0 0 20 20'><path d='M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 11.793a1 1 0 1 1-1.414 1.414L10 11.414l-2.293 2.293a1 1 0 0 1-1.414-1.414L8.586 10 6.293 7.707a1 1 0 0 1 1.414-1.414L10 8.586l2.293-2.293a1 1 0 0 1 1.414 1.414L11.414 10l2.293 2.293Z' /></svg><span class='sr-only'>Error icon</span></div><div class='ml-3 text-sm font-normal'>This email already exists</div><button @click='dismissed=true' type='button'class='-mx-1.5 -my-1.5 ml-auto inline-flex h-8 w-8 items-center justify-center rounded-lg bg-white p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-900 focus:ring-2 focus:ring-gray-300 dark:bg-gray-800 dark:text-gray-500 dark:hover:bg-gray-700 dark:hover:text-white'data-dismiss-target='#toast' aria-label='Close'><span class='sr-only'>Close</span><svg class='h-3 w-3' aria-hidden='true' xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 14 14'><path stroke='currentColor' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6' /></svg></button></div></div>"
        )
    else:
        return HttpResponse(
            "<div class='mysuccess    mt-4' x-data='{ dismissed:false }' x-show='!dismissed' x-init='setTimeout(() =>  dismissed=true, 10000)'><div id='toast'class='mb-4 flex w-full max-w-md items-center rounded-lg bg-white p-4 text-gray-500 shadow dark:bg-gray-800 dark:text-gray-400'role='alert'><div class='success' ><svg class='h-5 w-5' aria-hidden='true' xmlns='http://www.w3.org/2000/svg' fill='currentColor' viewBox='0 0 20 20'><path d='M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z' /></svg><span class='sr-only'>Check icon</span></div><div class='ml-3 text-sm font-normal'>This email is available</div><button @click='dismissed=true' type='button' class='-mx-1.5 -my-1.5 ml-auto inline-flex h-8 w-8 items-center justify-center rounded-lg bg-white p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-900 focus:ring-2 focus:ring-gray-300 dark:bg-gray-800 dark:text-gray-500 dark:hover:bg-gray-700 dark:hover:text-white' data-dismiss-target='#toast' aria-label='Close'><span class='sr-only'>Close</span><svg class='h-3 w-3' aria-hidden='true' xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 14 14'><path stroke='currentColor' stroke-linecap='round' stroke-linejoin='round' stroke-width='2'd='m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6' /></svg></button></div></div>"
        )


@require_http_methods(["POST", "GET"])
@user_only
@admin_only
@login_required
def user_list(request):

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():

            email = form.cleaned_data["email"]
            username = form.cleaned_data["username"]
            password1 = form.cleaned_data["password1"]
            images = form.cleaned_data["images"]
            User.objects.create_superuser(
                email=email, username=username, images=images, password=password1
            )

            context = {"form": UserForm()}
        else:
            context = {"form": form}
        html = render_block_to_string(
            "partials/users/create.html", "Userscreate", context
        )
        response = HttpResponse(html)
        if form.is_valid():
            return trigger_client_event(response, "user_added")
            # return HttpResponseClientRefresh()
        return response

    users = User.objects.all()
    myFilter = UserFilter(request.GET, queryset=users)
    table = UserTable(myFilter.qs)
    # table.paginate(page=request.GET.get("page", 1), per_page=settings.PAGINATE_BY)
    RequestConfig(request, paginate={"per_page": settings.PAGINATE_BY}).configure(table)
    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response(f"table.{export_format}")
    form = UserForm()
    export_formats = ["json"]
    context = {
        "table": table,
        "form": form,
        "filter": myFilter,
        "export_formats": export_formats,
    }

    if request.htmx:
        return render(request, "partials/users/table.html", context)

    return render(request, "users/admin.html", context)


class Login(LoginView):
    template_name = "account/login.html"


class RegisterView(SignupView):
    template_name = "account/signup.html"
    # form_class = UserSignupForm

    # def form_valid(self, form):
    #     email = form.cleaned_data["email"]
    #     username = form.cleaned_data["username"]
    #     password1 = form.cleaned_data["password1"]
    #     images = form.cleaned_data["images"]
    #     u = User.objects.get_or_create(email=email, username=username, images=images)[0]
    #     u.set_password(password1)
    #     u.save()

    #     return HttpResponse("")


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "id"
    slug_url_kwarg = "id"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["username", "email", "images", "first_name", "last_name"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        # for mypy to know that the user is authenticated
        assert self.request.user.is_authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail", kwargs={"pk": self.request.user.pk})


user_redirect_view = UserRedirectView.as_view()


@require_http_methods(["GET", "POST"])
@user_only
@login_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserAdminForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            newuser = form.save(commit=False)

            newuser.save()

            context = {
                "record": user,
                "user": user,
                "form": UserAdminForm(instance=user),
            }
        else:
            context = {"record": user, "user": user, "form": form}

        html = render_block_to_string(
            "partials/users/update_button.html", "Usersupdate", context
        )
        response = HttpResponse(html)
        if form.is_valid():
            return trigger_client_event(response, "user_added")
            # return HttpResponseClientRefresh()
        return response

    form = UserAdminForm(instance=user)
    context = {"record": user, "user": user, "form": form}
    html = render_block_to_string(
        "partials/users/update_button.html", "Usersupdate", context
    )
    return HttpResponse(html)


@require_http_methods(["DELETE"])
@admin_only
@login_required
def user_delete(request, pk):
    if User.objects.filter(pk=pk).exists():
        user = get_object_or_404(User, pk=pk)

        user.delete()

        # response = HttpResponse("")

        # return trigger_client_event(response, "user_added")
        return HttpResponseClientRefresh()
