from django.shortcuts import render
from django.views.generic import TemplateView
from rooms.models import Room, RoomType


def index(request):
    """Landing page view"""
    featured_rooms = Room.objects.filter(status='available').select_related('room_type').order_by('price_per_night')[:6]
    context = {
        'title': 'Hotel Management System',
        'featured_rooms': featured_rooms,
        'room_types': RoomType.objects.all(),
    }
    return render(request, 'index.html', context)


def about(request):
    """About page view"""
    return render(request, 'common/about.html')


def contact(request):
    """Contact page view"""
    return render(request, 'common/contact.html')


def home(request):
    """Home page view"""
    return render(request, 'common/index.html')