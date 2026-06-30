from django.urls import path

from .views import post_detail, post_list

urlpatterns = [
    path("post/<int:pk>/", post_detail, name="post_detail"),
    path("", post_list, name="home"),
]
