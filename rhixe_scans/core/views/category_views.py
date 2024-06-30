from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, FormView
from core.models import Category
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic.detail import SingleObjectMixin
from core.forms import CategoryComicFormset
from django.urls import reverse


class CategoryListView(ListView):
    model = Category
    template_name = "core/category/category_list.html"


class CategoryDetailView(DetailView):
    model = Category
    template_name = "core/category/category_detail.html"


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    template_name = "core/category/category_create.html"
    fields = [
        "name",
    ]

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.SUCCESS, "The category has been added"
        )
        return super().form_valid(form)


class CategoryUpdateView(SingleObjectMixin, LoginRequiredMixin, FormView):
    model = Category
    template_name = "core/category/category_update.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().post(request, *args, **kwargs)

    def get_form(self, form_class=None):

        return CategoryComicFormset(**self.get_form_kwargs(), instance=self.object)

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, "Changes were saved.")
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("category:detail", kwargs={"pk": self.object.pk})
