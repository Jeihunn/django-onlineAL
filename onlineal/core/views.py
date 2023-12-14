from django.shortcuts import render

# Create your views here.


def index_view(request):
    return render(request, 'core/index.html')


def contact_us_view(request):
    return render(request, 'core/contact-us.html')

def about_us_view(request):
    return render(request, 'core/about-us.html')