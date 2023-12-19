from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from .models import BlogPost, BlogCategory


# Create your views here.


def blog_list_view(request):
    blog_posts = BlogPost.objects.filter(is_active=True).order_by("-created_at")

    context = {
        "blog_posts": blog_posts,
    }
    return render(request, 'blog/blog-listing.html', context)


def blog_detail_view(request, slug):
    blog = get_object_or_404(BlogPost, slug=slug, is_active=True)

    context = {
        "blog": blog,
    }
    return render(request, 'blog/post-single.html', context)
