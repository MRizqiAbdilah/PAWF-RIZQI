from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import ProtectedError, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import CategoryForm, CustomAuthenticationForm, DashboardSearchForm, PostForm
from .models import Category, Post


class DashboardMixin(LoginRequiredMixin):
    login_url = "/login/"
    extra_context = {"dashboard_view": True}


class PostListView(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        query = self.request.GET.get("q", "")
        slug = self.kwargs.get("slug")
        queryset = Post.objects.filter(is_published=True)
        if slug:
            queryset = queryset.filter(category__slug=slug)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query)
                | Q(body__icontains=query)
                | Q(category__name__icontains=query)
            )
        return queryset.select_related("category", "author")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_query"] = self.request.GET.get("q", "")
        context["categories"] = Category.objects.all()
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"


class DashboardPostListView(DashboardMixin, ListView):
    model = Post
    template_name = "blog/dashboard_home.html"
    context_object_name = "posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class DashboardCategoryListView(DashboardMixin, ListView):
    model = Category
    template_name = "blog/dashboard_categories.html"
    context_object_name = "categories"


class DashboardCategoryCreateView(DashboardMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = "blog/dashboard_form.html"
    success_url = reverse_lazy("dashboard_categories")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create New Category"
        context["cancel_url"] = "dashboard_categories"
        return context


class DashboardCategoryUpdateView(DashboardMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = "blog/dashboard_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("dashboard_categories")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Category"
        context["cancel_url"] = "dashboard_categories"
        return context


class DashboardCategoryDeleteView(DashboardMixin, DeleteView):
    model = Category
    template_name = "blog/dashboard_category_delete.html"
    context_object_name = "category"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("dashboard_categories")

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                f"Kategori '{self.object.name}' tidak dapat dihapus karena masih memiliki post. "
                "Pindahkan atau hapus post tersebut terlebih dahulu.",
            )
            return redirect(self.success_url)


class DashboardPostCreateView(DashboardMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/dashboard_form.html"
    success_url = reverse_lazy("dashboard_home")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Create New Post"
        context["cancel_url"] = "dashboard_home"
        return context


class DashboardPostUpdateView(DashboardMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/dashboard_form.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("dashboard_home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Update Post"
        context["cancel_url"] = "dashboard_home"
        return context


class DashboardPostDeleteView(DashboardMixin, DeleteView):
    model = Post
    template_name = "blog/dashboard_delete.html"
    context_object_name = "post"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    success_url = reverse_lazy("dashboard_home")


class CustomLoginView(LoginView):
    template_name = "blog/login.html"
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True


class CustomLogoutView(LogoutView):
    next_page = "/"


class CategoryPostListView(PostListView):
    def get_queryset(self):
        return super().get_queryset()