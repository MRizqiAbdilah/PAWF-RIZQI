from django.urls import path

from .views import (
    CategoryPostListView,
    CustomLoginView,
    CustomLogoutView,
    DashboardCategoryCreateView,
    DashboardCategoryDeleteView,
    DashboardCategoryListView,
    DashboardCategoryUpdateView,
    DashboardPostCreateView,
    DashboardPostDeleteView,
    DashboardPostListView,
    DashboardPostUpdateView,
    PostDetailView,
    PostListView,
)

urlpatterns = [
    # Public pages
    path("", PostListView.as_view(), name="home"),
    path("kategori/<slug:slug>/", CategoryPostListView.as_view(), name="category_posts"),
    path("post/<slug:slug>/", PostDetailView.as_view(), name="post_detail"),

    # Auth custom
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),

    # Dashboard CRUD internal management
    path("dashboard/", DashboardPostListView.as_view(), name="dashboard_home"),
    path("dashboard/post/buat/", DashboardPostCreateView.as_view(), name="dashboard_post_create"),
    path("dashboard/post/<slug:slug>/edit/", DashboardPostUpdateView.as_view(), name="dashboard_post_edit"),
    path("dashboard/post/<slug:slug>/hapus/", DashboardPostDeleteView.as_view(), name="dashboard_post_delete"),

    # Dashboard category management
    path("dashboard/kategori/", DashboardCategoryListView.as_view(), name="dashboard_categories"),
    path("dashboard/kategori/buat/", DashboardCategoryCreateView.as_view(), name="dashboard_category_create"),
    path("dashboard/kategori/<slug:slug>/edit/", DashboardCategoryUpdateView.as_view(), name="dashboard_category_edit"),
    path("dashboard/kategori/<slug:slug>/hapus/", DashboardCategoryDeleteView.as_view(), name="dashboard_category_delete"),
]
