from django.shortcuts import render

# Create your views here.


def blog_list_view(request):
    return render(request, 'blog/blog-listing.html')