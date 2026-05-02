from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache


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

@never_cache
@login_required(login_url='accounts:login')
def home(request):
    context = {
        'session_user_name': request.session.get('user_display_name', request.user.get_full_name() or request.user.username),
        'session_login_time': request.session.get('login_time'),
        'session_last_activity': request.session.get('last_activity'),
    }
    request.session['last_activity'] = 'home'
    return render(request, 'home.html', context)


@login_required(login_url='accounts:login')
def add_new_record(request):
    request.session['last_activity'] = 'add_new_record_redirect'
    return redirect('booking:add_booking')


@login_required(login_url='accounts:login')
def edit_profile_redirect(request):
    request.session['last_activity'] = 'edit_profile_redirect'
    return redirect('accounts:edit_profile')


@login_required(login_url='accounts:login')
def logoff_redirect(request):
    return redirect('accounts:logout')
