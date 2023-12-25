from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import gettext_lazy as _
from django.http import Http404

from .models import BlogPost, BlogCategory


# Create your views here.


def blog_list_view(request):
    category_slug = request.GET.get("category")
    query = request.GET.get("query")

    blog_posts = BlogPost.objects.filter(
        is_active=True).order_by("-created_at")

    category = None

    if category_slug:
        category = get_object_or_404(
            BlogCategory, slug=category_slug, is_active=True)
        blog_posts = blog_posts.filter(category=category)

    if query:
        blog_posts = blog_posts.filter(title__icontains=query)

    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(blog_posts, 1)

    try:
        blog_posts = paginator.page(page)
    except PageNotAnInteger:
        raise Http404(_("Invalid page number."))
    except EmptyPage:
        raise Http404(_("Invalid page number."))

    # Elipsis Pagination
    index = blog_posts.number - 1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index - 3 else max_index

    page_range = paginator.page_range[start_index:end_index]

    context = {
        "blog_posts": blog_posts,
        "selected_category": category,
        "selected_query": query,
        "page_range": page_range,
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
