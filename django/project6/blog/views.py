from django.shortcuts import get_object_or_404, render # upadate

from .models import Post


def post_list(request):
    posts = Post.objects.all()
    return render(request, "home.html", {"posts": posts})

# add
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "post_detail.html", {"post": post})
