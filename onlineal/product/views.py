from django.shortcuts import render

# Create your views here.


def product_list_view(request):
    return render(request, "product/shop-banner-sidebar.html")