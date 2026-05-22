from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.index, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/<int:booking_id>/approve/', views.approve_booking, name='approve_booking'),
    path('admin-dashboard/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    path('addNewBooking/', views.add_booking, name='add_booking'),
    path('room/<int:room_id>/book/', views.add_booking, name='book_room'),
]
