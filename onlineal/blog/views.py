from django.shortcuts import render
from django.shortcuts import render, get_object_or_404

from .models import BlogPost, BlogCategory


# Create your views here.


def blog_list_view(request):
    category_slug = request.GET.get("category")
    query = request.GET.get("query")
                            
    blog_posts = BlogPost.objects.filter(is_active=True).order_by("-created_at")

    category = None

    if category_slug:
        category = get_object_or_404(
            BlogCategory, slug=category_slug, is_active=True)
        blog_posts = blog_posts.filter(category=category)

    if query:
        blog_posts = blog_posts.filter(title__icontains=query)

    context = {
        "blog_posts": blog_posts,
        "selected_category": category,
        "selected_query": query,
    }
    return render(request, 'blog/blog-listing.html', context)


def blog_detail_view(request, slug):
    blog_post = get_object_or_404(BlogPost, slug=slug, is_active=True)

    blog_post.view_count += 1
    blog_post.save()

    context = {
        "blog_post": blog_post,
    }
    return render(request, 'blog/post-single.html', context)
