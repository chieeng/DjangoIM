from django.shortcuts import render
from django.views.generic import TemplateView


def index(request):
    """Landing page view"""
    context = {
        'title': 'Hotel Management System',
    }
    return render(request, 'landing.html', context)


def about(request):
    """About page view"""
    return render(request, 'common/about.html')


def contact(request):
    """Contact page view"""
    return render(request, 'common/contact.html')
