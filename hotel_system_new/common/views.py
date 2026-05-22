from django.shortcuts import render, redirect
from django.views.generic import TemplateView


def index(request):
    """Home page."""
    context = {
        'title': 'Hotel Management System',
        'username': request.session.get('username'),
        'user_type': request.session.get('user_type'),
    }
    return render(request, 'landing.html', context)


def about(request):
    """About page view"""
    if not request.session.get('username'):
        return redirect('accounts:login')

    return render(request, 'common/about.html')


def contact(request):
    """Contact page view"""
    if not request.session.get('username'):
        return redirect('accounts:login')

    return render(request, 'common/contact.html')
